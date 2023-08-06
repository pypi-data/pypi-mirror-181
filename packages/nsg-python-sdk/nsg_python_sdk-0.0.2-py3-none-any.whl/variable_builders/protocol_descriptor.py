"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly 
prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution and may 
change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyDevice
from net.happygears.nw2.py.py_wrappers import PyProtocolDescriptor

from variable_builders.base_variable_builder import BaseVariableBuilder


class ProtocolDescriptorVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build monitoring variables for protocols (OSPF and BGP4 at the moment).
    We create an object of this class and call its method `make_variable()`
    for all fixtures and all interfaces. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variable()` in it.
    """

    def __init__(self, log):
        super(ProtocolDescriptorVariableBuilder, self).__init__(log)

    def make_variables(self, device, protocol):
        """
        Given device and protocol descriptor objects, build set of monitoring variables
        for the protocol

        :type device: PyDevice
        :param device:   network device object
        :type protocol: PyProtocolDescriptor
        :param protocol:  protocol object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(protocol, PyProtocolDescriptor)

        name = protocol.getComponent().monitoring_variable_hint
        return {
            name: {
                'component': protocol,
                'snmp_oid': protocol.oid,
                # 'container': protocol.name,
            }
        }

