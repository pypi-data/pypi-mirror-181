from net.happygears.proto.NSG_pb2 import Component
from net.happygears.nw2.py.monitoring_data_type import MonitoringDataType
from net.happygears.nw2.py.py_wrappers.hardware_component_class import HardwareComponentClass
from net.happygears.nw2.py.sensor_data_type import SensorDataType
from .journaled_set import JournaledSet
from nsg import get_first_tag, get_all_tags_in_facet

class PyComponent:
    def __init__(self, component: Component):
        self.component = component
        self.tags = component

    @property
    def name(self):
        return self.component.name

    @property
    def index(self):
        return self.component.index

    @property
    def description(self):
        return self.component.description

    @property
    def model(self):
        return self.component.model_name

    @property
    def oid(self):
        return self.component.OID

    @property
    def sensor_scale(self):
        return self.component.sensor_data_scale

    @property
    def sensor_data_type(self):
        return SensorDataType.reverse(self.component.sensor_data_type).name

    @property
    def component_class(self):
        return HardwareComponentClass.reverse(self.component.component_class).name

    @property
    def var_hint(self):
        return self.component.monitoring_variable_hint

    @property
    def data_type(self):
        return MonitoringDataType.reverse(self.component.data_type)

    @property
    def encoded_oid_subindex(self):
        return self.component.encoded_OID_subindex

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, component):
        self._tags = JournaledSet(component.tags)

    def getComponent(self):
        return self.component

    def getIndex(self):
        return self.component.index

    def getName(self):
        return self.component.name

    def getTags(self):
        return self.tags

    def getTagsInFacet(self, facet):
        return get_all_tags_in_facet(self, facet)

    def getFirstTag(self, facet):
        return get_first_tag(self.tags, facet)