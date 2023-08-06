class SVCMonitor:

  validTypes = ['prometheus']
  monitors = {}
  _name = None
  _metricType = None
  _serviceName = None


  def __init__(self, name, metricType, serviceName):
    self._name = name
    self._metricType = metricType
    self._serviceName = serviceName


  def validateParams(self, name, metricType, serviceName):
    if (
      type(name) != str or
      type(metricType) != str or
      metricType not in self.validTypes or
      type(serviceName) != str
      ):
      raise Exception('Monitor creation parameters are not valid.')
    return True


  def create(self, name, metricType, serviceName):
    from svc_monitor_prom import SVCMonitorPrometheus 
    self.validateParams(name, metricType, serviceName)
    # I'd want to make this a match case to be more generic, but assuming we are using same py version as analytics
    if (metricType == 'prometheus'):
      self.monitors[name] = SVCMonitorPrometheus(name, metricType, serviceName)
    else:
      raise Exception('Unsupported metric type') # This is caught by validation, but mirroring npm logic
    
    monitor = self.monitors[name]

    return monitor


  def getInstance(self, monitorName):
    return self.monitors.get(monitorName, None)


  def destroyMonitor(self, monitorName):
    self.monitors.pop(monitorName, None)