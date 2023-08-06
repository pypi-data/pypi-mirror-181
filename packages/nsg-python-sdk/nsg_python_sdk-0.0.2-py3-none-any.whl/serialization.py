import copy

from google.protobuf import json_format, text_format

from net.happygears.proto.NSG_pb2 import Component
from net.happygears.proto.NSG_pb2 import Device
from net.happygears.proto.NSG_pb2 import Interface


class Serialization:
    @staticmethod
    def deserialize_device_json(ser):
        from net.happygears.nw2.py.py_wrappers.py_device import PyDevice

        device = Device()
        json_format.Parse(ser, device)
        return PyDevice(device)

    @staticmethod
    def deserialize_device_pb(ser):
        from net.happygears.nw2.py.py_wrappers.py_device import PyDevice

        device = Device()
        text_format.Parse(ser, device)
        return PyDevice(device)

    @staticmethod
    def serialize_device_json(device):
        new_device = Serialization.rebuild(device)
        return json_format.MessageToJson(new_device, including_default_value_fields=True, sort_keys=True)

    @staticmethod
    def serialize_device_pb(device):
        new_device = Serialization.rebuild(device)
        return text_format.MessageToString(new_device)

    @staticmethod
    def rebuild(device):
        new_device = copy.deepcopy(device.node)
        del new_device.tags[:]
        new_device.tags.extend(device.tags)

        new_device.ClearField('interfaces')
        for py_network_interface in device.getPyInterfaces():
            ni = Serialization.replace_interface_tags(py_network_interface)
            new_device.interfaces[ni.index].CopyFrom(ni)

        new_device.ClearField('firewall_counters')
        for comp in device.getPyFwCounters():
            nc = Serialization.replace_component_tags(comp)
            new_device.firewall_counters[nc.index].CopyFrom(nc)

        new_device.ClearField('hardware_components')
        for comp in device.getPyHardwareComponents():
            nc = Serialization.replace_component_tags(comp)
            new_device.hardware_components.append(nc)

        new_device.ClearField('chassis_alarms')
        for comp in device.getPyChassisAlarms():
            nc = Serialization.replace_component_tags(comp)
            new_device.chassis_alarms.append(nc)

        new_device.ClearField('protocol_descriptors')
        for comp in device.getPyProtocolDescriptors():
            nc = Serialization.replace_component_tags(comp)
            new_device.protocol_descriptors.append(nc)

        new_device.ClearField('MPLS_tunnels')
        for comp in device.getPyMplsTunnels():
            nc = Serialization.replace_component_tags(comp)
            new_device.MPLS_tunnels[nc.index].CopyFrom(nc)

        new_device.ClearField('ipsec_tunnels')
        for comp in device.getPyIpsecTunnels():
            nc = Serialization.replace_component_tags(comp)
            new_device.ipsec_tunnels[nc.index].CopyFrom(nc)

        new_device.ClearField('virtual_servers')
        for comp in device.getPyVirtualServers():
            nc = Serialization.replace_component_tags(comp)
            new_device.virtual_servers[nc.index].CopyFrom(nc)

        new_device.ClearField('server_pools')
        for comp in device.getPyServerPools():
            nc = Serialization.replace_component_tags(comp)
            new_device.server_pools[nc.index].CopyFrom(nc)

        new_device.ClearField('load_balancers')
        for comp in device.getPyLbNodes():
            nc = Serialization.replace_component_tags(comp)
            new_device.load_balancers[nc.index].CopyFrom(nc)

        new_device.ClearField('vpn_control_connections')
        for comp in device.getPyVpnControlConnections():
            nc = Serialization.replace_component_tags(comp)
            new_device.vpn_control_connections[nc.index].CopyFrom(nc)

        new_device.ClearField('ephemeral_components')
        for comp in device.getPyEphemeralComponents():
            nc = Serialization.replace_component_tags(comp)
            new_device.ephemeral_components.append(nc)

        new_device.ClearField('azure_resources')
        for comp in device.getPyAzureResources():
            nc = Serialization.replace_component_tags(comp)
            new_device.azure_resources[nc.index].CopyFrom(nc)

        new_device.ClearField('aws_resources')
        for comp in device.getPyAwsResources():
            nc = Serialization.replace_component_tags(comp)
            new_device.aws_resources[nc.index].CopyFrom(nc)

        return new_device

    @staticmethod
    def replace_interface_tags(comp):
        nc = Interface()
        nc.MergeFrom(comp.intf)
        nc.ClearField('tags')
        nc.tags.extend(comp.tags)
        return nc

    @staticmethod
    def replace_component_tags(comp):
        nc = Component()
        nc.MergeFrom(comp.component)
        nc.ClearField('tags')
        nc.tags.extend(comp.tags)
        return nc
