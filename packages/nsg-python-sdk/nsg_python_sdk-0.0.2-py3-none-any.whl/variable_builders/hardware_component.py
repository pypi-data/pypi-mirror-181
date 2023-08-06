"""
Copyright (C) 2022 HappyGears - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly
prohibited. Proprietary and confidential

DO NOT MODIFY ! This file is part of the distribution and may
change in the future versions.

"""

from net.happygears.nw2.py import MonitoringDataType
from net.happygears.nw2.py.py_wrappers import PyComponent
from net.happygears.nw2.py.py_wrappers import PyDevice

from variable_builders.base_variable_builder import BaseVariableBuilder


class HWComponentVariableBuilder(BaseVariableBuilder):
    """
    This class is used to build monitoring variables for chassis alarms.
    We create an object of this class and call its method `make_variable()`
    for all fixtures and all interfaces. If you need to add, remove or
    modify monitoring variables, create your own class based on this
    and overwrite method `make_variable()` in it.
    """

    def __init__(self, log):
        super(HWComponentVariableBuilder, self).__init__(log)

    def make_variable_index(self, device, component):
        """
        Given device and h/w component objects, return a number that
        can identify the component within the device. This may depend
        on the device vendor and nature of the component

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return:         a number
        """
        if component.index:
            return int(component.index)
        elif 'Vendor.Juniper' in device.tags:
            comps = component.oid.split('.')
            # I fully admit this is a strange way to compute index from Juniper's 4-part h/w component
            # index but this is what was used in the previous versions of the Java code and some
            # customers already have variables defined by this index.
            return int(comps[-1]) + int(comps[-2]) * 256 + int(comps[-3]) * 256 + int(comps[-4]) * 256
        else:
            return int(component.oid.split('.')[-1])

    def make_vars_using_var_hint(self, device, component):
        """
        Build monitoring variable for the HardwareComponent object that provides
        "hint", that is, call to component.getComponent().getMonitoringVariableHint() returns
        non-empty string. Returned value is the name of "suggested" monitoring
        variable that can get its value from the OID of this component.

        Many fixtures respond to the OID ENTITY-STATE-MIB::entStateOper for their
        hardware components, such as modules, bays, slots, ports, etc. This OID
        can be useful to monitor operational state of the component, however,
        on big fixtures this adds lots of monitoring variables. Since we can not
        predict whether the operator wants to monitor operational state of all
        hardware components this way, creation of these variables is disabled by default.
        To enable, override variable self.make_ent_state_oper_vars.

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        var_name = component.var_hint
        if var_name and component.oid and component.index:
            var = {
                'snmp_oid': component.oid,
                'component': component,
                'index': component.index
            }
            if component.data_type == 'String':
                var['type'] = MonitoringDataType.String

            return {var_name: var}
        else:
            return {}

    def make_pdu_vars(self, device, component):
        """
        Make variables for PDUs

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)
        name = component.name.lower()
        descr = component.description.lower()

        if 'Vendor.APC' in component.tags:
            if 'bank' in name:
                return {
                    'pduAPCBankLoad': {
                        'snmp_oid': component.oid,
                        'component': component,
                        'index': self.make_variable_index(device, component),
                    }
                }

            if 'phase' in name:
                return {
                    'pduAPCPhaseLoad': {
                        'snmp_oid': component.oid,
                        'component': component,
                        'index': self.make_variable_index(device, component),
                    }
                }

        if 'Vendor.ServerTech' in component.tags:
            # We only monitor tower status for Sentry PDU tower components
            if 'tower' in name and 'status' in descr:
                return {
                    'pduSentryTowerStatus': {
                        'snmp_oid': component.oid,
                        'component': component,
                        'index': self.make_variable_index(device, component),
                    }
                }

            if 'infeed' in name:
                return {
                    'pduSentryInFeedLoad': {
                        'snmp_oid': component.oid,
                        'component': component,
                        'index': self.make_variable_index(device, component),
                    }
                }
        return {}

    def make_psu_vars(self, device, component):
        """
        Make variables for Power Supply status monitoring.

        In the end, we want a variable to track PSU "operational state". Not all vendors provide
        OID that can be used to get that directly though. If such OID is available, we use it
        and create monitoring variable 'psuState' with it. When an OID like this is not available,
        we create vendor-specific variable with the name matching the OID and then post-process
        the information in nw2rules.py to get equivalent of psuState

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)
        if 'Vendor.Cisco' in component.tags and '1.3.6.1.4.1.9.9.117.1.1.2' in component.oid:
            # this is Cisco and the oid is from CISCO-ENTITY-FRU-CONTROL-MIB:cefcFRUPowerStatusTable
            return {
                'ciscoEntFruControlPowerStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Cisco' in component.tags and '1.3.6.1.4.1.9.9.13.1' in component.oid:
            # this is Cisco and the oid is from CISCO-ENVMON-MIB
            return {
                'ciscoEnvMonSupplyState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Arista' in component.tags and 'input current sensor' in component.name.lower():
            return {
                'aristaPSUInputCurrentSensor': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Juniper' in component.tags:
            return {
                'jnxPSUOperatingState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.F10' in component.tags and '1.3.6.1.4.1.6027.3.26.1.4' in component.oid:
            # this is F10 that supports DELL-NETWORKING-CHASSIS-MIB, oid is dellNetPowerSupplyOperStatus
            return {
                'dellPSUOperatingState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Brocade' in component.tags and '1.3.6.1.4.1.1588.2.1.1.1.1.22.1.3' in component.oid:
            # Brocade device that supports their SYSTEM-MIB
            return {
                'brcdPSUSwSensorStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.CumulusLinux' in component.tags and component.component_class == 'powerSupply':
            return {
                'cumulusLinuxPSUOperStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Viptela' in component.tags and '1.3.6.1.4.1.41916.3.1.2.1.4' in component.oid:
            return {
                'viptelaPsuStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        return {}

    def make_fan_vars(self, device, component):
        """
        Make variables for Fan status monitoring

        In the end, we want a variable to track fan "operational state". Not all vendors provide
        OID that can be used to get that directly though. If such OID is available, we use it
        and create monitoring variable 'fanState' with it. When an OID like this is not available,
        we create vendor-specific variable with the name matching the OID and then post-process
        the information in nw2rules.py to get equivalent of fanState

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)
        if 'Vendor.Cisco' in component.tags and '1.3.6.1.4.1.9.9.117.1.4.1' in component.oid:
            # this is Cisco and the oid is from CISCO-ENTITY-FRU-CONTROL-MIB:cefcFanTrayStatusTable
            return {
                'ciscoEntFruControlFanStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Cisco' in component.tags and '1.3.6.1.4.1.9.9.13.1' in component.oid:
            # this is Cisco and the oid is from CISCO-ENVMON-MIB
            return {
                'ciscoEnvMonFanState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Arista' in component.tags and 'Fan' in component.name and 'Sensor' in component.name:
            return {
                'aristaFanSensor': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Juniper' in component.tags:
            return {
                'jnxFanOperatingState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.F10' in component.tags and '1.3.6.1.4.1.6027.3.26.1.4' in component.oid:
            # this is F10 that supports DELL-NETWORKING-CHASSIS-MIB, oid is dellNetFanTrayOperStatus
            return {
                'dellFanOperatingState': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Brocade' in component.tags and '1.3.6.1.4.1.1588.2.1.1.1.1.22.1.3' in component.oid:
            # Brocade device that supports their SYSTEM-MIB
            return {
                'brcdFanSwSensorStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.CumulusLinux' in component.tags and component.component_class == 'fan':
            return {
                'cumulusLinuxFanOperStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }
        if 'Vendor.Viptela' in component.tags and '1.3.6.1.4.1.41916.3.1.2.1.4' in component.oid:
            return {
                'viptelaFanStatus': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index
                }
            }

        # if 'Vendor.CumulusLinux' in component.tags and 'Fan' in component.name and component.sensor_data_type == 'rpm':
        #     return {
        #         'cumulusLinuxFanSensor': {
        #             'snmp_oid': component.oid,
        #             'component': component,
        #             'index': component.index
        #         }
        #     }

        return {}

    def make_cpu_vars(self, device, component):
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)

        if 'Vendor.Viptela' in component.tags and component.index and '1.3.6.1.4.1.41916.11.1.16.0' in component.oid:
            # fix monitoring type because device responds with variable type OCTET STRING
            return {
                'viptelaCpuIdlePercent': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': component.index,
                    'type': MonitoringDataType.Double
                }
            }

        var_dict = self.make_vars_using_var_hint(device, component)

        if var_dict:
            return var_dict
        elif component.oid:
            return {
                'cpuUtil': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': self.make_variable_index(device, component),
                }
            }
        else:
            return {}

    def make_memory_vars(self, device, component):
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)
        if 'Vendor.Viptela' in component.tags and component.index and '1.3.6.1.4.1.41916.11.1' in component.oid:
            # fix monitoring type because device responds with variable type OCTET STRING
            return {
                'viptelaSystemStatusMemTotal': {
                    'snmp_oid': 'VIPTELA-OPER-SYSTEM:systemStatusMemTotal.0',
                    'component': component,
                    'index': component.index,
                    'type': MonitoringDataType.Double
                },
                'viptelaSystemStatusMemFree': {
                    'snmp_oid': 'VIPTELA-OPER-SYSTEM:systemStatusMemFree.0',
                    'component': component,
                    'index': component.index,
                    'type': MonitoringDataType.Double
                },
                'viptelaSystemStatusMemUsed': {
                    'snmp_oid': 'VIPTELA-OPER-SYSTEM:systemStatusMemUsed.0',
                    'component': component,
                    'index': component.index,
                    'type': MonitoringDataType.Double
                }
            }

        return self.make_vars_using_var_hint(device, component)

    def make_temp_vars(self, device, component):
        assert isinstance(device, PyDevice)
        assert isinstance(component, PyComponent), type(component)
        product_name = device.product_name
        #
        # print('####  device={0}, product_name={1}, comp.name={2}'.format(device.name, product_name, component.name))
        #
        if 'Vendor.Cisco' in device.tags and 'cevChassisN' in product_name and 'Ethernet' in component.name:
            #
            # this is a Cisco Nexus switch. Examples of model names:
            # cevChassisN7Kc7010
            # cevChassisN3KC3172PQ10GE
            # cevChassisN7Kc7009
            # On these, 'Ethernet 1/1 Transceiver Temperature Sensor' is in 1/1000 of a degree Celsius
            #
            # query to test:
            #
            # SELECT device,component,Model,tslast(metric) as temperature FROM tempSensor WHERE Vendor="Cisco" ORDER BY temperature DESC'
            #
            # Other components on the same Cisco switch report
            #
            return {
                'tempSensor': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': self.make_variable_index(device, component),
                    'scale': 0.001
                }
            }
        else:
            return {
                'tempSensor': {
                    'snmp_oid': component.oid,
                    'component': component,
                    'index': self.make_variable_index(device, component),
                }
            }

    def make_variables(self, device, component):
        """
        Given device and h/w component objects, build set of monitoring variables
        for the component

        :type device: PyDevice
        :param device:   network device object
        :type component: PyHardwareComponent
        :param component:     h/w component object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice), type(component)
        assert isinstance(component, PyComponent), type(component)

        # if device.name == 'mtag1':
        #     self.log.info('+++ Device: ' + device.name + ' component: ' + component.name)

        component_class = component.component_class
        data_type = component.sensor_data_type
        name_lowercase = component.name.lower()

        # print('#### device={0} component={1} component_class={2} data_type={3}'.format(device.name, component.name, component_class, data_type))

        if component_class == 'pdu':
            return self.make_pdu_vars(device, component)

        # elif component_class == 'opticalTransceiver':
        #     return self.make_transceiver_vars(device, component)

        # elif not component.oid:
        #     return {}

        elif component_class == 'cpu':
            return self.make_cpu_vars(device, component)

        elif component_class == 'memory':
            return self.make_memory_vars(device, component)

        var_dict = self.make_vars_using_var_hint(device, component)
        if var_dict:
            return var_dict

        if component_class == 'sensor' and data_type == 'celsius':
            return self.make_temp_vars(device, component)

        elif component_class == 'powerSupply':
            return self.make_psu_vars(device, component)

        elif 'Vendor.Arista' in component.tags and 'input current sensor' in component.name:
            return self.make_psu_vars(device, component)

        elif component_class == 'fan':
            return self.make_fan_vars(device, component)

        elif 'Vendor.Arista' in component.tags and 'Fan' in component.name and 'Sensor' in component.name:
            # "Fan Tray 2 Fan 1 Sensor 1"
            return self.make_fan_vars(device, component)

        return {}
