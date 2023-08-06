from starlette.applications import Starlette
from svc_monitor import SVCMonitor

# Builds a prometheus monitor class using the generic service monitor class w type = prometheus
# generates a bunch of default python metrics from prometheus clint
# generates request metrics using middleware that tracks request count + time (refresh the page to see more pop up)
# Tests adding / getting metric of each type + getting a metric of each type that doesnt exist (makes a new one)
# Tests interfacing with metrics by incrementing a counter that was made above (result shown below for that counter, not the others)

# still needs requirements, init, setup etc.

# run locally with 'uvicorn test:app' to expose metrics at 127.0.0.1:8000/metrics

test_monitor = SVCMonitor('test', 'prometheus', 'very_cool_service')

test_monitor.create(test_monitor._name, test_monitor._metricType, test_monitor._serviceName)

test_monitor.monitors[test_monitor._name].addGauge(
    'test_gauge', 
      (
        'method',
        'path',
        'status',
      ),
      'test_gauge'
)
test_monitor.monitors[test_monitor._name].addCounter(
    'test_counter', 
      (
        'method',
        'path',
        'status',
      ),
      'test_counter'
)
test_monitor.monitors[test_monitor._name].addHistogram(
    'test_histogram', 
      (
        'method',
        'path',
        'status',
      ),
      'test_histogram'
)
test_monitor.monitors[test_monitor._name].addSummary(
    'test_summary', 
      (
        'method',
        'path',
        'status',
      ),
      'test_summary'
)

test_get_gauge = test_monitor.monitors[test_monitor._name].getGauge('test_gauge')
print(test_get_gauge)
test_get_counter = test_monitor.monitors[test_monitor._name].getCounter('test_counter')
print(test_get_counter)
test_get_histogram = test_monitor.monitors[test_monitor._name].getHistogram('test_histogram')
print(test_get_histogram)
test_get_summary = test_monitor.monitors[test_monitor._name].getSummary('test_summary')
print(test_get_summary)

test_get_new_gauge = test_monitor.monitors[test_monitor._name].getGauge(
    'test_new_gauge', 
    {
        'name': 'test_new_gauge',
        'labels': (
            'method',
            'path',
            'status',
        ),
        'help': 'test get monitor that doesnt exist'
    }
)
print(test_get_new_gauge)

test_get_new_counter = test_monitor.monitors[test_monitor._name].getCounter(
    'test_new_counter', 
    {
        'name': 'test_new_counter',
        'labels': (
            'method',
            'path',
            'status',
        ),
        'help': 'test get monitor that doesnt exist'
    }
)
print(test_get_new_counter)

test_get_new_histogram = test_monitor.monitors[test_monitor._name].getHistogram(
    'test_new_histogram', 
    {
        'name': 'test_new_histogram',
        'labels': (
            'method',
            'path',
            'status',
        ),
        'help': 'test get monitor that doesnt exist'
    }
)
print(test_get_new_histogram)

test_get_new_summary = test_monitor.monitors[test_monitor._name].getSummary(
    'test_new_summary', 
    {
        'name': 'test_new_summary',
        'labels': (
            'method',
            'path',
            'status',
        ),
        'help': 'test get monitor that doesnt exist'
    }
)
print(test_get_new_summary)

test_get_new_counter.labels("test_method", "test_path", "test_status").inc()

app = Starlette()
test_monitor.monitors[test_monitor._name].start_app(app)
