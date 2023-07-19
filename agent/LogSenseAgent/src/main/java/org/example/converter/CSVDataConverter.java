package org.example.converter;

import org.example.common.DataConverter;
import org.example.common.ListToStringConverter;
import org.example.model.*;

import java.net.InetAddress;
import java.util.Arrays;
import java.util.List;

public class CSVDataConverter implements DataConverter {
    @Override
    public String convertApplicationData(long timestamp, List<Application> applicationData) {
        StringBuilder csv = new StringBuilder();
        csv.append("timestamp|contextSwitches|majorFaults|bitness|commandLine|currentWorkingDirectory|name|openFiles|parentProcessID|path|residentSetSize|state|threadCount|upTime|user|processCountDifference|cpuUsage\n");

        for (Application application : applicationData) {
            csv.append(timestamp).append("|");
            csv.append(application.getContextSwitches()).append("|");
            csv.append(application.getMajorFaults()).append("|");
            csv.append(application.getBitness()).append("|");
            csv.append(application.getCommandLine()).append("|");
            csv.append(application.getCurrentWorkingDirectory()).append("|");
            csv.append(application.getName()).append("|");
            csv.append(application.getOpenFiles()).append("|");
            csv.append(application.getParentProcessID()).append("|");
            csv.append(application.getPath()).append("|");
            csv.append(application.getResidentSetSize()).append("|");
            csv.append(application.getState()).append("|");
            csv.append(application.getThreadCount()).append("|");
            csv.append(application.getUpTime()).append("|");
            csv.append(application.getUser()).append("|");
            csv.append(application.getProcessCountDifference()).append("|");
            csv.append(application.getCpuUsage()).append("\n");
        }
        return csv.toString();
    }

    @Override
    public String convertResourceData(long timestamp, Resources resources) {
        ListToStringConverter<Long> longListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<Boolean> booleanListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<Double> doubleListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<String> stringListToStringConvert = new ListToStringSpacesConverter<>();

        StringBuilder csv = new StringBuilder();
        csv.append("timestamp|freeDiskSpace|readBytesDiskStores|readsDiskStores|writeBytesDiskStores|writesDiskStores|partitionsMajorFaults|partitionsMinorFaults|availableMemory|namesPowerSources|chargingPowerSources|dischargingPowerSources|powerOnLinePowerSources|remainingCapacityPercentPowerSources|contextSwitchesProcessor|interruptsProcessor\n");

        csv.append(timestamp).append("|");

        csv.append(resources.getFreeDiskSpace()).append("|");
        csv.append(longListToStringConverter.convert(resources.getReadBytesDiskStores())).append("|");
        csv.append(longListToStringConverter.convert(resources.getReadsDiskStores())).append("|");
        csv.append(longListToStringConverter.convert(resources.getWriteBytesDiskStores())).append("|");
        csv.append(longListToStringConverter.convert(resources.getWritesDiskStores())).append("|");
        csv.append(longListToStringConverter.convert(resources.getPartitionsMajorFaults())).append("|");
        csv.append(longListToStringConverter.convert(resources.getPartitionsMinorFaults())).append("|");

        csv.append(resources.getAvailableMemory()).append("|");

        csv.append(stringListToStringConvert.convert(resources.getPowerSourcesNames())).append("|");
        csv.append(booleanListToStringConverter.convert(resources.getPowerSourcesCharging())).append("|");
        csv.append(booleanListToStringConverter.convert(resources.getPowerSourcesDischarging())).append("|");
        csv.append(booleanListToStringConverter.convert(resources.getPowerSourcesPowerOnLine())).append("|");
        csv.append(doubleListToStringConverter.convert(resources.getPowerSourcesRemainingCapacityPercent())).append("|");

        csv.append(resources.getProcessorContextSwitches()).append("|");
        csv.append(resources.getProcessorInterrupts()).append("\n");
        return csv.toString();
    }

    @Override
    public String convertConnectionData(long timestamp, List<Connection> connectionData) {
        StringBuilder csv = new StringBuilder();
        csv.append("timestamp|localAddress|localPort|foreignAddress|foreignPort|state|type|owningProcessID\n");

        for (Connection connection : connectionData) {
            csv.append(timestamp).append("|");
            csv.append(connection.getLocalAddress()).append("|");
            csv.append(connection.getLocalPort()).append("|");
            csv.append(connection.getForeignAddress()).append("|");
            csv.append(connection.getForeignPort()).append("|");
            csv.append(connection.getState()).append("|");
            csv.append(connection.getType()).append("|");
            csv.append(connection.getOwningProcessID()).append("\n");
        }
        return csv.toString();
    }

