"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly 
prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution and may 
change in the future versions.

"""

from net.happygears.nw2.py.py_wrappers import PyChassisAlarm
from net.happygears.nw2.py.py_wrappers import PyDevice
from variable_builders.base_variable_builder import BaseVariableBuilder


class ChassisAlarmVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build monitoring variables for chassis alarms.
    We create an object of this class and call its method `make_variable()`
    for all fixtures and all interfaces. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variable()` in it.
    """

    def __init__(self, log):
        super(ChassisAlarmVariableBuilder, self).__init__(log)

    def make_variables(self, device, component):
        """
        Given device and chassis alarm objects, build set of monitoring variables
        for the chassis alarm.

        :type device: PyDevice
        :param device:   network device object
        :type component: PyChassisAlarm
        :param component:     chassis alarm object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyChassisAlarm)

        alarm_type = component.type

        # Treat Cisco chassis alarms differently because we need to process values
        # of corresponding monitoring variables to make them compatible with our
        #     "standard" minorChassisAlarm and majorChassisAlarm vars. minorChassisAlarm
        # and majorChassisAlarm count number of alarms that exist on the device, however
        # Cisco OIDs chassisMinorAlarm and chassisMajorAlarm return "alarm status" and
        # have value "1" when it is off and "2" when it is on. Function
        # normalize_cisco_chassis_alarm() in nw2rules converts it so that "0" meahs it
        # is off and "1" means it is on. Source monitoring variable should have different
        # name to make sure this correction does not happen twice when the system runs
        # in cluster configuration and the variable can be processed twice, first in
        # the secondary server and then in the primary
        #
        if 'Vendor.Cisco' in component.tags:
            if alarm_type == 'minor':
                name = 'ciscoMinorChassisAlarm'
            elif alarm_type == 'major':
                name = 'ciscoMajorChassisAlarm'
            else:
                name = alarm_type + 'ChassisAlarm'
            return {
                name: {
                    'name': 'Chassis',
                    'snmp_oid': component.oid,
                    'component': component,
                }}
        else:
            name = alarm_type + 'ChassisAlarm'
            return {
                name: {
                    'name': 'Chassis',
                    'snmp_oid': component.oid,
                    'component': component,
                }}
