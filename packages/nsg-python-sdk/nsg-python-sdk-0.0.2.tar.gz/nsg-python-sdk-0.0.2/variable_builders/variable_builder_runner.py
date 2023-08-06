"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly
prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution and may
change in the future versions.

"""

# NSG.DataSource is a protobuf, it does not change when we move to Python3, but maybe we need to import it
# differently
from net.happygears.proto.NSG_pb2 import DataSource

from variable_builders import AzureResourceVariableBuilder
from variable_builders import ChassisAlarmVariableBuilder
from variable_builders import DeviceVariableBuilder
from variable_builders import FwCounterVariableBuilder
from variable_builders import HWComponentVariableBuilder
from variable_builders import InterfaceVariableBuilder
from variable_builders import IpsecTunnelVariableBuilder
from variable_builders import LoadBalancerVariableBuilder
from variable_builders import MplsTunnelVariableBuilder
from variable_builders import ProtocolDescriptorVariableBuilder
from variable_builders import VpnDeviceVariableBuilder
from variable_builders import AwsResourceVariableBuilder


def merge_into(target_mvar_dir, mvar_dir):
    """

    :param target_mvar_dir:  a dict of lists. Key is variable name
    :param mvar_dir:  a dictionary where the key is variable name and value is dict. that describes variable instance
    """
    for key, vd in list(mvar_dir.items()):
        if key not in target_mvar_dir:
            target_mvar_dir[key] = []
        target_mvar_dir[key].append(mvar_dir[key])


def make_vars(dsc_value, components, mvars, func):
    for comp in components:
        variables = func(comp)
        # add reference to corresponding DataSource value
        for v in list(variables.values()):
            v['dsc'] = dsc_value
        merge_into(mvars, variables)


class VariableBuilder(object):
    """
    Monitoring variable descriptors are created by the actual builder classes
    `DeviceVariableBuilder`, `HWComponentVariableBuilder`, `ProtocolDescriptorVariableBuilder`
    and others.

    :param log: Java logger object. Call it using self.log.info("log message")
    """

    def __init__(self, log):
        self.log = log
        self.device = DeviceVariableBuilder(log)
        self.interface = InterfaceVariableBuilder(log)
        self.hw_components = HWComponentVariableBuilder(log)
        self.protocols = ProtocolDescriptorVariableBuilder(log)
        self.chassis_alarms = ChassisAlarmVariableBuilder(log)
        self.mpls_tunnels = MplsTunnelVariableBuilder(log)
        self.fw_counters = FwCounterVariableBuilder(log)
        self.lb = LoadBalancerVariableBuilder(log)
        self.vpn = VpnDeviceVariableBuilder(log)
        self.ipsec_tunnels = IpsecTunnelVariableBuilder(log)
        self.azure_resources = AzureResourceVariableBuilder(log)
        self.aws_resources = AwsResourceVariableBuilder(log)

    def execute(self, device):
        """
        Generate variables for `device`

        :param device:   PyDevice object
        :return: a dictionary where the key is variable name and value is list of dictionaries, each
                 describing one monitoring variable, all of it for one device
        """
        # this is a dict of lists
        mvars = {}
        dv = DeviceVariableBuilder(self.log).make_variables(device)
        for v in list(dv.values()):
            v['dsc'] = DataSource.DS_Unknown
        merge_into(mvars, dv)

        make_vars(DataSource.DS_Interface, device.getPyInterfaces(), mvars,
                  lambda c: self.interface.make_variables(device, c))
        make_vars(DataSource.DS_GenericHardwareComponent, device.getPyHardwareComponents(), mvars,
                  lambda c: self.hw_components.make_variables(device, c))
        make_vars(DataSource.DS_ProtocolDescriptor, device.getPyProtocolDescriptors(), mvars,
                  lambda c: self.protocols.make_variables(device, c))
        make_vars(DataSource.DS_ChassisAlarm, device.getPyChassisAlarms(), mvars,
                  lambda c: self.chassis_alarms.make_variables(device, c))
        make_vars(DataSource.DS_MplsTunnel, device.getPyMplsTunnels(), mvars,
                  lambda c: self.mpls_tunnels.make_variables(device, c))
        make_vars(DataSource.DS_FirewallCounter, device.getPyFwCounters(), mvars,
                  lambda c: self.fw_counters.make_variables(device, c))

        make_vars(DataSource.DS_VirtualServer, device.getPyVirtualServers(), mvars,
                  lambda c: self.lb.make_vserver_variables(device, c))
        make_vars(DataSource.DS_ServerPool, device.getPyServerPools(), mvars,
                  lambda c: self.lb.make_server_pool_variables(device, c))
        make_vars(DataSource.DS_LbNode, device.getPyLbNodes(), mvars,
                  lambda c: self.lb.make_lb_node_variables(device, c))

        make_vars(DataSource.DS_VpnControlConnection, device.getPyVpnControlConnections(), mvars,
                  lambda c: self.vpn.make_variables(device, c))

        make_vars(DataSource.DS_AzureResourceMetric, device.getPyAzureResources(), mvars,
                  lambda c: self.azure_resources.make_variables(device, c))
        make_vars(DataSource.DS_AwsResourceMetric, device.getPyAwsResources(), mvars,
                  lambda c: self.aws_resources.make_variables(device, c))

        # ipsec tunnels are an exception. We take information from an ipsec tunnel h/w
        # component object but associate variables with a tunnel interface. For this reason,
        # I set field `dsc=DataSource.DS_Interface`
        #
        make_vars(DataSource.DS_Interface, device.getPyIpsecTunnels(), mvars,
                  lambda c: self.ipsec_tunnels.make_variables(device, c))  # spec. case

        return mvars
