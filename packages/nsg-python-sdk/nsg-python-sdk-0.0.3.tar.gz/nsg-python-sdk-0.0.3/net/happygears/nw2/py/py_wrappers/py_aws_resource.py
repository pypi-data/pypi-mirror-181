from net.happygears.proto.NSG_pb2 import Component
from .py_component import PyComponent


class PyAwsResource(PyComponent):
    def __init__(self, component: Component):
        super().__init__(component)

    @property
    def metric_definitions(self):
        return self.component.aws_metric_definitions

    @property
    def resource_definition(self):
        return self.component.aws_resource_definition
