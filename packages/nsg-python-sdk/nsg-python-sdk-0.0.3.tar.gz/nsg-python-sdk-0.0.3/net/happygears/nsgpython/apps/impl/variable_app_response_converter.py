from functools import cmp_to_key

from net.happygears.proto.NSG_pb2 import DataType, DataSource, PollingVariable, PollingVariables, PollingVariableMap
from net.happygears.nw2.py import MonitoringDataType


def compare_instance(instance_1, instance_2):
    index1 = instance_1['index']
    index2 = instance_2['index']
    return (index1 > index2) - (index1 < index2)


class VariableAppResponseConverter:

    @staticmethod
    def convert(request_id, response_dict):
        polling_variables_map = PollingVariableMap()
        for key in sorted(response_dict):
            var_instance = response_dict[key]
            polling_variables = PollingVariables()
            for v_instance in sorted(var_instance, key=cmp_to_key(compare_instance)):
                polling_variable = VariableAppResponseConverter.convert_to_polling_variable(v_instance)
                polling_variables.variables.append(polling_variable)
            polling_variables_map.polling_variables[key].CopyFrom(polling_variables)
        return polling_variables_map

    @staticmethod
    def convert_to_polling_variable(var_instance):
        name = var_instance.get('name', '')
        index = var_instance.get('index', 0)
        scale = var_instance.get('scale', float(1.0))
        if not scale or scale == 0:
            scale = float(1.0)

        mon_data_type = var_instance.get('type', MonitoringDataType.Unknown)
        data_type = mon_data_type.value
        dsc = var_instance.get('dsc', DataSource.DS_Unknown)
        snmp_walk_oid = var_instance.get('snmp_walk_oid', '')
        snmp_oid = var_instance.get('snmp_oid', '')
        metric_name = var_instance.get('metric_name', '')

        polling_variable = PollingVariable()
        polling_variable.index = index
        polling_variable.component_name = name
        polling_variable.data_type = data_type
        polling_variable.sensor_scale = scale
        polling_variable.dsc = dsc
        polling_variable.metric_name = metric_name
        if snmp_walk_oid:
            polling_variable.OID = snmp_walk_oid
            polling_variable.SNMP_walk = True
        else:
            polling_variable.OID = snmp_oid

        return polling_variable
