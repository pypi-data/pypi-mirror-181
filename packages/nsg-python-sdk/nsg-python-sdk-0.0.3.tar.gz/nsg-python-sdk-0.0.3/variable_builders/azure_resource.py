"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py import MonitoringDataType
from net.happygears.nw2.py.py_wrappers import PyAzureResource
from net.happygears.nw2.py.py_wrappers import PyDevice
from variable_builders.hardware_component import HWComponentVariableBuilder

VMSS_VIRTUAL_MACHINES_NS = "Microsoft.Compute/virtualMachineScaleSets/virtualMachines"

VIRTUAL_MACHINES_NS = "Microsoft.Compute/virtualMachines"
VIRTUAL_NETWORKS_NS = "Microsoft.Network/virtualNetworks"
NETWORK_INTERFACES_NS = "Microsoft.Network/networkInterfaces"
DISKS_NS = "Microsoft.Compute/disks"
LB_NS = "Microsoft.Network/loadBalancers"

METRIC_VARS = {
    # disks
    ("%s/Composite Disk Read Bytes/sec" % DISKS_NS):                                "diskIOBytesReadRate",
    ("%s/Composite Disk Read Operations/sec" % DISKS_NS):                           "diskIOReadsRate",
    ("%s/Composite Disk Write Bytes/sec" % DISKS_NS):                               "diskIOBytesWritesRate",
    ("%s/Composite Disk Write Operations/sec" % DISKS_NS):                          "diskIOWritesRate",
    ("%s/DiskPaidBurstIOPS" % DISKS_NS):                                            "diskIOPSPaidBurst",
    # nic
    ("%s/BytesSentRate" % NETWORK_INTERFACES_NS):                                   "ifOutRate",
    ("%s/BytesReceivedRate" % NETWORK_INTERFACES_NS):                               "ifInRate",
    ("%s/PacketsSentRate" % NETWORK_INTERFACES_NS):                                 "ifOutUcastPktsRate",
    ("%s/PacketsReceivedRate" % NETWORK_INTERFACES_NS):                             "ifInUcastPktsRate",
    # vnet
    ("%s/PacketsInDDoS" % VIRTUAL_NETWORKS_NS):                                     "ddosPacketsIn",
    ("%s/PacketsDroppedDDoS" % VIRTUAL_NETWORKS_NS):                                "ddosPacketsDropped",
    ("%s/PacketsForwardedDDoS" % VIRTUAL_NETWORKS_NS):                              "ddosPacketsForwarded",
    ("%s/TCPPacketsInDDoS" % VIRTUAL_NETWORKS_NS):                                  "ddosPacketsTcpIn",
    ("%s/TCPPacketsDroppedDDoS" % VIRTUAL_NETWORKS_NS):                             "ddosPacketsTcpDropped",
    ("%s/TCPPacketsForwardedDDoS" % VIRTUAL_NETWORKS_NS):                           "ddosPacketsTcpForwarded",
    ("%s/UDPPacketsInDDoS" % VIRTUAL_NETWORKS_NS):                                  "ddosPacketsUdpIn",
    ("%s/UDPPacketsDroppedDDoS" % VIRTUAL_NETWORKS_NS):                             "ddosPacketsUdpDropped",
    ("%s/UDPPacketsForwardedDDoS" % VIRTUAL_NETWORKS_NS):                           "ddosPacketsUdpForwarded",
    ("%s/BytesInDDoS" % VIRTUAL_NETWORKS_NS):                                       "ddosBytesIn",
    ("%s/BytesDroppedDDoS" % VIRTUAL_NETWORKS_NS):                                  "ddosBytesDropped",
    ("%s/BytesForwardedDDoS" % VIRTUAL_NETWORKS_NS):                                "ddosBytesForwarded",
    ("%s/TCPBytesInDDoS" % VIRTUAL_NETWORKS_NS):                                    "ddosBytesTcpIn",
    ("%s/TCPBytesDroppedDDoS" % VIRTUAL_NETWORKS_NS):                               "ddosBytesTcpDropped",
    ("%s/TCPBytesForwardedDDoS" % VIRTUAL_NETWORKS_NS):                             "ddosBytesTcpForwarded",
    ("%s/UDPBytesInDDoS" % VIRTUAL_NETWORKS_NS):                                    "ddosBytesUdpIn",
    ("%s/UDPBytesDroppedDDoS" % VIRTUAL_NETWORKS_NS):                               "ddosBytesUdpDropped",
    ("%s/UDPBytesForwardedDDoS" % VIRTUAL_NETWORKS_NS):                             "ddosBytesUdpForwarded",
    ("%s/IfUnderDDoSAttack" % VIRTUAL_NETWORKS_NS):                                 "ddosActive",
    ("%s/DDoSTriggerTCPPackets" % VIRTUAL_NETWORKS_NS):                             "ddosTriggerTcpPackets",
    ("%s/DDoSTriggerUDPPackets" % VIRTUAL_NETWORKS_NS):                             "ddosTriggerUdpPackets",
    ("%s/DDoSTriggerSYNPackets" % VIRTUAL_NETWORKS_NS):                             "ddosTriggerSynPackets",
    # vm
    ("%s/Percentage CPU" % VIRTUAL_MACHINES_NS):                                    "cpuUtil",
    ("%s/CPU Credits Remaining" % VIRTUAL_MACHINES_NS):                             "cpuCreditsRemaining",
    ("%s/CPU Credits Consumed" % VIRTUAL_MACHINES_NS):                              "cpuCreditsConsumed",
    ("%s/Available Memory Bytes" % VIRTUAL_MACHINES_NS):                            "memAvail",
    ("%s/Disk Read Operations/Sec" % VIRTUAL_MACHINES_NS):                          "diskIOReadsRate",
    ("%s/Disk Write Operations/Sec" % VIRTUAL_MACHINES_NS):                         "diskIOWritesRate",
    ("%s/Data Disk Read Bytes/sec" % VIRTUAL_MACHINES_NS):                          "dataDiskIOBytesReadRate",
    ("%s/Data Disk Write Bytes/sec" % VIRTUAL_MACHINES_NS):                         "dataDiskIOBytesWriteRate",
    ("%s/Data Disk Read Operations/Sec" % VIRTUAL_MACHINES_NS):                     "dataDiskIOReadsOpRate",
    ("%s/Data Disk Write Operations/Sec" % VIRTUAL_MACHINES_NS):                    "dataDiskIOWritesOpRate",
    ("%s/Data Disk Queue Depth" % VIRTUAL_MACHINES_NS):                             "dataDiskQueueDepth",
    ("%s/Data Disk Bandwidth Consumed Percentage" % VIRTUAL_MACHINES_NS):           "dataDiskBandwidthConsumeRate",
    ("%s/Data Disk IOPS Consumed Percentage" % VIRTUAL_MACHINES_NS):                "dataDiskIOPSConsumeRate",
    ("%s/Data Disk Target Bandwidth" % VIRTUAL_MACHINES_NS):                        "dataDiskTargetBandwidth",
    ("%s/Data Disk Target IOPS" % VIRTUAL_MACHINES_NS):                             "dataDiskTargetIOPS",
    ("%s/Data Disk Max Burst Bandwidth" % VIRTUAL_MACHINES_NS):                     "dataDiskMaxBurstBandwidth",
    ("%s/Data Disk Max Burst IOPS" % VIRTUAL_MACHINES_NS):                          "dataDiskMaxBurstIOPS",
    ("%s/Data Disk Used Burst BPS Credits Percentage" % VIRTUAL_MACHINES_NS):       "diskUsedBPSCredits",
    ("%s/Data Disk Used Burst IO Credits Percentage" % VIRTUAL_MACHINES_NS):        "diskUsedIOCredits",
    ("%s/OS Disk Read Bytes/sec" % VIRTUAL_MACHINES_NS):                            "osDiskIOBytesReadRate",
    ("%s/OS Disk Write Bytes/sec" % VIRTUAL_MACHINES_NS):                           "osDiskIOBytesWriteRate",
    ("%s/OS Disk Read Operations/Sec" % VIRTUAL_MACHINES_NS):                       "osDiskIOReadsOpRate",
    ("%s/OS Disk Write Operations/Sec" % VIRTUAL_MACHINES_NS):                      "osDiskIOWritesOpRate",
    ("%s/OS Disk Queue Depth" % VIRTUAL_MACHINES_NS):                               "osDiskQueueDepth",
    ("%s/OS Disk Bandwidth Consumed Percentage" % VIRTUAL_MACHINES_NS):             "osDiskBandwidthConsumeRate",
    ("%s/OS Disk IOPS Consumed Percentage" % VIRTUAL_MACHINES_NS):                  "osDiskIOPSConsumeRate",
    ("%s/OS Disk Target Bandwidth" % VIRTUAL_MACHINES_NS):                          "osDiskTargetBandwidth",
    ("%s/OS Disk Target IOPS" % VIRTUAL_MACHINES_NS):                               "osDiskTargetIOPS",
    ("%s/OS Disk Max Burst Bandwidth" % VIRTUAL_MACHINES_NS):                       "osDiskMaxBurstBandwidth",
    ("%s/OS Disk Max Burst IOPS" % VIRTUAL_MACHINES_NS):                            "osDiskMaxBurstIOPS",
    ("%s/OS Disk Used Burst BPS Credits Percentage" % VIRTUAL_MACHINES_NS):         "osUsedBPSCredits",
    ("%s/OS Disk Used Burst IO Credits Percentage" % VIRTUAL_MACHINES_NS):          "osUsedIOCredits",
    ("%s/Inbound Flows" % VIRTUAL_MACHINES_NS):                                     "inboundFlows",
    ("%s/Outbound Flows" % VIRTUAL_MACHINES_NS):                                    "outboundFlows",
    ("%s/Inbound Flows Maximum Creation Rate" % VIRTUAL_MACHINES_NS):               "maxInFlowRate",
    ("%s/Outbound Flows Maximum Creation Rate" % VIRTUAL_MACHINES_NS):              "maxOutFlowsRate",
    ("%s/Premium Data Disk Cache Read Hit" % VIRTUAL_MACHINES_NS):                  "diskCacheReadHits",
    ("%s/Premium Data Disk Cache Read Miss" % VIRTUAL_MACHINES_NS):                 "diskCacheReadMisses",
    ("%s/Premium OS Disk Cache Read Hit" % VIRTUAL_MACHINES_NS):                    "premiumOsDiskCacheReadHits",
    ("%s/Premium OS Disk Cache Read Miss" % VIRTUAL_MACHINES_NS):                   "premiumOsDiskCacheReadMisses",
    ("%s/VM Cached Bandwidth Consumed Percentage" % VIRTUAL_MACHINES_NS):           "diskCacheBandwidth",
    ("%s/VM Cached IOPS Consumed Percentage" % VIRTUAL_MACHINES_NS):                "diskCachedIOPS",
    ("%s/VM Uncached Bandwidth Consumed Percentage" % VIRTUAL_MACHINES_NS):         "diskUncachedBandwidth",
    ("%s/VM Uncached IOPS Consumed Percentage" % VIRTUAL_MACHINES_NS):              "diskUncachedIOS",
    ("%s/Network In Total" % VIRTUAL_MACHINES_NS):                                  "ifInRate",
    ("%s/Network Out Total" % VIRTUAL_MACHINES_NS):                                 "ifOutRate",
    # vmss vm
    ("%s/Percentage CPU" % VMSS_VIRTUAL_MACHINES_NS):                               "cpuUtil",
    ("%s/CPU Credits Remaining" % VMSS_VIRTUAL_MACHINES_NS):                        "cpuCreditsRemaining",
    ("%s/CPU Credits Consumed" % VMSS_VIRTUAL_MACHINES_NS):                         "cpuCreditsConsumed",
    ("%s/Available Memory Bytes" % VMSS_VIRTUAL_MACHINES_NS):                       "memAvail",
    ("%s/Disk Read Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):                     "diskIOReadsRate",
    ("%s/Disk Write Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):                    "diskIOWritesRate",
    ("%s/Data Disk Read Bytes/sec" % VMSS_VIRTUAL_MACHINES_NS):                     "dataDiskIOBytesReadRate",
    ("%s/Data Disk Write Bytes/sec" % VMSS_VIRTUAL_MACHINES_NS):                    "dataDiskIOBytesWriteRate",
    ("%s/Data Disk Read Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):                "dataDiskIOReadsOpRate",
    ("%s/Data Disk Write Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):               "dataDiskIOWritesOpRate",
    ("%s/Data Disk Queue Depth" % VMSS_VIRTUAL_MACHINES_NS):                        "dataDiskQueueDepth",
    ("%s/Data Disk Bandwidth Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):      "dataDiskBandwidthConsumeRate",
    ("%s/Data Disk IOPS Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):           "dataDiskIOPSConsumeRate",
    ("%s/Data Disk Target Bandwidth" % VMSS_VIRTUAL_MACHINES_NS):                   "dataDiskTargetBandwidth",
    ("%s/Data Disk Target IOPS" % VMSS_VIRTUAL_MACHINES_NS):                        "dataDiskTargetIOPS",
    ("%s/Data Disk Max Burst Bandwidth" % VMSS_VIRTUAL_MACHINES_NS):                "dataDiskMaxBurstBandwidth",
    ("%s/Data Disk Max Burst IOPS" % VMSS_VIRTUAL_MACHINES_NS):                     "dataDiskMaxBurstIOPS",
    ("%s/Data Disk Used Burst BPS Credits Percentage" % VMSS_VIRTUAL_MACHINES_NS):  "diskUsedBPSCredits",
    ("%s/Data Disk Used Burst IO Credits Percentage" % VMSS_VIRTUAL_MACHINES_NS):   "diskUsedIOCredits",
    ("%s/OS Disk Read Bytes/sec" % VMSS_VIRTUAL_MACHINES_NS):                       "osDiskIOBytesReadRate",
    ("%s/OS Disk Write Bytes/sec" % VMSS_VIRTUAL_MACHINES_NS):                      "osDiskIOBytesWriteRate",
    ("%s/OS Disk Read Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):                  "osDiskIOReadsOpRate",
    ("%s/OS Disk Write Operations/Sec" % VMSS_VIRTUAL_MACHINES_NS):                 "osDiskIOWritesOpRate",
    ("%s/OS Disk Queue Depth" % VMSS_VIRTUAL_MACHINES_NS):                          "osDiskQueueDepth",
    ("%s/OS Disk Bandwidth Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):        "osDiskBandwidthConsumeRate",
    ("%s/OS Disk IOPS Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):             "osDiskIOPSConsumeRate",
    ("%s/OS Disk Target Bandwidth" % VMSS_VIRTUAL_MACHINES_NS):                     "osDiskTargetBandwidth",
    ("%s/OS Disk Target IOPS" % VMSS_VIRTUAL_MACHINES_NS):                          "osDiskTargetIOPS",
    ("%s/OS Disk Max Burst Bandwidth" % VMSS_VIRTUAL_MACHINES_NS):                  "osDiskMaxBurstBandwidth",
    ("%s/OS Disk Max Burst IOPS" % VMSS_VIRTUAL_MACHINES_NS):                       "osDiskMaxBurstIOPS",
    ("%s/OS Disk Used Burst BPS Credits Percentage" % VMSS_VIRTUAL_MACHINES_NS):    "osUsedBPSCredits",
    ("%s/OS Disk Used Burst IO Credits Percentage" % VMSS_VIRTUAL_MACHINES_NS):     "osUsedIOCredits",
    ("%s/Inbound Flows" % VMSS_VIRTUAL_MACHINES_NS):                                "inboundFlows",
    ("%s/Outbound Flows" % VMSS_VIRTUAL_MACHINES_NS):                               "outboundFlows",
    ("%s/Inbound Flows Maximum Creation Rate" % VMSS_VIRTUAL_MACHINES_NS):          "maxInFlowRate",
    ("%s/Outbound Flows Maximum Creation Rate" % VMSS_VIRTUAL_MACHINES_NS):         "maxOutFlowsRate",
    ("%s/Premium Data Disk Cache Read Hit" % VMSS_VIRTUAL_MACHINES_NS):             "diskCacheReadHits",
    ("%s/Premium Data Disk Cache Read Miss" % VMSS_VIRTUAL_MACHINES_NS):            "diskCacheReadMisses",
    ("%s/Premium OS Disk Cache Read Hit" % VMSS_VIRTUAL_MACHINES_NS):               "premiumOsDiskCacheReadHits",
    ("%s/Premium OS Disk Cache Read Miss" % VMSS_VIRTUAL_MACHINES_NS):              "premiumOsDiskCacheReadMisses",
    ("%s/VM Cached Bandwidth Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):      "diskCacheBandwidth",
    ("%s/VM Cached IOPS Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):           "diskCachedIOPS",
    ("%s/VM Uncached Bandwidth Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):    "diskUncachedBandwidth",
    ("%s/VM Uncached IOPS Consumed Percentage" % VMSS_VIRTUAL_MACHINES_NS):         "diskUncachedIOS",
    ("%s/Network In Total" % VMSS_VIRTUAL_MACHINES_NS):                             "ifInRate",
    ("%s/Network Out Total" % VMSS_VIRTUAL_MACHINES_NS):                            "ifOutRate",
    # lb
    # Average Load Balancer data path availability per time duration
    ("%s/VipAvailability" % LB_NS):                                                 "lbVipAvailability",
    # Average Load Balancer health probe status per time duration
    ("%s/DipAvailability" % LB_NS):                                                 "lbDipAvailability",
    # Total number of Bytes transmitted within time period
    ("%s/ByteCount" % LB_NS):                                                       "lbBytesRate",
    # Total number of Packets transmitted within time period
    ("%s/PacketCount" % LB_NS):                                                     "lbPacketsRate",
    # Total number of SYN Packets transmitted within time period
    ("%s/SYNCount" % LB_NS):                                                        "lbSynRate",
    # Total number of new SNAT connections created within time period
    ("%s/SnatConnectionCount" % LB_NS):                                             "lbSnatConnectionsCreatedRate",
    # Total number of SNAT ports allocated within time period
    ("%s/AllocatedSnatPorts" % LB_NS):                                              "lbSnatPortsAllocatedRate",
    # Total number of SNAT ports used within time period
    ("%s/UsedSnatPorts" % LB_NS):                                                   "lbSnatPortsUsedRate",
}


class AzureResourceVariableBuilder(HWComponentVariableBuilder):

    def __init__(self, log):
        super(AzureResourceVariableBuilder, self).__init__(log)

    def make_azure_resource_variables(self, device, component):
        """
        Make monitoring variables for the azure resource

        :type device:    PyDevice
        :param device:   network device object
        :type component:      PyAzureResource
        :param component:     AzureResourceMetrics object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        mvars = {}

        index = component.getComponent().index
        metric_definitions = component.metric_definitions
        for metric_name in metric_definitions:
            metric_namespace = metric_definitions[metric_name].namespace
            var_name_key = metric_namespace + "/" + metric_name
            if var_name_key in list(METRIC_VARS.keys()):
                var_name = METRIC_VARS[var_name_key]
                mvars[var_name] = {
                    'index': index,
                    'component': component,
                    'metric_name': metric_name,
                    'type': MonitoringDataType.Double
                }

        return mvars

    def make_variables(self, device, component):
        """
        Given device and h/w component objects, build set of monitoring variables
        for the component

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     PyVirtualServer or PyServerPool object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        if isinstance(component, PyAzureResource):
            return self.make_azure_resource_variables(device, component)
        else:
            return {}

