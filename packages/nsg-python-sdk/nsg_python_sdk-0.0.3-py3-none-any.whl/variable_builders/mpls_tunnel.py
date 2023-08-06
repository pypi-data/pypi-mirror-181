"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyDevice
from net.happygears.nw2.py.py_wrappers import PyMplsTunnel

from variable_builders.base_variable_builder import BaseVariableBuilder


class MplsTunnelVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build MPLS tunnel-related monitoring variables.
    We create an object of this class and call its method `make_variables()`
    for all fixtures and all components. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variables()` in it.
    """

    def __init__(self, log):
        super(MplsTunnelVariableBuilder, self).__init__(log)

    def make_variables(self, device, tunnel):
        """
        Given device and MPLS tunnel objects, build set of monitoring variables
        for the tunnel

        :type device:    PyDevice
        :param device:   network device object
        :type tunnel:    PyMplsTunnel
        :param tunnel:   mpls tunnel object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(tunnel, PyMplsTunnel)

        subind = tunnel.encoded_oid_subindex

        if not tunnel.index or not subind:
            return {}

        return {
            'mplsLspInfoState': {
                'component': tunnel,
                'snmp_oid': 'MPLS-MIB:mplsLspInfoState.{0}'.format(subind)
            },

            'mplsLspInfoOctets': {
                'component': tunnel,
                'snmp_oid': 'MPLS-MIB:mplsLspInfoOctets.{0}'.format(subind)
            },

            'mplsLspInfoPackets': {
                'component': tunnel,
                'snmp_oid': 'MPLS-MIB:mplsLspInfoPackets.{0}'.format(subind)
            },

            'mplsLspLastPathChange': {
                'component': tunnel,
                'snmp_oid': 'MPLS-MIB:mplsLspInfoLastPathChange.{0}'.format(subind)
            },

            'mplsPathBandwidth': {
                'component': tunnel,
                'snmp_oid': 'MPLS-MIB:mplsPathInfoBandwidth.{0}'.format(subind)
            },

        }


