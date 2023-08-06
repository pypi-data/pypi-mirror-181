"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyDevice
from net.happygears.nw2.py.py_wrappers import PyIpsecTunnel

from variable_builders.base_variable_builder import BaseVariableBuilder


class IpsecTunnelVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build IPSEC tunnel-related monitoring variables.
    """

    def __init__(self, log):
        super(IpsecTunnelVariableBuilder, self).__init__(log)

    def make_variables(self, device, tunnel):
        """
        Given device and IPSEC tunnel objects, build set of monitoring variables
        for the tunnel

        :type device:    PyDevice
        :param device:   network device object
        :type tunnel:    PyIpsedTunnel
        :param tunnel:   ipsec tunnel object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(tunnel, PyIpsecTunnel)

        if not tunnel.index:
            return {}

        intf = device.interfaces[tunnel.if_index]
        if intf is None:
            return {}

        # This uses fields `in_traffic_oid_index`, `out_traffic_oid_index` and `oper_status_oid_index`
        # in the :class:`PyIpsedTunnel` object. These fields are strings, the value is
        # an index in the table where corresponding OID is found. Passing just index rather
        # than whole OID from discoery provides for better flexibility in case user wants to
        # monitor another OID in the same table, e.g. packet counter in addition to the byte
        # counter. The downside is that code in Java classes that perform discovery of
        # IPSEC tunnels should be coordinated with this scritpt. We pass indexes from Java
        # via fields in underlying IpsecTunnel object but dont pass the name of the table
        # these indexes are for.
        #
        # In case of Cisco fixtures, indexes `in_traffic_oid_index`, `out_traffic_oid_index`
        # and `oper_status_oid_index` are for the table cipSecTunnelTable in CISCO-IPSEC-FLOW-MONITOR-MIB
        #
        # In case of Juniper fixtures, indexes `in_traffic_oid_index` and `out_traffic_oid_index`
        # are for the table jnxIpSecTunnelMonTable in JUNIPER-IPSEC-FLOW-MON-MIB and index
        # `oper_status_oid_index` is for the table  jnxIpSecSaMonTable in the same MIB
        #

        if 'Vendor.Cisco' in device.tags:
            return {
                'ifHCInOctets': {
                    'component': intf,
                    'snmp_oid': 'CISCO-IPSEC-FLOW-MONITOR-MIB:cipSecTunHcInOctets.{0}'.format(tunnel.in_traffic_oid_index)
                },
    
                'ifHCOutOctets': {
                    'component': intf,
                    'snmp_oid': 'CISCO-IPSEC-FLOW-MONITOR-MIB:cipSecTunHcOutOctets.{0}'.format(tunnel.out_traffic_oid_index)
                },

                'ifOperStatus': {
                    'component': intf,
                    'snmp_oid': 'CISCO-IPSEC-FLOW-MONITOR-MIB:cipSecTunIkeTunnelAlive.{0}'.format(tunnel.oper_status_oid_index)
                },
            }

        if 'Vendor.Juniper' in device.tags:
            return {
                'ifHCInOctets': {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IPSEC-FLOW-MON-MIB:jnxIpSecTunMonInDecryptedBytes.{0}'.format(tunnel.in_traffic_oid_index)
                },

                'ifHCOutOctets': {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IPSEC-FLOW-MON-MIB:jnxIpSecTunMonOutEncryptedBytes.{0}'.format(tunnel.out_traffic_oid_index)
                },

                'ifOperStatus': {
                    'component': intf,
                    'snmp_oid': 'JUNIPER-IPSEC-FLOW-MON-MIB:jnxIpSecSaMonState.{0}'.format(tunnel.oper_status_oid_index)
                },
            }

        return {}
