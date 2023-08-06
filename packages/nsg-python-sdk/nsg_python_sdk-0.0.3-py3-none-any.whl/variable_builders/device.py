"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly
prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution and may
change in the future versions.

"""

from net.happygears.nsgpython.common import HappyGearsOids
from net.happygears.nw2.py import MonitoringDataType
from net.happygears.nw2.py.py_wrappers import PyDevice

from variable_builders.base_variable_builder import BaseVariableBuilder
from variable_builders.load_balancer import LoadBalancerVariableBuilder


class DeviceVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build monitoring variables for the device.
    We create an object of this class and call its method `make_variable()`
    for all fixtures. If you need to add, remove or modify monitoring variables,
    create your own class based on this and overwrite method `make_variable()`
    in it.
    """

    def __init__(self, log):
        super(DeviceVariableBuilder, self).__init__(log)

    def make_walk_polling_vars(self, device):
        """
        make variables for things we monitor by walking. Usually this means that components
        are not created during discovery time because they fluctuate at the run time.
        """
        mvars = {}
        # for all vendors: OSPF-MIB:ospfNbrState

        if 'SupportedMIBs.OSPF-MIB' in device.tags:
            mvars['ospfNbrState'] = {
                'index': 1,
                'snmp_walk_oid': 'OSPF-MIB:ospfNbrState',
                'type': MonitoringDataType.Int
            }

        # TODO: we should revert the change that removed attempt to walk VIPTELA-SECURITY MIB at discovery time
        #       at least to be able to register the fact that this MIB is supported and then check for it here

        if 'Vendor.Viptela' in device.tags:
            # fix monitoring type because device responds with variable type OCTET STRING
            mvars.update({
                # These aren't really part of the CPU, but they do occur on Viptela fixtures
                # identified by this component.oid. It's a chicken/egg problem: these variables
                # generate new components when we poll them, but no such component is known at
                # discovery time. The number and type of such components fluctuates during the
                # device's uptime, so it would not make sense to enumerate such components at
                # discovery time for the purpose of creating these variables.
                'viptelaControlConnectionsState': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsState',
                    'type': MonitoringDataType.Int
                },

                'viptelaControlConnectionsProtocol': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsProtocol',
                    'type': MonitoringDataType.Int
                },

                'viptelaControlConnectionsLocalColor': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsLocalColor',
                    'type': MonitoringDataType.Int
                },

                'viptelaControlConnectionsSystemIp': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsSystemIp',
                    'type': MonitoringDataType.String
                },

                'viptelaControlConnectionsPrivateIp': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsPrivateIp',
                    'type': MonitoringDataType.String
                },

                # device returns uptime as human-readable string:
                # .1.3.6.1.4.1.41916.4.2.2.1.20.0.3.201.1.4.10.106.250.29.41690.4.52.8.172.6.23456 = STRING: "0:09:50:34"
                'viptelaControlConnectionsUptime': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-SECURITY:controlConnectionsUptime',
                    'type': MonitoringDataType.String
                },
            })

        if device.isSupported('ISIS-MIB:isisISAdjIPAddrTable') and device.isSupported('ISIS-MIB:isisISAdjState'):
            # Note: the MonitoringDataType is not used here; instead, certain items are extracted
            # from the table and given variable/tag names of their own. The table needs to be processed
            # as a unit, however, so that entries with matching OID index segments can be paired up.
            mvars['isisISAdj'] = {
                'index': 1,
                'snmp_walk_oid': 'ISIS-MIB:isisISAdj',
                'type': MonitoringDataType.Int
            }

        return mvars

    def make_routing_table_size_vars(self, device):
        """
        Given device object, build set of monitoring variables
        to monitor size of the routing table

        :type device: PyDevice
        :param device:   network device object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        mvars = {}

        if 'SupportedMIBs.IP-FORWARD-MIB' in device.tags:
            ip4var = {
                'index': 1,
                'name': 'Device',
                'type': MonitoringDataType.Gauge,
            }
            # if device.isSupported('IP-FORWARD-MIB:ipCidrRouteNumber'):
            #     ip4var['snmp_oid'] = 'IP-FORWARD-MIB:ipCidrRouteNumber.0'
            # if device.isSupported('IP-FORWARD-MIB:inetCidrRouteNumber'):
            #     ip4var['snmp_oid'] = 'IP-FORWARD-MIB:inetCidrRouteNumber.0'
            if device.ip_cidr_route_number_supported:
                ip4var['snmp_oid'] = 'IP-FORWARD-MIB:ipCidrRouteNumber.0'
            if device.inet_cidr_route_number_supported:
                ip4var['snmp_oid'] = 'IP-FORWARD-MIB:inetCidrRouteNumber.0'
            mvars['ipv4CidrRouteNumber'] = ip4var
        elif 'SupportedMIBs.CUMULUS-RESOURCES-MIB' in device.tags and device.ip_cidr_route_number_supported:
            # it is unclear from the definition of this OID in CUMULUS-RESOURCES-MIB if it
            # covers only ipv4 or ipv4 and ipv6. This means I can't use variable names
            # ipv4CidrRouteNumber and ipv6CidrRouteNumber because they refer ipv4/ipv6 explicitly
            mvars['l3RoutingTableCurrentEntries'] = {
                'snmp_oid': 'CUMULUS-RESOURCES-MIB:l3RoutingTableCurrentEntries',
                'index': 1,
                'name': 'Device',
                'type': MonitoringDataType.Gauge,
            }

        if 'SupportedMIBs.IPV6-MIB' in device.tags and device.ipv_6_route_number_supported:
            mvars['ipv6CidrRouteNumber'] = {
                'snmp_oid': 'IPV6-MIB:ipv6RouteNumber.0',
                'index': 1,
                'name': 'Device',
                'type': MonitoringDataType.Gauge,
            }

        return mvars

    def make_time_since_config_change_var(self, device):
        """
        Given device object, build set of monitoring variables
        to monitor the time since last configuration change

        :type device: PyDevice
        :param device:   network device object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        name = None
        oid = None
        if 'Vendor.Cisco' in device.tags:
            name = 'ccmHistoryRunningLastChanged'
            oid = 'CISCO-CONFIG-MAN-MIB:ccmHistoryRunningLastChanged.0'
        elif 'Vendor.Juniper' in device.tags:
            name = 'jnxCmCfgChgLatestTime'
            oid = 'JUNIPER-CFGMGMT-MIB:jnxCmCfgChgLatestTime.0'
        else:
            return {}

        mvars = {
            name: {
                'snmp_oid': oid,
                'index': 1,  # should be the same index as the one we use for sysUpTime
                'name': 'Device Configuration',
                'type': MonitoringDataType.TimeTick,
            },
        }

        return mvars

    def make_uptime_var(self, device):
        """
        SNMPv2-MIB:sysUpTime measures device uptime in 1/100 sec and rolls over in 497 days because
        it is a 32-bit integer. SNMP-FRAMEWORK-MIB:snmpEngineTime is also 32-bit integer but measures
        uptime in seconds, so it takes 100 times longer to roll over.

        :type device: PyDevice
        :param device:   network device object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        if device.isSupported('SNMP-FRAMEWORK-MIB:snmpEngineTime'):
            return {
                'snmpEngineTime': {
                    'snmp_oid': 'SNMP-FRAMEWORK-MIB:snmpEngineTime.0',
                    'index': 1,
                    'name': 'SNMP Agent',
                    'type': MonitoringDataType.Gauge,
                }}
        else:
            # do not change index without changing it in MonitoredNodeContainer constructor
            return {
                'snmpV2SysUpTime': {
                    'snmp_oid': 'SNMPv2-MIB:sysUpTime.0',
                    'index': 1,
                    'name': 'SNMP Agent',
                    'type': MonitoringDataType.TimeTick,
                }}

    def make_process_variables(self, device):
        """
        Goal: process table with name, cpu, and memory columns

        :type device: PyDevice
        :param device:   network device object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        new_vars = {}

        if 'Darwin' in device.sys_descr:
            # As of this writing (v 10.14.5), polling these variables causes Mac OSX's stock snmpd to crash
            return new_vars

        # Colin has added hrSWRunName and other variables here but the reason has been lost in the mist of time.
        # I suspect this was a good testbed to develop transformers with.
        # As far as I can tell, we do not really need these in production.

        if 'Vendor.NetSnmp' in device.tags:
            if device.isSupported('HOST-RESOURCES-MIB:hrSWRunName'):
                new_vars['hrSWRunName'] = {
                    'snmp_walk_oid': 'HOST-RESOURCES-MIB:hrSWRunName',
                    'index': 1,
                    'name': 'SNMP Agent',
                    'type': MonitoringDataType.String,
                }
            if device.isSupported('HOST-RESOURCES-MIB:hrSWRunPerfMem'):
                new_vars['hrSWRunPerfMem'] = {
                    'snmp_walk_oid': 'HOST-RESOURCES-MIB:hrSWRunPerfMem',
                    'index': 1,
                    'name': 'SNMP Agent',
                    'type': MonitoringDataType.Int,
                }
            if device.isSupported('HOST-RESOURCES-MIB:hrSWRunPerfCPU'):
                new_vars['hrSWRunPerfCPU'] = {
                    'snmp_walk_oid': 'HOST-RESOURCES-MIB:hrSWRunPerfCPU',
                    'index': 1,
                    'name': 'SNMP Agent',
                    'type': MonitoringDataType.Int,
                }
        return new_vars

    def make_ha_variables(self, device):
        assert isinstance(device, PyDevice)
        new_vars = {}
        # We record these variable with a Str suffix here; a compute plugin maps the
        # string values to integers later.
        if device.isSupported('IB-PLATFORMONE-MIB:ibHaStatus'):
            new_vars['ibHaStatusStr'] = {
                'snmp_oid': 'IB-PLATFORMONE-MIB:ibHaStatus.0',
                'index': 1,
                'name': 'High Availability Status',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('IB-PLATFORMONE-MIB:ibGridStatus'):
            new_vars['ibGridStatusStr'] = {
                'snmp_oid': 'IB-PLATFORMONE-MIB:ibGridStatus.0',
                'index': 1,
                'name': 'Grid Status',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('IB-PLATFORMONE-MIB:ibGridMasterCandStatus'):
            new_vars['ibGridMasterCandStatusStr'] = {
                'snmp_oid': 'IB-PLATFORMONE-MIB:ibGridMasterCandStatus.0',
                'index': 1,
                'name': 'Grid Master Candidate Status',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('IB-PLATFORMONE-MIB:ibGridReplicationState'):
            new_vars['ibGridReplicationStateStr'] = {
                'snmp_oid': 'IB-PLATFORMONE-MIB:ibGridReplicationState.0',
                'index': 1,
                'name': 'Grid Replication State',
                'type': MonitoringDataType.String,
            }
        # This is just an ordinary string-valued variable.
        if device.isSupported('IB-PLATFORMONE-MIB:ibGridMasterVIP'):
            new_vars['ibGridMasterVIP'] = {
                'snmp_oid': 'IB-PLATFORMONE-MIB:ibGridMasterVIP.0',
                'index': 1,
                'name': 'Grid Master VIP',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('PAN-COMMON-MIB:panSysHAMode'):
            new_vars['panSysHAModeStr'] = {
                'snmp_oid': 'PAN-COMMON-MIB:panSysHAMode.0',
                'index': 1,
                'name': 'PAN Sys HA Mode',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('PAN-COMMON-MIB:panSysHAState'):
            new_vars['panSysHAStateStr'] = {
                'snmp_oid': 'PAN-COMMON-MIB:panSysHAState.0',
                'index': 1,
                'name': 'PAN Sys HA State',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('PAN-COMMON-MIB:panSysHAPeerState'):
            new_vars['panSysHAPeerStateStr'] = {
                'snmp_oid': 'PAN-COMMON-MIB:panSysHAPeerState.0',
                'index': 1,
                'name': 'PAN Sys HA Peer State',
                'type': MonitoringDataType.String,
            }
        if device.isSupported('PAN-COMMON-MIB:panChassisType'):
            new_vars['panChassisType'] = {
                'snmp_oid': 'PAN-COMMON-MIB:panChassisType.0',
                'index': 1,
                'name': 'PAN Chassis Type',
                'type': MonitoringDataType.String,
            }
        return new_vars

    def make_bfd_variables(self, device):
        if device.isSupported('VIPTELA-BFD:bfdSummary'):
            return {
                'bfdSummaryBfdSessionsUp': {
                    'index': 1,
                    'snmp_oid': 'VIPTELA-BFD:bfdSummaryBfdSessionsUp.0',
                    'type': MonitoringDataType.Unsigned
                },

                'bfdSummaryBfdSessionsTotal': {
                    'index': 1,
                    'snmp_oid': 'VIPTELA-BFD:bfdSummaryBfdSessionsTotal.0',
                    'type': MonitoringDataType.Unsigned
                },

                'bfdSummaryBfdSessionsMax': {
                    'index': 1,
                    'snmp_oid': 'VIPTELA-BFD:bfdSummaryBfdSessionsMax.0',
                    'type': MonitoringDataType.Unsigned
                },

                'bfdSummaryBfdSessionsFlap': {
                    'index': 1,
                    'snmp_oid': 'VIPTELA-BFD:bfdSummaryBfdSessionsFlap.0',
                    'type': MonitoringDataType.Unsigned
                },

                'bfdSessionsListTable': {
                    'index': 1,
                    'snmp_walk_oid': 'VIPTELA-BFD:bfdSessionsListTable',
                    'type': MonitoringDataType.Int
                }
            }
        else:
            return {}

    def make_vsys_variables(self, device):
        mvars = {}
        if device.isSupported('PAN-COMMON-MIB:panSessionActive'):
            mvars['panSessionActive'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panSessionActive.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panSessionActiveTcp'):
            mvars['panSessionActiveTcp'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panSessionActiveTcp.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panVsysActiveSessions'):
            mvars['panVsysActiveSessions'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panVsysActiveSessions.1',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panVsysMaxSessions'):
            mvars['panVsysMaxSessions'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panVsysMaxSessions.1',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panVsysSessionUtilizationPct'):
            mvars['panVsysSessionUtilizationPct'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panVsysSessionUtilizationPct.1',
                'type': MonitoringDataType.Int
            }
        return mvars

    def make_vpn_variables(self, device, _=None):
        if device.isSupported('JUNIPER-VPN-MIB:jnxVpnActiveVpns'):
            return {
                'jnxVpnActiveVpns': {
                    'index': 1,
                    'snmp_oid': 'JUNIPER-VPN-MIB:jnxVpnActiveVpns.0',
                    'type': MonitoringDataType.Gauge
                }
            }
        else:
            return {}

    def make_disk_variables(self, device, _=None):
        mvars = {}
        if device.isSupported('PULSESECURE-PSG-MIB:iveSwapUtil'):
            mvars['iveSwapUtil'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:iveSwapUtil.0',
                'type': MonitoringDataType.Gauge
            }
        if device.isSupported('PULSESECURE-PSG-MIB:diskFullPercent'):
            mvars['diskFullPercent'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:diskFullPercent.0',
                'type': MonitoringDataType.Gauge
            }
        return mvars

    def make_auth_variables(self, device, _=None):
        mvars = {}
        if device.isSupported('CPPM-MIB:dailySuccessAuthCount'):
            mvars['dailySuccessAuthCount'] = {
                'index': 1,
                'snmp_oid': 'CPPM-MIB:dailySuccessAuthCount.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('CPPM-MIB:dailyFailedAuthCount'):
            mvars['dailyFailedAuthCount'] = {
                'index': 1,
                'snmp_oid': 'CPPM-MIB:dailyFailedAuthCount.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('CPPM-MIB:dailyTotalAuthCount'):
            mvars['dailyTotalAuthCount'] = {
                'index': 1,
                'snmp_oid': 'CPPM-MIB:dailyTotalAuthCount.0',
                'type': MonitoringDataType.Int
            }
        return mvars

    def make_user_variables(self, device, _=None):
        mvars = {}
        if device.isSupported('PULSESECURE-PSG-MIB:signedInWebUsers'):
            mvars['signedInWebUsers'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:signedInWebUsers.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PULSESECURE-PSG-MIB:signedInMailUsers'):
            mvars['signedInMailUsers'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:signedInMailUsers.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PULSESECURE-PSG-MIB:meetingUserCount'):
            mvars['meetingUserCount'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:meetingUserCount.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PULSESECURE-PSG-MIB:iveConcurrentUsers'):
            mvars['iveConcurrentUsers'] = {
                'index': 1,
                'snmp_oid': 'PULSESECURE-PSG-MIB:iveConcurrentUsers.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panGPGWUtilizationPct'):
            mvars['panGPGWUtilizationPct'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panGPGWUtilizationPct.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panGPGWUtilizationMaxTunnels'):
            mvars['panGPGWUtilizationMaxTunnels'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panGPGWUtilizationMaxTunnels.0',
                'type': MonitoringDataType.Int
            }
        if device.isSupported('PAN-COMMON-MIB:panGPGWUtilizationActiveTunnels'):
            mvars['panGPGWUtilizationActiveTunnels'] = {
                'index': 1,
                'snmp_oid': 'PAN-COMMON-MIB:panGPGWUtilizationActiveTunnels.0',
                'type': MonitoringDataType.Int
            }

        # assume that if it supports  avCmStatusHealthAlmMaj, then it must support other OIDs in this table
        aura_cm_mib_supported = device.isSupported('AVAYA-AURA-CM-MIB:avCmStatusHealthAlmMaj')
        # documentation:
        # https://documentation.avaya.com/bundle/SNMPAdministrationAndReferenceGuide_r8.1/page/avCmStatusHealth.html
        if aura_cm_mib_supported:
            # these have type INTEGER32
            int_type_vars = [
                'avCmStatusHealthAlmMaj', 'avCmStatusHealthAlmMin', 'avCmStatusHealthAlmWrn',
                'avCmStatusHealthBusyOutTrk', 'avCmStatusHealthBusyOutStn', 'avCmStatusHealthBusyOutOth',
                'avCmStatusHealthLogins']
            for v in int_type_vars:
                mvars[v] = {
                    'index': 1,
                    'snmp_oid': 'AVAYA-AURA-CM-MIB:' + v + '.0',
                    'type': MonitoringDataType.Int
                }
            # all these are percentage values returned as a string
            # .1.3.6.1.4.1.6889.2.73.8.1.29.7.0 = STRING: 0
            str_type_vars = [
                'avCmStatusHealthOccupancySt',
                'avCmStatusHealthOccupancySm',
                'avCmStatusHealthOccupancyCp',
                'avCmStatusHealthOccupancyIdl',
                'avCmStatusHealthEntryTmRecOvrLd',
                'avCmStatusHealthExitTmRecOvrLd',
                'avCmStatusHealthLogins'
            ]
            # the value is a string, which is either a number "0" or "15%"
            for v in str_type_vars:
                mvars[v] = {
                    'index': 1,
                    'snmp_oid': 'AVAYA-AURA-CM-MIB:' + v + '.0',
                    'type': MonitoringDataType.Double
                }
        # NSGHELP-771: OIDs for Avaya G450 Media Gateways
        # the same here: I assume entire table is supported if this oid works
        g700_mib_supported = device.isSupported('G700-MG-MIB:cmgModelNumber')
        if g700_mib_supported:
            mvars['cmgRegistrationState'] = {
                'index': 1,
                'snmp_oid': 'G700-MG-MIB:cmgRegistrationState.0',
                'type': MonitoringDataType.Int
            }
            mvars['cmgH248LinkStatus'] = {
                'index': 1,
                'snmp_oid': 'G700-MG-MIB:cmgH248LinkStatus.0',
                'type': MonitoringDataType.Int
            }
            # I could not find the MIB this OID defined in. It appears to return memory utilization in percent, which
            # is what they asked in NSGHELP-771
            mvars['memUtil'] = {
                'index': 1,
                'snmp_oid': '.1.3.6.1.4.1.6889.2.1.11.1.2.6.1.3.10',
                'type': MonitoringDataType.Int
            }
            # NSGHELP-776
            # todo: need to discover this table and create these variables using h/w components
            # components these variables describe are "voip channels" which is a new concept for us.
            # One way to deal with them is to add them as generic h/w components, or maybe they
            # deserve their own h/w component class along with tunnels and sensors. Meanwhile, Gap
            # asks for very specific oids so I am going to add them just like they ask.
            mvars['cmgVoipTotalChannels'] = {
                'index': 101,
                'snmp_oid': 'G700-MG-MIB:cmgVoipTotalChannels.101',
                'type': MonitoringDataType.Int
            }
            mvars['cmgVoipChannelsInUse'] = {
                'index': 101,
                'snmp_oid': 'G700-MG-MIB:cmgVoipChannelsInUse.101',
                'type': MonitoringDataType.Int
            }
            mvars['cmgVoipAdminState'] = {
                'index': 101,
                'snmp_oid': 'G700-MG-MIB:cmgVoipAdminState.101',
                'type': MonitoringDataType.Int
            }

        # assume that if it supports memTotalReal, then it should support other memory-related OIDs as well
        # This is mostly for BigSwitch (NSGHELP-755, NSGHELP-762)
        if device.isSupported('UCD-SNMP-MIB:memTotalReal'):
            # we already have variable memAvail, I do not want to create new one even though the OID has different name
            # mvars['memAvail'] = {
            #     'index': 1,
            #     'snmp_oid': 'UCD-SNMP-MIB:memAvailReal.0',
            #     'type': MonitoringDataType.Int
            # }
            mvars['memBuffer'] = {
                'index': 1,
                'snmp_oid': 'UCD-SNMP-MIB:memBuffer.0',
                'type': MonitoringDataType.Int
            }
            mvars['memCached'] = {
                'index': 1,
                'snmp_oid': 'UCD-SNMP-MIB:memCached.0',
                'type': MonitoringDataType.Int
            }

        return mvars

    def make_variables(self, device, _=None):
        """
        Given device object, build set of monitoring variables
        for it

        :type device: PyDevice
        :param device:   network device object
        :param _: a placeholder second argument to make function signature compatible with other variable builder classes
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        # note that the name of the container should correspond to index
        # So, if the container is the same (i.e. "SNMP Agent"), then index should also be the same
        mvars = {
            'snmpTimeoutsPercentage': {
                'snmp_oid': HappyGearsOids.snmpTimeoutsOid,
                'index': 1,
                'name': 'SNMP Agent',
                # 'container': 'SNMP Agent',
                'type': MonitoringDataType.Double,
            },

            'snmpInTotalReqVars': {
                'snmp_oid': 'SNMPv2-MIB:snmpInTotalReqVars.0',
                'index': 1,
                'name': 'SNMP Agent',
                # 'container': 'SNMP Agent',
                'type': MonitoringDataType.Counter,
            },

            'monitorFreeTime': {
                'snmp_oid': HappyGearsOids.deviceMonitorFreeTimeOid,
                'index': 1,
                'name': 'SNMP Monitor',
                # 'container': 'SNMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'snmpRtt': {
                'snmp_oid': HappyGearsOids.snmpRttOid,
                'index': 1,
                'name': 'SNMP Monitor',
                # 'container': 'SNMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'icmpAvgRtt': {
                'snmp_oid': HappyGearsOids.icmpAvgRttOid,
                'index': 1,
                'name': 'ICMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'icmpMinRtt': {
                'snmp_oid': HappyGearsOids.icmpMinRttOid,
                'index': 1,
                'name': 'ICMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'icmpMaxRtt': {
                'snmp_oid': HappyGearsOids.icmpMaxRttOid,
                'index': 1,
                'name': 'ICMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'icmpLoss': {
                'snmp_oid': HappyGearsOids.icmpLossOid,
                'index': 1,
                'name': 'ICMP Monitor',
                'type': MonitoringDataType.Double,
            },

            'lastContactTime': {
                'snmp_oid': HappyGearsOids.lastContactTimeOid,
                'index': 1,
                'type': MonitoringDataType.Gauge,
            }

        }

        for f in [self.make_uptime_var,
                  self.make_time_since_config_change_var,
                  self.make_routing_table_size_vars,
                  self.make_process_variables,
                  self.make_walk_polling_vars,
                  self.make_ha_variables,
                  self.make_bfd_variables,
                  self.make_vsys_variables,
                  self.make_vpn_variables,
                  self.make_disk_variables,
                  self.make_auth_variables,
                  self.make_user_variables]:
            mvars.update(f(device))

        lb = LoadBalancerVariableBuilder(self.log)
        mvars.update(lb.make_global_variables(device))

        return mvars
