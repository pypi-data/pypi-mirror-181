"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py import MonitoringDataType
from net.happygears.nw2.py.py_wrappers import PyDevice

from variable_builders.hardware_component import HWComponentVariableBuilder


class LoadBalancerVariableBuilder(HWComponentVariableBuilder):
    """
    This class is used to build monitoring variables for load balancer fixtures
    """

    def __init__(self, log):
        super(LoadBalancerVariableBuilder, self).__init__(log)

    def make_global_variables(self, device):
        """
        Build "global" monitoring variables for a load balancer device. These variables
        track parameters that can be attirbuted to the device as a whole rather than one
        of its components, vservers, server pools or servers.

        this is called by DeviceVariableBuilder

        :type device: PyDevice
        :param device:   network device object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        if 'Vendor.F5' not in device.tags:
            return {}

        return {
            'f5SysStatClientTotConns': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatClientTotConns.0'
            },

            'f5SysStatClientCurConns': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatClientCurConns.0'
            },

            'f5SysClientsslStatCurNativeConns': {
                'index': 1,
                'name': 'sysGlobalClientSslStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysClientsslStatCurNativeConns.0'
            },

            'f5SysClientsslStatCurCompatConns': {
                'index': 1,
                'name': 'sysGlobalClientSslStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysClientsslStatCurCompatConns.0'
            },

            'f5SysStatClientBytesIn': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatClientBytesIn.0'
            },

            'f5SysStatClientBytesOut': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatClientBytesOut.0'
            },

            'f5SysStatServerBytesIn': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatServerBytesIn.0'
            },

            'f5SysStatServerBytesOut': {
                'index': 1,
                'name': 'sysGlobalStat',
                'type': MonitoringDataType.Counter64,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysStatServerBytesOut.0'
            },

            'f5SysCmFailoverStatusId': {
                'index': 1,
                'name': 'failoverStatus',
                'type': MonitoringDataType.Gauge,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysCmFailoverStatusId.0'
            },

            'f5SysCmSyncStatusId': {
                'index': 1,
                'name': 'syncStatus',
                'type': MonitoringDataType.Gauge,
                'snmp_oid': 'F5-BIGIP-SYSTEM-MIB:sysCmSyncStatusId.0'
            },

        }

    # def make_variables(self, device, component):
    #     """
    #     Given device and h/w component objects, build set of monitoring variables
    #     for the component
    #
    #     :type device: PyDevice
    #     :param device:   network device object
    #     :type component: PyHardwareComponent
    #     :param component:     PyVirtualServer or PyServerPool object
    #     :return: a dictionary where the key is variable name and value is another dictionary
    #     """
    #     assert isinstance(device, PyDevice)
    #
    #     if isinstance(component, PyVirtualServer):
    #         return self.make_vserver_variables(device, component)
    #     elif isinstance(component, PyServerPool):
    #         return self.make_server_pool_variables(device, component)
    #     elif isinstance(component, PyLbNode):
    #         return self.make_lb_node_variables(device, component)
    #     else:
    #         return {}

    def make_vserver_variables(self, device, vserver):
        """
        Make monitoring variables for the VirtualServer object
        
        :type device:    PyDevice
        :param device:   network device object
        :type vserver:   PyVirtualServer
        :param vserver:  virtual server object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        if 'Vendor.F5' not in device.tags:
            return {}

        subind = vserver.encoded_oid_subindex

        if not subind:
            return {}

        var_dict = self.make_vars_using_var_hint(device, vserver)

        mv = {
            'ltmVsStatusEnabledState': {
                'component': vserver,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmVsStatusEnabledState.{0}'.format(subind)
            },

            'ltmVsStatusAvailState': {
                'component': vserver,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmVsStatusAvailState.{0}'.format(subind)
            },

            'ltmVirtualServStatClientCurConns': {
                'component': vserver,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmVirtualServStatClientCurConns.{0}'.format(subind)
            },

        }

        var_dict.update(mv)
        return var_dict

    def make_server_pool_variables(self, device, pool):
        """
        Make monitoring variables for the ServerPool object
        
        :type device:    PyDevice
        :param device:   network device object
        :type pool:      PyServerPool
        :param pool:     server pool object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        if 'Vendor.F5' not in device.tags:
            return {}

        subind = pool.encoded_oid_subindex

        if not subind:
            return {}

        var_dict = self.make_vars_using_var_hint(device, pool)

        mv = {
            'ltmPoolMemberCnt': {
                'component': pool,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmPoolMemberCnt.{0}'.format(subind)
            },

            'ltmPoolActiveMemberCnt': {
                'component': pool,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmPoolActiveMemberCnt.{0}'.format(subind)
            },

            'ltmPoolStatusEnabledState': {
                'component': pool,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmPoolStatusEnabledState.{0}'.format(subind)
            },

            'ltmPoolStatusAvailState': {
                'component': pool,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmPoolStatusAvailState.{0}'.format(subind)
            }
        }

        var_dict.update(mv)
        return var_dict

    def make_lb_node_variables(self, device, lb_node):
        """
        Make monitoring variables for the Node

        :type device:    PyDevice
        :param device:   network device object
        :type lb_node:      PyLbNode
        :param lb_node:     load balancer node object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        if 'Vendor.F5' not in device.tags:
            return {}

        subind = lb_node.encoded_oid_subindex

        if not subind:
            return {}

        var_dict = self.make_vars_using_var_hint(device, lb_node)

        mv = {
            'ltmNodeAddrStatusEnabledState': {
                'component': lb_node,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmNodeAddrStatusEnabledState.{0}'.format(subind)
            },

            'ltmNodeAddrStatusAvailState': {
                'component': lb_node,
                'snmp_oid': 'F5-BIGIP-LOCAL-MIB:ltmNodeAddrStatusAvailState.{0}'.format(subind)
            }
        }

        var_dict.update(mv)
        return var_dict
