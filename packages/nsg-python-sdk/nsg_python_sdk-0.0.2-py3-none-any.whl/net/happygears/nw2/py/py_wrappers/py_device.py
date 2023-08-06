import re

from net.happygears.nw2.py.py_wrappers.py_aws_resource import PyAwsResource
from net.happygears.nw2.py.py_wrappers.py_azure_resource import PyAzureResource
from net.happygears.nw2.py.py_wrappers.py_chassis_alarm import PyChassisAlarm
from net.happygears.nw2.py.py_wrappers.py_component import PyComponent
from net.happygears.nw2.py.py_wrappers.py_ipsec_tunnel import PyIpsecTunnel
from net.happygears.nw2.py.py_wrappers.py_mpls_tunnel import PyMplsTunnel
from net.happygears.nw2.py.py_wrappers.py_network_interface import PyNetworkInterface
from net.happygears.nw2.py.py_wrappers.py_protocol_descriptor import PyProtocolDescriptor
from net.happygears.proto.NSG_pb2 import Device
from .journaled_set import JournaledSet
from nsg import get_first_tag, get_all_tags_in_facet

class PyDevice:
    def __init__(self, node: Device):
        self.node = node
        self.tags = node.tags
        self.pyInterfaces = {intf.index: PyNetworkInterface(node, intf) for intf in node.interfaces.values()}
        self.pyMplsTunnels = None
        self.pyHardwareComponents = None
        self.pyProtocolDescriptors = None
        self.pyChassisAlarms = None
        self.pyFirewallCounters = None
        self.pyIpsecTunnels = None
        self.pyLbNodes = None
        self.pyServerPools = None
        self.pyVirtualServers = None
        self.pyEphemeralComponents = None
        self.pyAzureResources = None
        self.pyAwsResources = None
        self.pyVpnControlConnections = None

    @property
    def id(self):
        return self.node.ID

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node: Device):
        self._node = node

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = JournaledSet(tags)

    @property
    def interfaces(self):
        return self.pyInterfaces

    # @interfaces.setter
    # def interfaces(self, device):
    #     self.pyInterfaces = {intf.index: PyNetworkInterface(device, intf) for intf in device.interfaces.values()}

    def getPyInterfaces(self):
        return self.pyInterfaces.values()

    @property
    def boxdescr(self):
        return self.node.box_description

    @property
    def box_descr(self):
        return self.node.box_description

    @property
    def description(self):
        return self.node.sys_description

    @property
    def sys_descr(self):
        return self.node.sys_description

    @property
    def name(self):
        return self.node.name

    @property
    def device(self):
        return self.node.name

    @property
    def address(self):
        return self.node.address

    @property
    def deviceaddress(self):
        return self.node.address

    @property
    def sw_rev(self):
        return self.node.software_revision

    @property
    def sys_name(self):
        return self.node.system_name

    @property
    def contact(self):
        return self.node.sys_contact

    @property
    def location(self):
        return self.node.sys_location

    @property
    def reverse_dns(self):
        return self.node.reverse_DNS_name

    @property
    def ip_cidr_route_number_supported(self):
        return self.node.ip_CIDR_route_number_supported

    @property
    def inet_cidr_route_number_supported(self):
        return self.node.inet_CIDR_route_number_supported

    @property
    def ipv_6_route_number_supported(self):
        return self.node.ipv6_route_number_supported

    @property
    def product_name(self):
        return self.node.product_name

    @property
    def hostname(self):
        ipv4_only = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
        system_name = self.node.system_name
        return system_name if ipv4_only.match(system_name) else system_name.split(".")[0]

    def getNode(self):
        return self

    def getDelegate(self):
        return self.node

    def getId(self):
        return self.node.ID

    def getName(self):
        return self.node.name

    def getTags(self):
        return self.tags

    def getTagsInFacet(self, facet):
        return get_all_tags_in_facet(self, facet)

    def getFirstTag(self, facet):
        return get_first_tag(self.tags, facet)

    def forwardingClasses(self):
        return self.node.cos_fc_name.keys()

    def getQueueNum(self, fc_number):
        return self.node.cos_fc_queue_number.get(fc_number, None)

    def getFcName(self, fc_number):
        return self.node.cos_fc_name.get(fc_number, None)

    def getFcNumber(self, queue_number):
        for fcnum in self.node.cos_fc_queue_number.keys():
            if self.node.cos_fc_queue_number.get(fcnum, None) == queue_number:
                return fcnum
        return -1

    def getVmHostName(self):
        tags1 = self.getTagsInFacet('VmHost')
        if tags1 is None or len(tags1) == 0:
            return ''
        return next(iter(tags1)).split("\\.")[1]

    def getInterface(self, if_index):
        return self.pyInterfaces.get(if_index, None)

    def getPyHardwareComponents(self):
        if self.pyHardwareComponents is None:
            if not self.node.hardware_components:
                return []
            self.pyHardwareComponents = [PyComponent(comp) for comp in self.node.hardware_components]
        return self.pyHardwareComponents

    def getPyProtocolDescriptors(self):
        if self.pyProtocolDescriptors is None:
            if not self.node.protocol_descriptors:
                return []
            self.pyProtocolDescriptors = [PyProtocolDescriptor(protocol_desc) for protocol_desc in
                                          self.node.protocol_descriptors]
        return self.pyProtocolDescriptors

    def getPyChassisAlarms(self):
        if self.pyChassisAlarms is None:
            if not self.node.chassis_alarms:
                return []
            self.pyChassisAlarms = [PyChassisAlarm(chassis_alarm) for chassis_alarm in self.node.chassis_alarms]
        return self.pyChassisAlarms

    def getPyFwCounters(self):
        if self.pyFirewallCounters is None:
            if not self.node.firewall_counters:
                return []
            self.pyFirewallCounters = [PyComponent(firewall) for firewall in self.node.firewall_counters.values()]
        return self.pyFirewallCounters

    def getPyIpsecTunnels(self):
        if self.pyIpsecTunnels is None:
            if not self.node.ipsec_tunnels:
                return []
            self.pyIpsecTunnels = [PyIpsecTunnel(tunnel) for tunnel in self.node.ipsec_tunnels.values()]
        return self.pyIpsecTunnels

    def getPyLbNodes(self):
        if self.pyLbNodes is None:
            if not self.node.load_balancers:
                return []
            self.pyLbNodes = [PyComponent(load_balancer) for load_balancer in self.node.load_balancers.values()]
        return self.pyLbNodes

    def getPyServerPools(self):
        if self.pyServerPools is None:
            if not self.node.server_pools:
                return []
            self.pyServerPools = [PyComponent(server) for server in self.node.server_pools.values()]
        return self.pyServerPools

    def getPyVirtualServers(self):
        if self.pyVirtualServers is None:
            if not self.node.virtual_servers:
                return []
            self.pyVirtualServers = [PyComponent(server) for server in self.node.virtual_servers.values()]
        return self.pyVirtualServers

    def getPyEphemeralComponents(self):
        if self.pyEphemeralComponents is None:
            if not self.node.ephemeral_components:
                return []
            self.pyEphemeralComponents = [PyComponent(component) for component in self.node.ephemeral_components]
        return self.pyEphemeralComponents

    def getPyAzureResources(self):
        if self.pyAzureResources is None:
            if not self.node.azure_resources:
                return []
            self.pyAzureResources = [PyAzureResource(component) for component in self.node.azure_resources.values()]
        return self.pyAzureResources

    def getPyAwsResources(self):
        if self.pyAwsResources is None:
            if not self.node.aws_resources:
                return []
            self.pyAwsResources = [PyAwsResource(component) for component in self.node.aws_resources.values()]
        return self.pyAwsResources

    def getPyVpnControlConnections(self):
        if self.pyVpnControlConnections is None:
            if not self.node.vpn_control_connections:
                return []
            self.pyVpnControlConnections = [PyComponent(component) for component in
                                            self.node.vpn_control_connections.values()]
        return self.pyVpnControlConnections

    def getPyMplsTunnels(self):
        return self.getMplsTunnels().values()

    def getMplsTunnels(self):
        if self.pyMplsTunnels is None:
            self.pyMplsTunnels = {tunnel.index: PyMplsTunnel(tunnel) for tunnel in self.node.MPLS_tunnels.values()}
        return self.pyMplsTunnels

    def isSupported(self, handle):
        res = self.node.OID_support.get(handle, False)

        if res:
            return True

        return self.node.OID_support.get(handle.replace(':', ' : '), False)

    def getIsIsCircuitLevel(self, circ):
        if not circ in self.node.ISIS_circuit_if_index:
            return -1
        if circ in self.node.ISIS_circuit_level1_metric:
            return 1
        if circ in self.node.ISIS_circuit_level2_metric:
            return 2
        return -1

    def getOspfAdminStatus(self):
        return self.node.OSPF_admin_status
