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

            return "timestamp|freeDiskSpace|readBytesDiskStores|readsDiskStores|writeBytesDiskStores|writesDiskStores|partitionsMajorFaults|partitionsMinorFaults|availableMemory|namesPowerSources|chargingPowerSources|dischargingPowerSources|powerOnLinePowerSources|remainingCapacityPercentPowerSources|contextSwitchesProcessor|interruptsProcessor\n" +
                    timestamp + "|" +
                    resources.freeDiskSpace() + "|" +
                    longListToStringConverter.convert(resources.readBytesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.readsDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.writeBytesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.writesDiskStores()) + "|" +
                    longListToStringConverter.convert(resources.partitionsMajorFaults()) + "|" +
                    longListToStringConverter.convert(resources.partitionsMinorFaults()) + "|" +
                    resources.availableMemory() + "|" +
                    stringListToStringConvert.convert(resources.powerSourcesNames()) + "|" +
                    booleanListToStringConverter.convert(resources.powerSourcesCharging()) + "|" +
                    booleanListToStringConverter.convert(resources.powerSourcesDischarging()) + "|" +
                    booleanListToStringConverter.convert(resources.powerSourcesPowerOnLine()) + "|" +
                    doubleListToStringConverter.convert(resources.powerSourcesRemainingCapacityPercent()) + "|" +
                    resources.processorContextSwitches() + "|" +
                    resources.processorInterrupts() + "\n";
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
                csv.append(connection.localAddress()).append("|");
                csv.append(connection.localPort()).append("|");
                csv.append(connection.foreignAddress()).append("|");
                csv.append(connection.foreignPort()).append("|");
                csv.append(connection.state()).append("|");
                csv.append(connection.type()).append("|");
                csv.append(connection.owningProcessID()).append("\n");
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
                csv.append(networkInterface.displayName()).append("|");
                csv.append(networkInterface.name()).append("|");
                csv.append(inetAddressListToStringConverter.convert(networkInterface.ipv4Addresses())).append("|");
                csv.append(inetAddressListToStringConverter.convert(networkInterface.ipv6Addresses())).append("|");
                csv.append(networkInterface.macAddress()).append("|");
                csv.append(shortListToStringConverter.convert(Arrays.stream(networkInterface.subnetMasks()).toList())).append("|");
                csv.append(networkInterface.bytesReceived()).append("|");
                csv.append(networkInterface.bytesSent()).append("|");
                csv.append(networkInterface.collisions()).append("|");
                csv.append(networkInterface.packetsReceived()).append("|");
                csv.append(networkInterface.packetsSent()).append("\n");
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

            csv.append(client.timestamp()).append("|");

            Computer computer = client.computer();
            Memory memory = client.memory();
            Processor processor = client.processor();

            csv.append(computer.hardwareUUID()).append("|");
            csv.append(computer.manufacturer()).append("|");
            csv.append(computer.model()).append("|");

            csv.append(memory.totalSize()).append("|");
            csv.append(memory.pageSize()).append("|");

            csv.append(processor.name()).append("|");
            csv.append(processor.identifier()).append("|");
            csv.append(processor.ID()).append("|");
            csv.append(processor.vendor()).append("|");
            csv.append(processor.bitness()).append("|");
            csv.append(processor.physicalPackageCount()).append("|");
            csv.append(processor.physicalProcessorCount()).append("|");
            csv.append(processor.logicalProcessorCount()).append("\n");

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
                csv.append(diskStore.timestamp()).append("|");
                csv.append(diskStore.serialNumber()).append("|");
                csv.append(diskStore.model()).append("|");
                csv.append(diskStore.name()).append("|");
                csv.append(diskStore.size()).append("\n");
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
                csv.append(partition.timestamp()).append("|");
                csv.append(partition.diskStoreName()).append("|");
                csv.append(partition.identification()).append("|");
                csv.append(partition.name()).append("|");
                csv.append(partition.type()).append("|");
                csv.append(partition.mountPoint()).append("|");
                csv.append(partition.size()).append("|");
                csv.append(partition.majorFaults()).append("|");
                csv.append(partition.minorFaults()).append("\n");
            }
            return csv.toString();
        } else {
            LOGGER.error("Error while converting the partition data to CSV: either the list of partitions is null or the timestamp is not between epoch and now. Therefore the partitions can not be converted to CSV.");
            return null;
        }
    }
}
