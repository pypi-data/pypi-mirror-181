from net.happygears.proto.NSG_pb2 import Device
from net.happygears.proto.NSG_pb2 import Interface
from net.happygears.nw2.py.monitoring_data_type import MonitoringDataType
from .journaled_set import JournaledSet
from nsg import get_all_tags_in_facet, get_first_tag


class PyNetworkInterface:
    def __init__(self, node: Device, intf: Interface):
        self.node = node
        self.intf = intf
        self.tags = intf.tags

    @property
    def name(self):
        return self.intf.name

    @property
    def description(self):
        return self.intf.alias

    @property
    def addresses(self):
        return list(self.intf.addresses)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = JournaledSet(tags)

    @property
    def address(self):
        if not self.intf.addresses:
            return None
        else:
            return self.intf.addresses[0]

    @property
    def index(self):
        return self.intf.index

    @property
    def if_index(self):
        return self.intf.index

    @property
    def if_speed(self):
        return self.intf.speed

    @property
    def if_high_speed(self):
        return self.intf.high_speed

    @property
    def isis_circuit(self):
        return self.get_isis_circuit()

    @property
    def cos_queues(self):
        return self.intf.cos_queues

    @property
    def sensor_scale(self):
        return 1.0

    @property
    def data_type(self):
        return MonitoringDataType.Unknown

    def get_isis_circuit(self):
        for k, v in self.node.ISIS_circuit_if_index.items():
            if v == self.intf.idex:
                return k
        return -1

    def getIntf(self):
        return self.intf

    def getTagsInFacet(self, facet):
        return get_all_tags_in_facet(self, facet)

    def getFirstTag(self, facet):
        return get_first_tag(self.tags, facet)
