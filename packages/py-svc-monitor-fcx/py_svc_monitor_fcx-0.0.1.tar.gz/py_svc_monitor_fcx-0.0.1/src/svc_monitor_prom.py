from svc_monitor import SVCMonitor
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Gauge,
    Counter,
    Histogram,
    Summary
)
from starlette.requests import Request
from starlette.responses import Response
import time
from typing import Any, List, Optional, Dict
from prometheus_client import Counter, Histogram, Gauge
from starlette.requests import Request
from starlette.routing import Route, Match, Mount
from starlette.types import Message, Receive, Send, Scope, ASGIApp

def get_matching_route_path(
    scope: Dict[Any, Any], routes: List[Route], route_name: Optional[str] = None
) -> Optional[str]:
    """
    Find a matching route and return its original path string
    From https://github.com/elastic/apm-agent-python
    """
    for route in routes:
        match, child_scope = route.matches(scope)
        if match == Match.FULL:
            route_name = route.path
            child_scope = {**scope, **child_scope}
            if isinstance(route, Mount) and route.routes:
                child_route_name = get_matching_route_path(
                    child_scope, route.routes, route_name
                )
                if child_route_name is None:
                    route_name = None
                else:
                    route_name += child_route_name
            return route_name
        elif match == Match.PARTIAL and route_name is None:
            route_name = route.path

class SVCMonitorPrometheus(SVCMonitor):
  def __init__(self, name, metricType, serviceName, url_prefix='', metric_prefix=''):
    super().__init__(name, metricType, serviceName)

    if (type(url_prefix) != str) | (type(metric_prefix) != str):
      raise Exception('Monitor parameters are not valid.')
    
    self._url_prefix = url_prefix 
    self._metric_prefix = self.make_metric_prefix(metric_prefix)

    self.counters = {}
    self.gauges = {}
    self.histograms = {}
    self.summaries = {}

    # Prometheus' python client automatically makes default metrics

    self.reqCountGauge, self.reqDurationGauge = self.create_routes_monitor_metrics()


  def handle_metrics(self, request: Request) -> Response:
    registry = REGISTRY

    headers = {"Content-Type": CONTENT_TYPE_LATEST}
    return Response(generate_latest(registry), status_code=200, headers=headers)

  def start_app(self, app):
    app.add_middleware(
    PromMiddleware, 
    counters=self.counters, 
    histograms=self.histograms,
    gauges=self.gauges,
    summaries=self.summaries,
    )
    app.add_route("/metrics", self.handle_metrics)

  def make_metric_prefix(self, prefix=None):
    if prefix:
      if (not prefix.endswith('_')):
        prefix += '_'
    else:
      prefix = ''

    return prefix


  def make_metric_name(self, name):
    metric_name = name.lower().replace('-', '_')

    return metric_name

  
  def create_routes_monitor_metrics(self):
    reqCountGauge = self.addGauge(
      'http_request_count', 
      (
        'method',
        'path',
        'status',
        'app_name',
      ),
      'Service HTTP request count'
    )

    reqDurationGauge = self.addGauge(
      'http_request_duration_seconds',
      (
        'method',
        'path',
        'status',
        'app_name',
      ),
      'Service HTTP request duration (seconds)'
    )
    
    return reqCountGauge, reqDurationGauge


  def addGauge(self, name, labelnames, documentation):
    metric_name = self.make_metric_name(name)

    if metric_name in self.gauges:
      raise Exception(f'Gauge {name} already exists')
    
    name = self._metric_prefix + metric_name

    self.gauges[metric_name] = Gauge(name=name, labelnames=labelnames, documentation=documentation)
    
    return self.gauges[metric_name]


  def getGauge(self, name, params=None):
    if self.make_metric_name(name) in self.gauges:
      g = self.gauges[self.make_metric_name(name)]
    else:
      g = self.addGauge(params['name'], params['labels'], params['help'])

    return g


  def addCounter(self, name, labelnames, documentation):
    metric_name = self.make_metric_name(name)

    if metric_name in self.counters:
      raise Exception(f'Counter {name} already exists')
    
    name = self._metric_prefix + metric_name

    self.counters[metric_name] = Counter(name=name, labelnames=labelnames, documentation=documentation)
    
    return self.counters[metric_name]


  def getCounter(self, name, params=None):
    if self.make_metric_name(name) in self.counters:
      c = self.counters[self.make_metric_name(name)]
    else:
      c = self.addCounter(params['name'], params['labels'], params['help'])

    return c


  def addHistogram(self, name, labelnames, documentation):
    metric_name = self.make_metric_name(name)

    if metric_name in self.histograms:
      raise Exception(f'Histogram {name} already exists')
    
    name = self._metric_prefix + metric_name

    self.histograms[metric_name] = Histogram(name=name, labelnames=labelnames, documentation=documentation)
    
    return self.histograms[metric_name]


  def getHistogram(self, name, params=None):
    if self.make_metric_name(name) in self.histograms:
      h = self.histograms[self.make_metric_name(name)]
    else:
      h = self.addHistogram(params['name'], params['labels'], params['help'])

    return h


  def addSummary(self, name, labelnames, documentation):
    metric_name = self.make_metric_name(name)

    if metric_name in self.summaries:
      raise Exception(f'Summary {name} already exists')
    
    name = self._metric_prefix + metric_name

    self.summaries[metric_name] = Summary(name=name, labelnames=labelnames, documentation=documentation)
    
    return self.summaries[metric_name]


  def getSummary(self, name, params=None):
    if self.make_metric_name(name) in self.summaries:
      s = self.summaries[self.make_metric_name(name)]
    else:
      s = self.addSummary(params['name'], params['labels'], params['help'])

    return s

class PromMiddleware:
  def __init__(self, app: ASGIApp, counters, histograms, gauges, summaries):
    self.app = app
    self.counters = counters 
    self.histograms = histograms
    self.gauges = gauges
    self.summaries = summaries


  async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] not in ["http"]:
        await self.app(scope, receive, send)
        return

    request = Request(scope, receive)

    method = request.method
    path = request.url.path

    begin = time.perf_counter()
    end = None

    default_labels = []

    # Default status code used when the application does not return a valid response
    # or an unhandled exception occurs.
    status_code = 500


    async def wrapped_send(message: Message) -> None:
        if message["type"] == "http.response.start":
            nonlocal status_code
            status_code = message["status"]

        if message["type"] == "http.response.body":
            nonlocal end
            end = time.perf_counter()

        await send(message)

    try:
        await self.app(scope, receive, wrapped_send)
    finally:
        labels = [method, path, status_code, "starlette", *default_labels]
        # if we were not able to set end when the response body was written,
        # set it now.
        if end is None:
            end = time.perf_counter()

        self.gauges['http_request_count'].labels(*labels).inc()
        self.gauges['http_request_duration_seconds'].labels(*labels).set(end - begin)


  @staticmethod
  def _get_router_path(self, scope: Scope) -> Optional[str]:
    """Returns the original router path (with url param names) for given request."""
    if not (scope.get("endpoint", None) and scope.get("router", None)):
        return None

    root_path = scope.get("root_path", "")
    app = scope.get("app", {})

    if hasattr(app, "root_path"):
        app_root_path = getattr(app, "root_path")
        if root_path.startswith(app_root_path):
            root_path = root_path[len(app_root_path) :]

    base_scope = {
        "type": scope.get("type"),
        "path": root_path + scope.get("path"),
        "path_params": scope.get("path_params", {}),
        "method": scope.get("method"),
    }

    try:
        path = get_matching_route_path(base_scope, scope.get("router").routes)
        return path
    except:
        pass

    return None