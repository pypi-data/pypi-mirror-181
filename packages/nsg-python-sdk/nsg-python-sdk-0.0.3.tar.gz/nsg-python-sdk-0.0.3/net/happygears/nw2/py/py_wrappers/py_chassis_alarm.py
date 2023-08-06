from net.happygears.proto.NSG_pb2 import Component
from .py_component import PyComponent


class PyChassisAlarm(PyComponent):
    def __init__(self, component: Component):
        super().__init__(component)

    @property
    def type(self):
        return self.getChassisAlarmType()

    def getChassisAlarmType(self):
        alarm_type = self.component.alarm_type
        if alarm_type == Component.AlarmType.at_minor:
            return 'minor'
        elif alarm_type == Component.AlarmType.at_major:
            return 'major'
        else:
            return 'unknown'
