from enum import Enum


class HardwareComponentClass(Enum):
    other = 1
    unknown = 2
    chassis = 3
    backplane = 4
    container = 5
    powerSupply = 6
    fan = 7
    sensor = 8
    module = 9
    port = 10
    stack = 11
    cpu = 12
    opticalTransceiver = 13
    chassisAlarm = 14
    pdu = 15
    disk = 16
    memory = 17
    counter = 18
    virtServer = 19
    serverPool = 20
    tunnel = 21
    protocol = 22
    lbNode = 23
    fru = 24

    @staticmethod
    def reverse(val):
        try:
            return HardwareComponentClass(val)
        except ValueError:
            return HardwareComponentClass.unknown
