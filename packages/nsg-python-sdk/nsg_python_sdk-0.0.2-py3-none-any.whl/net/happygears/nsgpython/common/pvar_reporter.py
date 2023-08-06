from sortedcontainers import SortedSet

from net.happygears.proto.NSG_pb2 import DataType, DataSource


class PVarReporter:
    def __init__(self, device):
        self.device = device
        res = SortedSet()
        for tag in device.tags:
            res.add(tag)

        self.sb = '\n'

        self.sb = '\nMonitoring variables report for the device {}\n\nTags:\n'.format(device.name)
        self.sb += '[' + ', '.join(res) + ']'
        self.sb += '\n\n\n'

    def getContents(self):
        return self.sb

    def add(self, pvars):
        for var_name in sorted(pvars.polling_variables.keys()):
            vars = pvars.polling_variables[var_name]
            for polling_variable in vars.variables:
                triplet = '{}.{}.{}'.format(var_name, self.device.id, polling_variable.index)
                self.sb += '%-40s | %-40s | %24s | %16s |  %10.1g | %c | %s\n' % (triplet,
                                                                                         polling_variable.component_name,
                                                                                         DataSource.Name(
                                                                                             polling_variable.dsc),
                                                                                         DataType.Name(
                                                                                             polling_variable.data_type),
                                                                                         polling_variable.sensor_scale,
                                                                                         'W' if polling_variable.SNMP_walk else ' ',
                                                                                         polling_variable.OID)
