"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium
is strictly prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution
and may change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyDevice

from variable_builders.hardware_component import HWComponentVariableBuilder


class VpnDeviceVariableBuilder(HWComponentVariableBuilder):

    def __init__(self, log):
        super(VpnDeviceVariableBuilder, self).__init__(log)

    def make_control_connection_variables(self, device, component):
        """
        Make monitoring variables for the control connection

        :type device:    PyDevice
        :param device:   network device object
        :type component:      PyVpnControlConnection
        :param component:     control connection object
        :return: a dictionary where the key is variable name and value is another dictionary
        """

        return {}

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
        return self.make_control_connection_variables(device, component)

