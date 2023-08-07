package org.example.converter;

import org.example.common.DataConverter;
import org.example.common.ListToStringConverter;
import org.example.model.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetAddress;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;

public class CSVDataConverter implements DataConverter {
    private static final Logger LOGGER = LoggerFactory.getLogger(CSVDataConverter.class);

    @Override
    public String convertApplicationData(long timestamp, List<Application> applications) {
        if (applications != null && timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
            StringBuilder csv = new StringBuilder();
            csv.append("timestamp|contextSwitches|majorFaults|bitness|commandLine|currentWorkingDirectory|name|openFiles|parentProcessID|path|residentSetSize|state|threadCount|upTime|user|processCountDifference|cpuUsage\n");

            for (Application application : applications) {
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
        } else {
            LOGGER.error("Error while converting applications to CSV: either the list of applications is null or the timestamp is not between epoch and now. Therefore the applications can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertResourceData(long timestamp, Resources resources) {
        if (resources != null && timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
            ListToStringConverter<Long> longListToStringConverter = new ListToStringSpacesConverter<>();
            ListToStringConverter<Boolean> booleanListToStringConverter = new ListToStringSpacesConverter<>();
            ListToStringConverter<Double> doubleListToStringConverter = new ListToStringSpacesConverter<>();
            ListToStringConverter<String> stringListToStringConvert = new ListToStringSpacesConverter<>();

            String csv = "timestamp|freeDiskSpace|readBytesDiskStores|readsDiskStores|writeBytesDiskStores|writesDiskStores|partitionsMajorFaults|partitionsMinorFaults|availableMemory|namesPowerSources|chargingPowerSources|dischargingPowerSources|powerOnLinePowerSources|remainingCapacityPercentPowerSources|contextSwitchesProcessor|interruptsProcessor\n" +
                    timestamp + "|" +
                    resources.getFreeDiskSpace() + "|" +
                    longListToStringConverter.convert(resources.getReadBytesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.getReadsDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.getWriteBytesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.getWritesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.getPartitionsMajorFaults()) + "|" +
                    longListToStringConverter.convert(resources.getPartitionsMinorFaults()) + "|" +
                    resources.getAvailableMemory() + "|" +
                    stringListToStringConvert.convert(resources.getPowerSourcesNames()) + "|" +
                    booleanListToStringConverter.convert(resources.getPowerSourcesCharging()) + "|" +
                    booleanListToStringConverter.convert(resources.getPowerSourcesDischarging()) + "|" +
                    booleanListToStringConverter.convert(resources.getPowerSourcesPowerOnLine()) + "|" +
                    doubleListToStringConverter.convert(resources.getPowerSourcesRemainingCapacityPercent()) + "|" +
                    resources.getProcessorContextSwitches() + "|" +
                    resources.getProcessorInterrupts() + "\n";
            return csv;
        } else {
            LOGGER.error("Error while converting the resource data to CSV: either the resource data object is null or the timestamp is not between epoch and now. Therefore the resource data can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertConnectionData(long timestamp, List<Connection> connectionData) {
        if (connectionData != null && timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
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
        } else {
            LOGGER.error("Error while converting the connection data to CSV: either the list of connections is null or the timestamp is not between epoch and now. Therefore the connections can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertNetworkInterfacesData(long timestamp, List<NetworkInterface> networkInterfaces) {
        if (networkInterfaces != null && timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
            ListToStringConverter<InetAddress> inetAddressListToStringConverter = new ListToStringSpacesConverter<>();
            ListToStringConverter<Short> shortListToStringConverter = new ListToStringSpacesConverter<>();

            StringBuilder csv = new StringBuilder();
            csv.append("timestamp|displayName|name|ipv4Address|ipv6Address|macAddress|subnetMask|bytesReceived|bytesSent|collisions|packetsReceived|packetsSent\n");

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
                csv.append(networkInterface.getCollisions()).append("|");
                csv.append(networkInterface.getPacketsReceived()).append("|");
                csv.append(networkInterface.getPacketsSent()).append("\n");
            }
            return csv.toString();
        } else {
            LOGGER.error("Error while converting the network interfaces data to CSV: either the list of network interfaces is null or the timestamp is not between epoch and now. Therefore the network interfaces can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertClientData(Client client) {
        if (client != null) {
            StringBuilder csv = new StringBuilder();
            csv.append("measurement_time|computerHardwareUUID|computerManufacturer|computerModel|memoryTotalSize|memoryPageSize|processorName|processorIdentifier|processorID|processorVendor|processorBitness|physicalPackageCount|physicalProcessorCount|logicalProcessorCount\n");

            csv.append(client.getTimestamp()).append("|");

            Computer computer = client.getComputer();
            Memory memory = client.getMemory();
            Processor processor = client.getProcessor();

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
        } else {
            LOGGER.error("Error while converting the client data to CSV: either the client data object is null or the timestamp is not between epoch and now. Therefore the client data can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertDiskStoreData(List<DiskStore> diskStores) {
        if (diskStores != null) {
            StringBuilder csv = new StringBuilder();
            csv.append("measurement_time|serialNumber|model|name|size\n");
            for (DiskStore diskStore : diskStores) {
                csv.append(diskStore.getTimestamp()).append("|");
                csv.append(diskStore.getSerialNumber()).append("|");
                csv.append(diskStore.getModel()).append("|");
                csv.append(diskStore.getName()).append("|");
                csv.append(diskStore.getSize()).append("\n");
            }
            return csv.toString();
        } else {
            LOGGER.error("Error while converting the disk store data to CSV: either the list of disk stores is null or the timestamp is not between epoch and now. Therefore the disk stores can not be converted to CSV.");
            return null;
        }
    }

    @Override
    public String convertPartitionData(List<Partition> partitions) {
        if (partitions != null) {
            StringBuilder csv = new StringBuilder();
            csv.append("measurement_time|diskStoreName|identification|name|type|mountPoint|size|majorFaults|minorFaults\n");
            for (Partition partition : partitions) {
                csv.append(partition.getTimestamp()).append("|");
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
        } else {
            LOGGER.error("Error while converting the partition data to CSV: either the list of partitions is null or the timestamp is not between epoch and now. Therefore the partitions can not be converted to CSV.");
            return null;
        }
    }
}
