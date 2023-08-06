class HappyGearsOids:
    happyGearsInternalMonitoringOids = "1.3.6.1.4.1.44213.1"

    happyDeviceMonitoringOids = happyGearsInternalMonitoringOids + ".1"
    snmpTimeoutsOid = happyDeviceMonitoringOids + ".1"
    deviceMonitorFreeTimeOid = happyDeviceMonitoringOids + ".2"
    snmpRttOid = happyDeviceMonitoringOids + ".3"

    # this is the last time when we received _any_ data from the device. This includes both
    # real and NSG devices and should belong to its own separate category "Status" because it
    # is an amalgam (some times derived from SNMP polling, some times internally generated)
    lastContactTimeOid = happyDeviceMonitoringOids + ".4"

    icmpOids = happyDeviceMonitoringOids + ".5"

    icmpAvgRttOid = icmpOids + ".1"
    icmpMinRttOid = icmpOids + ".2"
    icmpMaxRttOid = icmpOids + ".3"
    icmpLossOid = icmpOids + ".4"
