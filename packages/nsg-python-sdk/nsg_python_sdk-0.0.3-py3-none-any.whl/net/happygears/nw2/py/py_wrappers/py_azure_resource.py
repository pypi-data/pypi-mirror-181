from .py_component import PyComponent
from net.happygears.proto.NSG_pb2 import Component

class PyAzureResource(PyComponent):
    def __init__(self, component:Component):
        super().__init__(component)

    @property
    def metric_definitions(self):
        return self.component.azure_metric_definitions

    @property
    def resource_definition(self):
        return self.component.azure_resource_definition