    @Override
    public String convertNetworkInterfacesData(long timestamp, List<NetworkInterface> networkInterfaces) {
        ListToStringConverter<InetAddress> inetAddressListToStringConverter = new ListToStringSpacesConverter<>();
        ListToStringConverter<Short> shortListToStringConverter = new ListToStringSpacesConverter<>();

        StringBuilder csv = new StringBuilder();
        csv.append("timestamp|displayName|name|ipv4Address|ipv6Address|macAddress|subnetMask|bytesReceived|bytesSent|packetsReceived|packetsSent\n");

        for (NetworkInterface networkInterface : networkInterfaces) {
            csv.append(timestamp).append("|");
            csv.append(networkInterface.getDisplayName()).append("|");
            csv.append(networkInterface.getName()).append("|");
            csv.append(inetAddressListToStringConverter.convert(networkInterface.getIpv4Addresses())).append("|");
            csv.append(inetAddressListToStringConverter.convert(networkInterface.getIpv6Addresses())).append("|");
            csv.append(networkInterface.getMacAddress()).append("|");
            csv.append(shortListToStringConverter.convert(Arrays.stream(networkInterface.getSubnetMasks()).toList())).append("|");
            csv.append(networkInterface.getBytesReceived()).append("|");
            csv.append(networkInterface.getBytesSent()).append("|");
            csv.append(networkInterface.getPacketsReceived()).append("|");
            csv.append(networkInterface.getPacketsSent()).append("\n");
        }
        return csv.toString();
    }

    @Override
    public String convertClientData(long timestamp, Client client) {
        Computer computer = client.getComputer();
        Memory memory = client.getMemory();
        Processor processor = client.getProcessor();

        StringBuilder csv = new StringBuilder();
        csv.append("computerHardwareUUID|computerManufacturer|computerModel|memoryTotalSize|memoryPageSize|processorName|processorIdentifier|processorID|processorVendor|processorBitness|physicalPackageCount|physicalProcessorCount|logicalProcessorCount\n");

        csv.append(computer.getHardwareUUID()).append("|");
        csv.append(computer.getManufacturer()).append("|");
        csv.append(computer.getModel()).append("|");

        csv.append(memory.getTotalSize()).append("|");
        csv.append(memory.getPageSize()).append("|");

        csv.append(processor.getName()).append("|");
        csv.append(processor.getIdentifier()).append("|");
        csv.append(processor.getID()).append("|");
        csv.append(processor.getVendor()).append("|");
        csv.append(processor.getBitness()).append("|");
        csv.append(processor.getPhysicalPackageCount()).append("|");
        csv.append(processor.getPhysicalProcessorCount()).append("|");
        csv.append(processor.getLogicalProcessorCount()).append("\n");

        return csv.toString();
    }

    @Override
    public String convertDiskStoreData(List<DiskStore> diskStores) {
        StringBuilder csv = new StringBuilder();
        csv.append("model|name|size\n");
        for (DiskStore diskStore : diskStores) {
            csv.append(diskStore.getModel()).append("|");
            csv.append(diskStore.getName()).append("|");
            csv.append(diskStore.getSize()).append("|");
        }
        return csv.toString();
    }

    @Override
    public String convertPartitionData(List<Partition> partitions) {
        StringBuilder csv = new StringBuilder();
        csv.append("diskStoreName|identification|name|type|mountPoint|size|majorFaults|minorFaults\n");
        for (Partition partition : partitions) {
            csv.append(partition.getDiskStoreName()).append("|");
            csv.append(partition.getIdentification()).append("|");
            csv.append(partition.getName()).append("|");
            csv.append(partition.getType()).append("|");
            csv.append(partition.getMountPoint()).append("|");
            csv.append(partition.getSize()).append("|");
            csv.append(partition.getMajorFaults()).append("|");
            csv.append(partition.getMinorFaults()).append("\n");
        }
        return csv.toString();
    }
}
