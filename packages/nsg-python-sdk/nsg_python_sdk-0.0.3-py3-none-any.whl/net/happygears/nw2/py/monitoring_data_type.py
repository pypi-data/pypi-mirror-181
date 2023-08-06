from enum import Enum


class MonitoringDataType(Enum):
    Unknown = 0
    Counter = 1
    Counter64 = 2
    Gauge = 3
    TimeTick = 4
    Int = 5
    Unsigned = 6
    Double = 7
    String = 8  # any kind of textual information (e.g. ifAlias)
    HexString = 9  # hex number as a string (e.g. dot3adAggPortActorOperState)

    @staticmethod
    def reverse(val):
        try:
            return MonitoringDataType(val)
        except ValueError:
            return MonitoringDataType.Unknown
