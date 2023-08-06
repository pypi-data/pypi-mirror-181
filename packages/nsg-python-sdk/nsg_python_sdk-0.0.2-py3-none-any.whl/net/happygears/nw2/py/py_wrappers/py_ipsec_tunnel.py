from net.happygears.proto.NSG_pb2 import Component
from .py_component import PyComponent

class PyIpsecTunnel(PyComponent):
    def __init__(self, tunnel: Component):
        super().__init__(tunnel)

    @property
    def if_index(self):
        return self.component.tunnel_index

    @property
    def in_traffic_oid_index(self):
        return self.component.in_traffic_OID_index

    @property
    def out_traffic_oid_index(self):
        return self.component.out_traffic_OID_index

    @property
    def oper_status_oid_index(self):
        return self.component.operational_status_OID_index