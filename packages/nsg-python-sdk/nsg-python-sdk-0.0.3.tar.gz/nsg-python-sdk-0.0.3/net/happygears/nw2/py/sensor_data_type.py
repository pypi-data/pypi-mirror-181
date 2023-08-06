from enum import Enum


class SensorDataType(Enum):
    other = 1
    unknown = 2
    voltsAC = 3
    voltsDC = 4
    amperes = 5
    watts = 6
    hertz = 7
    celsius = 8
    percentRH = 9
    rpm = 10
    cmm = 11
    truthvalue = 12
    specialEnum = 13
    dBm = 14

    @staticmethod
    def reverse(val):
        try:
            return SensorDataType(val)
        except ValueError as ve:
            return SensorDataType.unknown
