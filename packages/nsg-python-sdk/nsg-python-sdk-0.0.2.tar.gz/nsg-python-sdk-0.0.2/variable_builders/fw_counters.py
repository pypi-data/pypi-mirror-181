"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyDevice

from variable_builders.base_variable_builder import BaseVariableBuilder


class FwCounterVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build monitoring variables for firewall counters
    (both stateless ACL and stateful policy).
    We create an object of this class and call its method `make_variables()`
    for all fixtures and all AclComponent components. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variables()` in it.
    """

    def __init__(self, log):
        super(FwCounterVariableBuilder, self).__init__(log)

    def make_variables(self, device, component):
        """
        Given device and AclCounter objects, build set of monitoring variables
        for the counter

        :type device:    PyDevice
        :param device:   network device object
        :type component:    PyComponent object
        :param component:   fw counter object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        subind = component.encoded_oid_subindex

        if not subind:
            return {}

        # this is only supported for Juniper fixtures at the moment
        if 'Vendor.Juniper' in device.tags:
            return self.make_variables_jnpr(device, component)
        elif 'Vendor.Cisco' in device.tags:
            return self.make_variables_cisco(device, component)
        else:
            return {}

    def make_variables_jnpr(self, device, component):
        """
        Given device and FwCounter objects, build set of monitoring variables
        for the counter

        :type device:    PyDevice
        :param device:   network device object
        :type component:    PyComponent object
        :param component:   fw counter object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        subind = component.encoded_oid_subindex

        if 'jnxFWCounter' in component.getComponent().monitoring_variable_hint:
            return {
                'jnxFWCounterPacketCount': {
                    'snmp_oid': 'JUNIPER-FIREWALL-MIB:jnxFWCounterPacketCount.{0}'.format(subind),
                    'component': component
                },

                'jnxFWCounterByteCount': {
                    'snmp_oid': 'JUNIPER-FIREWALL-MIB:jnxFWCounterByteCount.{0}'.format(subind),
                    'component': component
                }
            }

        elif 'jnxJsPolicyStats' in component.getComponent().monitoring_variable_hint:
            return {
                'jnxJsPolicyStatsInputByteRate': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsInputByteRate.{0}'.format(subind),
                    'component': component
                },

                'jnxJsPolicyStatsOutputByteRate': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsOutputByteRate.{0}'.format(subind),
                    'component': component
                },

                'jnxJsPolicyStatsInputPacketRate': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsInputPacketRate.{0}'.format(subind),
                    'component': component
                },

                'jnxJsPolicyStatsOutputPacketRate': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsOutputPacketRate.{0}'.format(subind),
                    'component': component
                },

                'jnxJsPolicyStatsSessionRate': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsSessionRate.{0}'.format(subind),
                    'component': component
                },

                # jnxJsPolicyStatsNumSessions and jnxJsPolicyStatsSessionDeleted do not appear in GW, they
                # are used to calculate globalFwStatsSessionsActive.
                'jnxJsPolicyStatsNumSessions': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsNumSessions.{0}'.format(subind),
                    'component': component
                },

                'jnxJsPolicyStatsSessionDeleted': {
                    'snmp_oid': 'JUNIPER-JS-POLICY-MIB:jnxJsPolicyStatsSessionDeleted.{0}'.format(subind),
                    'component': component
                },
            }

        else:
            return {}

    def make_variables_cisco(self, device, component):
        """
        Given device and FWCounter objects, build set of monitoring variables
        for the counter

        :type device:    PyDevice
        :param device:   network device object
        :type component:    PyComponent object
        :param component:   fw counter object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        subind = component.encoded_oid_subindex

        if 'globalFwStatsConnSetupRate' == component.getComponent().monitoring_variable_hint:
            return {
                'globalFwStatsConnSetupRate': {
                    'snmp_oid': 'CISCO-UNIFIED-FIREWALL-MIB:cufwConnGlobalConnSetupRate1.{0}'.format(subind),
                    'component': component
                },
                'globalFwStatsSessionsActive': {
                    'snmp_oid': 'CISCO-UNIFIED-FIREWALL-MIB:cufwConnGlobalNumActive.{0}'.format(subind),
                    'component': component
                }
            }

        else:
            return {}
