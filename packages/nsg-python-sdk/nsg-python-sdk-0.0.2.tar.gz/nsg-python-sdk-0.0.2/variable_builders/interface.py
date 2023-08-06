"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""
import re

import ipaddr
from net.happygears.nw2.py.monitoring_data_type import MonitoringDataType
from net.happygears.nw2.py.py_wrappers.py_device import PyDevice
from net.happygears.nw2.py.py_wrappers.py_network_interface import PyNetworkInterface
from variable_builders.base_variable_builder import BaseVariableBuilder

OSPF_ADMIN_STATUS_ENABLE = 1
OSPF_ADMIN_STATUS_DISABLE = 2

# list of interface names for which we should always use ifHighSpeed
ALWAYS_HIGH_SPEED = ['ae', 'xe', 'et']
# couple of letters, followed by a digit or '-' or '.'
INTERFACE_TYPE_RE_1 = re.compile(r'([a-zA-Z]+)[\d\-.]')
# port-channelNNN or Port-ChannelNN (capitalization depends on the vendor)
INTERFACE_TYPE_RE_2 = re.compile(r'([pP]ort-[cC]hannel)\d+')


def is_always_high_speed(intf_name):
    """
    Use simple heuristics to determine when we should use ifHighSpeed to poll
    for interface speed even if it seemed to not respond during discovery

    NET-2697
    NSGHELP-156
    NSGHELP-414 (and NET-3682)

    :param intf_name:   interface name
    :return:            True if ifHighSpeed should be used
    """
    m = INTERFACE_TYPE_RE_2.match(intf_name)
    if m:
        return True
    m = INTERFACE_TYPE_RE_1.match(intf_name)
    if m:
        return m.group(1) in ALWAYS_HIGH_SPEED
    return False


def is_always_32_bit_interface_counters(device):
    """
    NET-3772

    Juniper PulseSecure does not support 64-bit counters
    """
    return 'Vendor.JuniperPulseSecure' in device.tags


class InterfaceVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build interface-related monitoring variables.
    We create an object of this class and call its method `make_variable()`
    for all fixtures and all interfaces. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variable()` in it.
    """

    def __init__(self, log):
        super(InterfaceVariableBuilder, self).__init__(log)
        self.make_interface_packet_counter_vars = False
        self.make_interface_duplex_status_vars = False

    def is_connected_interface(self, intf):
        """
        Check if given interface is connected anywhere.

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        """
        return any('Link.' in x for x in intf.tags)  # There is at least one tag in facet 'Link.' with any word

    def is_aggregation_port(self, intf):
        """
        Aggregation ports have tag 'ifRole.AggregationPort'.

        Note that aggregation ports on Juniper are actually .0 subinterfaces. This
        function includes those and is used to decide whether we should monitor
        LACP state.

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this is an aggregation port
        """
        return 'ifRole.AggregationPort' in intf.tags

    def is_physical_port(self, intf):
        """
        Physical ports have tag 'ifRole.PhysicalPort'

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this is a physical port
        """
        return 'ifRole.PhysicalPort' in intf.tags

    def is_peering_interface(self, intf):
        """
        Peering interfaces have tag 'ifRole.PeeringInterface'.

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this is an aggregation port
        """
        return 'ifRole.PeeringInterface' in intf.tags

    def is_juniper_parent_of_aggregation_port(self, intf):
        """
        Aggregation ports have tag 'ifRole.AggregationPort'. Special case:
        on Juniper aggregation ports are subinterfaces. Neither these, nor
        their parent physical interfaces appear connected anywhere (because
        it is corresponding bundle interface "ae*" that is connected). This
        means function is_connected_interface() does not match them. If you
        want to monitor traffic, errors, COS drops etc on their parent
        physical interfaces, you can identify those by searching for the tag
        'ifRole.ParentOfAggregationPort'

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this is a parent of an aggregation port
        """
        return 'ifRole.ParentOfAggregationPort' in intf.tags

    def is_simulated_ipsec_tunnel_interface(self, device, intf):
        """
        We create simulated interfaces that represent endpoints of IPSEC tunnels
        on Cisco fixtures (ASA)

        Simulated interfaces created to represent IPSEC tunnel endpoints
        are not "real" and don't respond to RFC1213 OIDs. Monitoring
        variables used to collect utilization data for these tunnels
        are generated in class IpsecTunnelVariableBuilder

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this is a simulated tunnel interface on Cisco device
        """
        pass
        return 'ifRole.SimulatedTunnelEndPointInterface' in intf.tags

    def is_interesting_aggregation_port(self, intf):
        """
        Decides if this is an aggregation port we should monitor. There are
        several possible scenarios:

         - on Juniper aggregation ports are actually .0 subinterfaces but we want to
           monitor corresponding parent physical interfaces. We can identify these
           interfaces by matching tag ifRole.ParentOfAggregationPort. These interfaces
           also have tag ifRole.PhysicalPort
         - on Cisco, Arista and other platforms (not Juniper) there are no .0
           subinterfaces and any interface with tag ifRole.AggregationPort should
           be monitored. These ports also have tag ifRole.PhysicalPort

        Logical expression should exclude Juniper .0 subinterfaces that have tag
        ifRole.AggregationPort. This works because these interfaces do not have tag
        ifRole.PhysicalPort

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True of this interface should be monitored
        """
        return self.is_juniper_parent_of_aggregation_port(intf) or (
                self.is_physical_port(intf) and self.is_aggregation_port(intf))

    def is_interesting_interface(self, intf):
        """
        This function implements some basic checks to decide if we want to monitor this interface

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return:  True if we want to monitor this interface
        """
        return ('ifAdminStatus.Up' in intf.tags and
                'ifRole.LoopbackInterface' not in intf.tags and
                'ifRole.OutOfBandManagement' not in intf.tags and
                'ifRole.SimulatedInterface' not in intf.tags and
                'ifRole.Internal' not in intf.tags)

    def is_otn_interface(self, intf):
        """
        Check this is one of the supported OTN interfaces

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        """
        return 'ifRole.OTN' in intf.tags

    def basic_interface_match(self, intf):
        """
        "Core" check to decide if we want to monitor this interface.
        This checks its Admin status and skips internal interfaces (loopback, out
        of band management ports, etc). We do not monitor interfaces that are in
        admin state down and loopbacks. Then this function performs several basic checks:

        - we monitor interfaces only if we were able to place them on the graph, that is, could find
          device and interface this one is connected to, OR
        - we could associate the interface with BGP session, OR
        - the interface is an aggregation port

        To change this, override `custom_interface_match()` implement your own logic.

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: True if we want to monitor this interface
        """
        return self.is_interesting_interface(intf) and (
                self.is_connected_interface(intf) or
                self.is_peering_interface(intf) or
                self.is_interesting_aggregation_port(intf)
        )

    def custom_interface_match(self, device, intf):
        """
        Placeholder method that can be used to override logic implemented by
        method `basic_interface_match()`. Unlike the former, this method gives you
        access to the device object. Implement your own logic and return True if you
        want the interface to be monitored, or False otherwise. Default implementation
        returns False which means it defers the decision to `basic_interface_match()`

        :type device: PyDevice
        :param device:   network device object
        :param intf: PyNetworkInterface wrapper object
        :return: True if we want to monitor this interface
        """
        return False

    def make_basic_vars(self, device, intf):
        """
        Generate configuration for the basic set of monitoring variables
        for the interface: interface utilization, errors, discards

        :type device: PyDevice
        :param device: PyDevice wrapper object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        mvars = {}
        if 'Vendor.Juniper' in device.tags:
            mvars.update(self.make_juniper_if_vars(device, intf))
        if 'Vendor.Cisco' in device.tags:
            mvars.update(self.make_cisco_if_extension_vars(device, intf))
        if 'Vendor.JuniperSSG' in device.tags:
            mvars.update(self.make_basic_vars_ssg(device, intf))
        elif 'SupportedMIBs.UBNT-UniFi-MIB' in device.tags:
            mvars.update(self.make_basic_vars_ubnt_unifi(device, intf))
        else:
            mvars.update(self.make_rfc1213_vars(device, intf, intf.if_index))
        return mvars

    def make_rfc1213_vars(self, device, intf, if_index):
        """
        Make monitoring variables for the interface given its ifIndex. Note that
        for interfaces of Juniper SSG fixtures ifIndex may come from a field different
        than intf.if_index, that is why it is passed as an argument

        :param device: PyDevice wrapper object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :param if_index:  ifIndex value
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_high_speed = intf.if_high_speed

        # choose the oid for interface speed. the "old" oid ifSpeed gives better resolution
        # for 'slow' interfaces (<10mbps), while "new" oid ifHighSpeed gives better range
        # for fast interfaces. When a customer uses "bandwidth" operator on the interface
        # to set actual available bandwidth which is lower than interface physical speed,
        # they want maximum available resolution. For example, when they set "bandwidth 1544"
        # on a GigE interface.
        intf_mvars = {}

        if 'SupportedMIBs.JUNIPER-IF-MIB:ifHCIn1SecRate' in device.tags:
            intf_mvars.update({
                'ifInRate': {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IF-MIB:ifHCIn1SecRate.{0}'.format(if_index)
                },
                'ifOutRate': {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IF-MIB:ifHCOut1SecRate.{0}'.format(if_index)
                }
            })
        else:
            if 'SupportedMIBs.IF-MIB' not in device.tags or is_always_32_bit_interface_counters(device):
                in_octets_oid = 'IF-MIB:ifInOctets.{0}'.format(if_index)
                out_octets_oid = 'IF-MIB:ifOutOctets.{0}'.format(if_index)
            else:
                in_octets_oid = 'IF-MIB:ifHCInOctets.{0}'.format(if_index)
                out_octets_oid = 'IF-MIB:ifHCOutOctets.{0}'.format(if_index)

            intf_mvars.update({
                'ifHCInOctets': {
                    'component': intf,
                    'snmp_oid': in_octets_oid
                },
                'ifHCOutOctets': {
                    'component': intf,
                    'snmp_oid': out_octets_oid
                }
            })

        if 'SupportedMIBs.IF-MIB' in device.tags and (if_high_speed > 10 or is_always_high_speed(intf.name)):
            # if 'SupportedMIBs.IF-MIB' in device.tags:
            # see NET-3774
            intf_mvars['ifHighSpeed'] = {
                'component': intf,
                'snmp_oid': 'IF-MIB:ifHighSpeed.{0}'.format(if_index),
            }
        else:
            # see NET-3774
            intf_mvars['ifSpeed'] = {
                'component': intf,
                'snmp_oid': 'IF-MIB:ifSpeed.{0}'.format(if_index),
            }

        other = {
            'ifInErrors': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifInErrors.{0}'.format(if_index)
            },

            'ifOutErrors': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifOutErrors.{0}'.format(if_index)
            },

            # ---------------------------------------------------------------
            'ifInDiscards': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifInDiscards.{0}'.format(if_index)
            },

            'ifOutDiscards': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifOutDiscards.{0}'.format(if_index)
            },

            # ---------------------------------------------------------------
            'ifOperStatus': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifOperStatus.{0}'.format(if_index),
            },

            # ---------------------------------------------------------------
            'ifLastChange': {
                'component': intf,
                'snmp_oid': 'RFC1213-MIB:ifLastChange.{0}'.format(if_index),
            },

            # ---------------------------------------------------------------
            # interface description (ifAlias). This is a string variable.
            'ifAlias': {
                'component': intf,
                'snmp_oid': 'IF-MIB:ifAlias.{0}'.format(if_index),
                'type': MonitoringDataType.String,
            },
        }

        intf_mvars.update(other)
        return intf_mvars

    def make_basic_vars_ssg(self, device, intf:PyNetworkInterface):
        """
        Generate configuration for the basic set of monitoring variables
        for the interface: interface utilization, errors, discards.
        This is only for Juniper SSG fixtures. We monitor interfaces
        that are exposed via RFC1213-MIB using OIDs from it, but SSG exposes
        only subset of interfaces that way. Other interfaces are monitored
        via NETSCREEN-INTERFACE-MIB.

        :type device: PyDevice
        :param device: PyDevice wrapper object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        real_rfc1213_ifindex = intf.getIntf().getRealRfc1213IfIndex()
        if real_rfc1213_ifindex != -1:
            return self.make_rfc1213_vars(device, intf, real_rfc1213_ifindex)

        if_index = intf.if_index

        return {
            'ifHCInOctets': {
                'component': intf,
                'snmp_oid': 'NETSCREEN-INTERFACE-MIB:nsIfFlowOutByte.{0}'.format(if_index),
            },

            'ifHCOutOctets': {
                'component': intf,
                'snmp_oid': 'NETSCREEN-INTERFACE-MIB:nsIfFlowInByte.{0}'.format(if_index),
            },

            'nsIfStatus': {
                'component': intf,
                'snmp_oid': 'NETSCREEN-INTERFACE-MIB:nsIfStatus.{0}'.format(if_index),
            },

        }

    def make_basic_vars_ubnt_unifi(self, device, intf):
        """
        Generate configuration for the basic set of monitoring variables
        for the interface: interface utilization, errors, discards.
        This is only for Ubiquiti fixtures and uses UBNT-Unifi-MIB.

        :type device: PyDevice
        :param device: PyDevice wrapper object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        intf_vars = self.make_rfc1213_vars(device, intf, intf.if_index)
        alt_index = intf.getIntf().getAlternateIndex()
        if alt_index != -1:
            intf_vars['ifSpeed'] = {
                'component': intf,
                'snmp_oid': 'UBNT-UniFi-MIB:unifiIfSpeed.{0}'.format(alt_index),
                'scale': 1E6  # like ifHighSpeed, in 1,000,000 bits/sec
            }
        return intf_vars

    def make_packet_counter_vars(self, intf):
        """
        Generate configuration for the packet counter set of monitoring variables
        for the interface: ifHCInUcastPkts, ifHCInMulticastPkts, ifHCInBroadcastPkts
        and similar for outbound

        These variables are not activated by default. To activate them, add call to
        self.make_packet_counter_vars() in make_variables()

        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index
        res = {}
        if intf.if_high_speed > 0:
            for oid in ['ifHCInUcastPkts', 'ifHCInMulticastPkts', 'ifHCInBroadcastPkts', 'ifHCOutUcastPkts',
                        'ifHCOutMulticastPkts', 'ifHCOutBroadcastPkts']:
                res[oid] = {
                    'component': intf,
                    'snmp_oid': 'IF-MIB:{0}.{1}'.format(oid, if_index)
                }
        else:
            for oid in ['ifInMulticastPkts', 'ifInBroadcastPkts', 'ifOutMulticastPkts', 'ifOutBroadcastPkts']:
                res[oid] = {
                    'component': intf,
                    'snmp_oid': 'IF-MIB:{0}.{1}'.format(oid, if_index)
                }
            for oid in ['ifInUcastPkts', 'ifOutUcastPkts']:
                res[oid] = {
                    'component': intf,
                    'snmp_oid': 'RFC1213-MIB:{0}.{1}'.format(oid, if_index)
                }
        return res

    def convert_to_dot_separated(self, name):
        """
        Convert a string to a dot separated sequence of decimal representation of each
        character, prepended with a number of characters. For example, string '1.10' is
        converted to '4.49.46.49.48' and 'mgmt0' converts to '5.109.103.109.116.48'

        :param name:  a string
        :return:      another string that consists of decimal representations of characters
        """
        return str(len(name)) + '.' + '.'.join([str(ord(c)) for c in name])

    def make_duplex_status_vars(self, device, intf):
        """
        Generate configuration for the monitoring variables to track "duplex" status of the interface.
        Note that actual OIDs and returned values depend on the vendor and availability of support
        for EtherLike-MIB. Normalization happens later in nw2rules.py

        These variables are not activated by default. To activate them, add call to
        self.make_duplex_status_vars() in make_variables()

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index
        res = {}
        if 'SupportedMIBs.EtherLike-MIB' in device.tags:
            res['dot3StatsDuplexStatus'] = {
                'component': intf,
                'snmp_oid': 'EtherLike-MIB:dot3StatsDuplexStatus.{0}'.format(if_index)
            }
        else:
            if 'Vendor.F5' in device.tags:
                # the index in F5-BIGIP-SYSTEM-MIB::sysInterfaceEntry is interface name as a sequence
                # of decimal numbers, preceded with a number of characters
                res['sysInterfaceMediaActiveDuplex'] = {
                    'component': intf,
                    'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysInterfaceMediaActiveDuplex.{0}'.format(
                        self.convert_to_dot_separated(intf.name))
                }
            elif 'Vendor.A10' in device.tags:
                res['axInterfaceMediaActiveDuplex'] = {
                    'component': intf,
                    'snmp_oid': 'A10-AX-MIB:axInterfaceMediaActiveDuplex.{0}'.format(if_index)
                }
            elif 'Vendor.Viptela' in device.tags:
                res['viptelaInterfaceDuplex'] = {
                    'component': intf,
                    'snmp_oid': 'VIPTELA-OPER-VPN:interfaceDuplex.{0}'.format(if_index)
                }

        return res

    def make_cos_vars(self, device, intf):
        """
        Generate configuration for the set of COS monitoring variables
        for the interface: tail and red drops.

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index
        cos_vars = {}
        if 'Vendor.Juniper' in device.tags:
            configured_queues = intf.cos_queues

            # TODO: use PyDevice.isSupported() instead:
            # device.isSupported('JUNIPER-COS-MIB:jnxCosQstatTotalDropPkts')
            # device.isSupported('JUNIPER-COS-MIB:jnxCosQstatTailDropPkts')
            #
            total_drops_supported = 'SupportedMIBs.JUNIPER-COS-MIB:jnxCosQstatTotalDropPkts' in device.tags
            tail_drops_supported = 'SupportedMIBs.JUNIPER-COS-MIB:jnxCosQstatTailDropPkts' in device.tags

            for queue in configured_queues:
                fc_number = device.getFcNumber(queue)
                fc_name_tag = 'CoS.{0}'.format(device.getFcName(fc_number))

                if tail_drops_supported:
                    cos_vars['jnxCosTailDropPktsQueue{0}'.format(queue)] = {
                        'component': intf,
                        'snmp_oid': 'JUNIPER-COS-MIB:jnxCosQstatTailDropPkts.{0}.{1}'.format(if_index, queue),
                        'tags': fc_name_tag
                    }
                    # this name is inconsistent (tail drops var above does not have "Qstat" in its name)
                    # but this name matches what nw2rules.py expects, so I keep it
                    cos_vars['jnxCosQstatTotalRedDropPktsQueue{0}'.format(queue)] = {
                        'component': intf,
                        'snmp_oid': 'JUNIPER-COS-MIB:jnxCosQstatTotalRedDropPkts.{0}.{1}'.format(if_index, queue),
                        'tags': fc_name_tag
                    }
                if total_drops_supported:
                    cos_vars['jnxCosTotalDropPktsQueue{0}'.format(queue)] = {
                        'component': intf,
                        'snmp_oid': 'JUNIPER-COS-MIB:jnxCosQstatTotalDropPkts.{0}.{1}'.format(if_index, queue),
                        'tags': fc_name_tag
                    }

                cos_vars['jnxCosQstatTxedPkts{0}'.format(queue)] = {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-COS-MIB:jnxCosQstatTxedPkts.{0}.{1}'.format(if_index, queue),
                    'tags': fc_name_tag
                }
                cos_vars['jnxCosQstatTxedBytes{0}'.format(queue)] = {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-COS-MIB:jnxCosQstatTxedBytes.{0}.{1}'.format(if_index, queue),
                    'tags': [fc_name_tag]
                }

        return cos_vars

    def make_igp_metrics_vars(self, device, intf):
        """
        Generate configuration for the set of IGP metrics monitoring variables
        for the interface: ISIS circuit metrics and OSPF interface metrics

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index
        circuit = intf.isis_circuit
        level = device.getIsIsCircuitLevel(circuit)

        mvars = {}
        if level == 1:
            mvars['isisCircLevel1Metrics'] = {
                'component': intf,
                'snmp_oid': 'ISIS-MIB:isisCircLevelWideMetric.{0}.1'.format(intf.isis_circuit),
            }

        if level == 2:
            mvars['isisCircLevel2Metrics'] = {
                'component': intf,
                'snmp_oid': 'ISIS-MIB:isisCircLevelWideMetric.{0}.2'.format(intf.isis_circuit),
            }

        if device.getOspfAdminStatus() == OSPF_ADMIN_STATUS_ENABLE and intf.address:
            addr_net = ipaddr.IPNetwork(intf.address)
            mvars['ospfIfMetricValue'] = {
                'component': intf,
                'snmp_oid': 'OSPF-MIB:ospfIfMetricValue.{0}.0.0'.format(str(addr_net.ip)),
            }

        return mvars

    def make_lacp_vars(self, device, intf):
        """
        Generate configuration for the set of LACP-related monitoring variables
        for the interface

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index

        # # NSGDB-153
        # # intf is a physical port rather than subinterface if we discovered association between
        # # aggregator ports and aggregation interfaces using JUNIPER-L2CP-FEATURES-MIB instead of
        # # IEEE8023-LAG-MIB. This happens when we encounter Junos bug described in the ticket NSGDB-153.
        # # Even when this bug is triggered, IEEE8023-LAG-MIB:dot3adAggPortActorOperState still works,
        # # but expects ifIndex of a subinterface. It is easier to use SupportedMIBs.JUNIPER-L2CP-FEATURES-MIB
        # # instead of searching subinterface of {intf} here.
        #
        # if 'ifRole.PhysicalPort' in intf.tags and 'SupportedMIBs.JUNIPER-L2CP-FEATURES-MIB' in device.tags:
        #     return {
        #         'dot3adAggPortActorOperState': {
        #             'component': intf,
        #             'snmp_oid': 'JUNIPER-L2CP-FEATURES-MIB:dot3adOperState.{0}'.format(if_index),
        #             'type': MonitoringDataType.HexString
        #         },
        #     }

        if 'SupportedMIBs.IEEE8023-LAG-MIB' in device.tags:
            return {
                'dot3adAggPortActorOperState': {
                    'component': intf,
                    'snmp_oid': 'IEEE8023-LAG-MIB:dot3adAggPortActorOperState.{0}'.format(if_index),
                    'type': MonitoringDataType.HexString
                },
            }
        else:
            return {}

    def make_ipv6_counter_vars(self, device, intf):
        """
        Generate configuration for the packet counter set of monitoring variables
        for the interface: ifHCInUcastPkts, ifHCInMulticastPkts, ifHCInBroadcastPkts
        and similar for outbound

        These variables are not activated by default. To activate them, add call to
        self.make_packet_counter_vars() in make_variables()

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if_index = intf.if_index
        res = {}
        if 'Vendor.Juniper' in device.tags and 'SupportedMIBs.JUNIPER-IPv6-MIB' in device.tags:
            for oid in ['jnxIpv6IfInOctets', 'jnxIpv6IfOutOctets']:
                res[oid] = {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IPv6-MIB:{0}.{1}'.format(oid, if_index)
                }
        return res

    def make_otn_vars(self, device, intf):
        """
        Generate configuration for the set of OTN metrics. Currently supported only
        for Cisco Network Convergence System 1002 fixtures. The interface is identified
        by the tag ifRole.OTN that is set simply by checking its ifType in InterfaceClassificator

        NSGHELP-672

        per explicit request from Dbx, we monitor only interval "15min" (second index == 1)
        but since others may want to track other available intervals, I am adding suffix "15min"
        to the variable name

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf: PyNetworkInterface wrapper object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        return {
            'coiFECCurrentCorBitErrs15min': {
                'component': intf,
                'snmp_oid': 'CISCO-OTN-IF-MIB:coiFECCurrentCorBitErrs.{0}.1'.format(intf.if_index),
            },
            'coiFECCurrentUncorWords15min': {
                'component': intf,
                'snmp_oid': 'CISCO-OTN-IF-MIB:coiFECCurrentUncorWords.{0}.1'.format(intf.if_index),
            },
        }

    def make_juniper_if_vars(self, device, intf):
        """
        NSGHELP-890 NET-7005
        Add OID  ifJnxCarrierTrans  from JUNIPER-IF_MIB
        """
        return {
            'ifCarrierTransitionCount': {
                'component': intf,
                'snmp_oid': 'JUNIPER-IF-MIB:ifJnxCarrierTrans.{0}'.format(intf.if_index)
            }
        }

    def make_cisco_if_extension_vars(self, device, intf):
        """
        NSGHELP-890 NET-7005
        Add OID  cieIfCarrierTransitionCount  from CISCO-IF-EXTENSION-MIB
        """
        return {
            'ifCarrierTransitionCount': {
                'component': intf,
                'snmp_oid': 'CISCO-IF-EXTENSION-MIB:cieIfCarrierTransitionCount.{0}'.format(intf.if_index)
            }
        }

    def make_variables(self, device, intf):
        """
        Given device and network interface objects, build set of monitoring variables
        for the interface

        :type device: PyDevice
        :param device:   network device object
        :type intf: PyNetworkInterface
        :param intf:     network interface object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(intf, PyNetworkInterface)

        if self.is_simulated_ipsec_tunnel_interface(device, intf):
            return {}

        mvars = {}

        # self.log.info('Analyse interface: {0}'.format(str(intf)))

        if self.basic_interface_match(intf) or self.custom_interface_match(device, intf):
            mvars.update(self.make_basic_vars(device, intf))
            mvars.update(self.make_cos_vars(device, intf))
            mvars.update(self.make_ipv6_counter_vars(device, intf))

            if self.make_interface_packet_counter_vars:
                mvars.update(self.make_packet_counter_vars(intf))

            if self.make_interface_duplex_status_vars:
                mvars.update(self.make_duplex_status_vars(device, intf))

        if self.is_aggregation_port(intf):
            mvars.update(self.make_lacp_vars(device, intf))

        if self.is_interesting_interface(intf) or self.is_juniper_parent_of_aggregation_port(intf):
            mvars.update(self.make_igp_metrics_vars(device, intf))

        if self.is_otn_interface(intf):
            self.log.info('Found OTN interface: {0}'.format(str(intf)))
            mvars.update(self.make_otn_vars(device, intf))


        return mvars
