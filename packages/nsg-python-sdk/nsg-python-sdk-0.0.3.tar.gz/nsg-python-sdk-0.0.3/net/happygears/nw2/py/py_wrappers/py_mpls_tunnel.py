from net.happygears.proto.NSG_pb2 import Component
from . import PyComponent


class PyMplsTunnel(PyComponent):
    def __init__(self, tunnel):
        super().__init__(tunnel)

    @property
    def is_if(self):
        return self.component.tunnel_is_interface

    @property
    def if_index(self):
        return self.component.tunnel_index

    @property
    def encoded_oid_subindex(self):
        return self.component.encoded_OID_subindex
