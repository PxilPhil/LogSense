package org.example.converter;

import org.example.common.DataConverter;
import org.example.common.ListToStringConverter;
import org.example.model.ApplicationData;
import org.example.model.ResourcesData;

import java.util.List;

public class CSVDataConverter implements DataConverter {
    public String convertApplicationData(long timestamp, List<ApplicationData> applicationData) {
        StringBuilder csv = new StringBuilder();
        csv.append("timestamp,contextSwitches,majorFaults,bytesRead,bytesWritten,kernelTime,minorFaults,name,path,residentSetSize,upTime,user,userTime,eventHeader,cpu,state");

        for (ApplicationData application : applicationData) {
            csv.append("\n");
            csv.append(timestamp).append(",");
            csv.append(application.getContextSwitches()).append(",");
            csv.append(application.getMajorFaults()).append(",");
            csv.append(application.getBytesRead()).append(",");
            csv.append(application.getBytesWritten()).append(",");
            csv.append(application.getKernelTime()).append(",");
            csv.append(application.getMinorFaults()).append(",");
            csv.append(application.getName()).append(",");
            csv.append(application.getPath()).append(",");
            csv.append(application.getResidentSetSize()).append(",");
            csv.append(application.getUpTime()).append(",");
            csv.append(application.getUser()).append(",");
            csv.append(application.getUserTime()).append(",");
            csv.append(application.getProcessCountDifference()).append(",");
            csv.append(application.getCpuUsage()).append(",");
            csv.append(application.getState());
        }
        return csv.toString();
    }

    @Override
    public String convertResourceData(long timestamp, ResourcesData resourcesData) {
        ListToStringConverter<Long> longListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<Boolean> booleanListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<Double> doubleListToStringConverter = new ListToStringSpacesConverter<>();

        StringBuilder csv = new StringBuilder();
        csv.append("timestamp,freeDiskSpace,readBytesDiskStores,readsDiskStores,writeBytesDiskStores,writesDiskStores,partitionsMajorFaults,partitionsMinorFaults,availableMemory,bytesReceivedNetworkInterfaces,bytesSentNetworkInterfaces,collisionsNetworkInterfaces,packetsReceivedNetworkInterfaces,packetsSentNetworkInterfaces,chargingPowerSources,dischargingPowerSources,powerOnLinePowerSources,powerUsageRatePowerSources,remainingCapacityPercentPowerSources,contextSwitchesProcessor,interruptsProcessor\n");

        csv.append(timestamp).append(",");

        csv.append(resourcesData.getFreeDiskSpace()).append(",");

        csv.append(longListToStringConverter.convert(resourcesData.getDiskStoresReadBytes())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getDiskStoresReads())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getDiskStoresWriteBytes())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getDiskStoresWrites())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getPartitionsMajorFaults())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getPartitionsMinorFaults())).append(",");

        csv.append(resourcesData.getAvailableMemory()).append(",");

        csv.append(longListToStringConverter.convert(resourcesData.getNetworkInterfacesBytesReceived())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getNetworkInterfacesBytesSent())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getNetworkInterfacesCollisions())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getNetworkInterfacesPacketsReceived())).append(",");
        csv.append(longListToStringConverter.convert(resourcesData.getNetworkInterfacesPacketsSent())).append(",");

        csv.append(booleanListToStringConverter.convert(resourcesData.getPowerSourcesCharging())).append(",");
        csv.append(booleanListToStringConverter.convert(resourcesData.getPowerSourcesDischarging())).append(",");
        csv.append(booleanListToStringConverter.convert(resourcesData.getPowerSourcesPowerOnLine())).append(",");
        csv.append(doubleListToStringConverter.convert(resourcesData.getPowerSourcesPowerUsageRate())).append(",");
        csv.append(doubleListToStringConverter.convert(resourcesData.getPowerSourcesRemainingCapacityPercent())).append(",");

        csv.append(resourcesData.getProcessorContextSwitches()).append(",");
        csv.append(resourcesData.getProcessorInterrupts());
        return csv.toString();
    }
}
