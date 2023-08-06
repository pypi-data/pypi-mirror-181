
from net.happygears.nw2.py import MonitoringDataType
from net.happygears.nw2.py.py_wrappers import PyAwsResource
from net.happygears.nw2.py.py_wrappers import PyDevice
from variable_builders.hardware_component import HWComponentVariableBuilder

EC2_INSTANCE_NS = "AWS/EC2"
DISKS_NS = "AWS/EBS"
LB_NS = "AWS/NetworkELB"
CLASSIC_LB_NS = "AWS/ELB"
SYSTEM_LINUX_NS = "System/Linux"

METRIC_VARS = {
    # disks
    ("%s/VolumeReadBytes" % DISKS_NS):                           "diskIOBytesReadRate",
    ("%s/VolumeTotalReadTime" % DISKS_NS):                       "diskIOReadsRate",
    ("%s/VolumeWriteOps" % DISKS_NS):                            "diskIOWritesRate",
    ("%s/VolumeWriteBytes" % DISKS_NS):                          "diskIOBytesWritesRate",
    ("%s/BurstBalance" % DISKS_NS):                              "diskBurstBalance",
    ("%s/VolumeIdleTime" % DISKS_NS):                            "diskIdleTime",
    ("%s/VolumeReadOps" % DISKS_NS):                             "diskReadOps",
    ("%s/VolumeTotalWriteTime" % DISKS_NS):                      "diskTotalWriteTime",
    # ec2
    ("%s/NetworkIn" % EC2_INSTANCE_NS):                          "networkIn",
    ("%s/MemoryUtilization" % EC2_INSTANCE_NS):                  "memUtilization",
    ("%s/DiskSpaceUtilization" % EC2_INSTANCE_NS):               "diskSpaceUtilization",
    ("%s/EBSWriteBytes" % EC2_INSTANCE_NS):                      "diskIOWritesBytesRate",
    ("%s/StatusCheckFailed_Instance" % EC2_INSTANCE_NS):         "instanceStatusCheckFailed",
    ("%s/NetworkPacketsIn" % EC2_INSTANCE_NS):                   "networkPacketsIn",
    ("%s/EBSWriteOps" % EC2_INSTANCE_NS):                        "dataDiskWritesRate",
    ("%s/StatusCheckFailed_System" % EC2_INSTANCE_NS):           "systemStatusCheckFailed",
    ("%s/NetworkPacketsOut" % EC2_INSTANCE_NS):                  "networkPacketsOut",
    ("%s/EBSReadBytes" % EC2_INSTANCE_NS):                       "dataDiskReadBytesRate",
    ("%s/MetadataNoToken" % EC2_INSTANCE_NS):                    "metadataNoToken",
    ("%s/CPUUtilization" % EC2_INSTANCE_NS):                     "cpuUtilization",
    # linux
    ("%s/DiskSpaceAvailable" % SYSTEM_LINUX_NS):                 "availableDiskSpace",
    ("%s/DiskSpaceUtilization" % SYSTEM_LINUX_NS):               "diskSpaceUtilization",
    ("%s/MemoryUtilization" % SYSTEM_LINUX_NS):                  "memoryUtilization",
    # lb
    ("%s/ProcessedBytes" % LB_NS):                               "processedBytes",
    ("%s/ProcessedPackets" % LB_NS):                             "processedPackets",
    ("%s/ConsumedLCUs_TCP" % LB_NS):                             "TCPConsumedLCUs",
    ("%s/ProcessedBytes_TCP" % LB_NS):                           "processedBytes",
    ("%s/PeakPacketsPerSecond" % LB_NS):                         "peakPacketsPerSecond",
    ("%s/TCP_Client_Reset_Count" % LB_NS):                       "clientResetCount",
    ("%s/NewFlowCount" % LB_NS):                                 "flowCount",
    ("%s/TCP_Target_Reset_Count" % LB_NS):                       "targetResetCount",
    ("%s/UnHealthyHostCount" % LB_NS):                           "unHealthyHostCount",
    ("%s/ActiveFlowCount_TCP" % LB_NS):                          "activeFlowCount",
    ("%s/ConsumedLCUs" % LB_NS):                                 "consumedLCUs",
    ("%s/PortAllocationErrorCount" % LB_NS):                     "portAllocationErrorCount",
    ("%s/HealthyHostCount" % LB_NS):                             "healthyHostCount",
    #classic lb
    ("%s/HTTPCode_Backend_2XX" % CLASSIC_LB_NS):                  "backendCode",
    ("%s/UnHealthyHostCount" % CLASSIC_LB_NS):                    "unHealthyHostCount",
    ("%s/EstimatedALBActiveConnectionCount" % CLASSIC_LB_NS):     "activeConnectionCount",
    ("%s/EstimatedProcessedBytes" % CLASSIC_LB_NS):               "estimatedProcessedBytes",
    ("%s/Latency" % CLASSIC_LB_NS):                               "latency",
    ("%s/HTTPCode_Backend_4XX" % CLASSIC_LB_NS):                  "backendCode4",
    ("%s/EstimatedALBNewConnectionCount" % CLASSIC_LB_NS):        "newConnectionCount",
    ("%s/HealthyHostCount" % CLASSIC_LB_NS):                      "healthyHostCount",
    ("%s/RequestCount" % CLASSIC_LB_NS):                          "requestCount",
    ("%s/EstimatedALBConsumedLCUs" % CLASSIC_LB_NS):              "consumedLCUs",
    ("%s/SurgeQueueLength" % CLASSIC_LB_NS):                      "surgeQueueLength",
}


class AwsResourceVariableBuilder(HWComponentVariableBuilder):

    def __init__(self, log):
        super(AwsResourceVariableBuilder, self).__init__(log)

    def make_aws_resource_variables(self, device, component):
        """
        Make monitoring variables for the aws resource

        :type device:         PyDevice
        :param device:        network device object
        :type component:      PyAwsResource
        :param component:     AwsResourceMetrics object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        mvars = {}

        index = component.getComponent().index
        metric_definitions = component.metric_definitions
        for metric_name in metric_definitions:
            metric_namespace = metric_definitions[metric_name].namespace
            var_name_key = metric_namespace + "/" + metric_name
            if var_name_key in METRIC_VARS.keys():
                var_name = METRIC_VARS[var_name_key]
                mvars[var_name] = {
                    'index': index,
                    'component': component,
                    'metric_name': metric_name,
                    'type': MonitoringDataType.Double
                }

        return mvars

    def make_variables(self, device, component):
        """
        Given device and h/w component objects, build set of monitoring variables
        for the component

        :type device:         PyDevice
        :param device:        network device object
        :type component:      PyHardwareComponent
        :param component:     PyVirtualServer or PyServerPool object
        :return: a dictionary where the key is variable name and value is another dictionary
        """
        assert isinstance(device, PyDevice)

        if isinstance(component, PyAwsResource):
            return self.make_aws_resource_variables(device, component)
        else:
            return {}