from net.happygears.proto.NSG_pb2 import Component
from .py_component import PyComponent


class PyProtocolDescriptor(PyComponent):
    def __init__(self, protocolDescriptor: Component):
        super().__init__(protocolDescriptor)

    @property
    def protocol(self):
        return self.component.protocol.name