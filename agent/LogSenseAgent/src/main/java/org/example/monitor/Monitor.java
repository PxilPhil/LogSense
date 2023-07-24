package org.example.monitor;

import org.example.converter.ObjectListConverter;
import org.example.model.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import oshi.SystemInfo;
import oshi.hardware.*;
import oshi.software.os.InternetProtocolStats;
import oshi.software.os.OSFileStore;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.*;

public class Monitor {
    private static final Logger LOGGER = LoggerFactory.getLogger(Monitor.class);
    private final OperatingSystem operatingSystem;
    private final HardwareAbstractionLayer hardware;

    public Monitor() {
        SystemInfo systemInfo = new SystemInfo();
        this.operatingSystem = systemInfo.getOperatingSystem();
        this.hardware = systemInfo.getHardware();
    }

    public List<OSProcess> monitorProcesses() {
        List<OSProcess> osProcesses = this.operatingSystem.getProcesses();
        if (osProcesses == null) {
            LOGGER.error("Error while monitoring the processes / application: the list of OS processes is null.");
        }
        return osProcesses;
    }

    public Resources monitorResources() {
        Resources resources = new Resources();
        List<OSFileStore> fileStores = this.operatingSystem.getFileSystem().getFileStores();
        if (fileStores != null) {
            resources.setFreeDiskSpace(calculateFreeDiskSpace(fileStores));
        } else {
            LOGGER.error("Error while monitoring the resources: the list of file stores is null. Therefore the free disk space can not be calculated.");
        }

        List<HWDiskStore> diskStores = this.hardware.getDiskStores();
        if (diskStores != null) {
            Map<String, List<Long>> diskStoresInformation = getDiskStoresInformation(diskStores);
            resources.setReadBytesDiskStores(diskStoresInformation.get("readBytesDiskStores"));
            resources.setReadsDiskStores(diskStoresInformation.get("readsDiskStores"));
            resources.setWriteBytesDiskStores(diskStoresInformation.get("writeBytesDiskStores"));
            resources.setWritesDiskStores(diskStoresInformation.get("writesDiskStores"));
            resources.setPartitionsMajorFaults(diskStoresInformation.get("partitionsMajorFaults"));
            resources.setPartitionsMinorFaults(diskStoresInformation.get("partitionsMinorFaults"));
        } else {
            LOGGER.error("Error while monitoring the resources: the list of disk stores is null. Therefore the information about the disk stores can not be collected.");
        }

        GlobalMemory memory = this.hardware.getMemory();
        if (memory != null) {
            resources.setAvailableMemory(memory.getAvailable());
        } else {
            LOGGER.error("Error while monitoring the resources: the global memory object is null. Therefore the available memory can not be collected.");
        }

        List<PowerSource> powerSources = this.hardware.getPowerSources();
        if (powerSources != null) {
            Map<String, List<Object>> powerSourcesInformation = getPowerSourcesInformation(powerSources);
            ObjectListConverter<Boolean> booleanObjectListConverter = new ObjectListConverter<>();
            ObjectListConverter<Double> doubleObjectListConverter = new ObjectListConverter<>();
            ObjectListConverter<String> stringObjectListConverter = new ObjectListConverter<>();
            resources.setPowerSourcesNames(stringObjectListConverter.convertObjectList(powerSourcesInformation.get("names"), String.class));
            resources.setPowerSourcesCharging(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("charging"), Boolean.class));
            resources.setPowerSourcesDischarging(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("discharging"), Boolean.class));
            resources.setPowerSourcesPowerOnLine(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("powerOnLine"), Boolean.class));
            resources.setPowerSourcesRemainingCapacityPercent(doubleObjectListConverter.convertObjectList(powerSourcesInformation.get("remainingCapacityPercent"), Double.class));
        } else {
            LOGGER.error("Error while monitoring the resources: the list of power sources is null. Therefore the information about the power sources can noz be collected.");
        }

        CentralProcessor processor = this.hardware.getProcessor();
        if (processor != null) {
            resources.setProcessorContextSwitches(processor.getContextSwitches());
            resources.setProcessorInterrupts(processor.getInterrupts());
        }

        return resources;
    }

    private long calculateFreeDiskSpace(List<OSFileStore> fileStores) {
        long freeDiskSpace = 0;
        for (OSFileStore fileStore : fileStores) {
            freeDiskSpace += fileStore.getFreeSpace();
        }
        return freeDiskSpace;
    }

    private Map<String, List<Long>> getDiskStoresInformation(List<HWDiskStore> diskStores) {
        Map<String, List<Long>> diskStoresInformation = new HashMap<>();
        for (HWDiskStore diskStore : diskStores) {
            List<Long> readBytesDiskStores = getReadBytesOfDiskStores(diskStoresInformation, diskStore);
            diskStoresInformation.put("readBytesDiskStores", readBytesDiskStores);

            List<Long> readsDiskStores = getReadsOfDiskStores(diskStoresInformation, diskStore);
            diskStoresInformation.put("readsDiskStores", readsDiskStores);

            List<Long> writeBytesDiskStores = getWriteBytesOfDiskStores(diskStoresInformation, diskStore);
            diskStoresInformation.put("writeBytesDiskStores", writeBytesDiskStores);

            List<Long> writesDiskStores = getWritesOfDiskStores(diskStoresInformation, diskStore);
            diskStoresInformation.put("writesDiskStores", writesDiskStores);

            List<Long> partitionsMajorFaults = getPartitionsMajorFaultsOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("partitionsMajorFaults", partitionsMajorFaults);

            List<Long> partitionsMinorFaults = getPartitionsMinorFaultsOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("partitionsMinorFaults", partitionsMinorFaults);
        }
        return diskStoresInformation;
    }

    private List<Long> getReadBytesOfDiskStores(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> readBytesDiskStores;
        if (diskStoresInformation.get("readBytesDiskStores") != null) {
            readBytesDiskStores = diskStoresInformation.get("readBytesDiskStores");
        } else {
            readBytesDiskStores = new ArrayList<>();
        }
        readBytesDiskStores.add(diskStore.getReadBytes());
        return readBytesDiskStores;
    }

    private List<Long> getReadsOfDiskStores(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> readsDiskStores;
        if (diskStoresInformation.get("readsDiskStores") != null) {
            readsDiskStores = diskStoresInformation.get("readsDiskStores");
        } else {
            readsDiskStores = new ArrayList<>();
        }
        readsDiskStores.add(diskStore.getReads());
        return readsDiskStores;
    }

    private List<Long> getWriteBytesOfDiskStores(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> writeBytesDiskStores;
        if (diskStoresInformation.get("writeBytesDiskStores") != null) {
            writeBytesDiskStores = diskStoresInformation.get("writeBytesDiskStores");
        } else {
            writeBytesDiskStores = new ArrayList<>();
        }
        writeBytesDiskStores.add(diskStore.getWriteBytes());
        return writeBytesDiskStores;
    }

    private List<Long> getWritesOfDiskStores(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> writesDiskStores;
        if (diskStoresInformation.get("writesDiskStores") != null) {
            writesDiskStores = diskStoresInformation.get("writesDiskStores");
        } else {
            writesDiskStores = new ArrayList<>();
        }
        writesDiskStores.add(diskStore.getWrites());
        return writesDiskStores;
    }

    private List<Long> getPartitionsMajorFaultsOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> partitionsMajorFaults;
        if (diskStoresInformation.get("partitionsMajorFaults") != null) {
            partitionsMajorFaults = diskStoresInformation.get("partitionsMajorFaults");
        } else {
            partitionsMajorFaults = new ArrayList<>();
        }
        for (HWPartition partition : diskStore.getPartitions()) {
            partitionsMajorFaults.add((long) partition.getMajor());
        }
        return partitionsMajorFaults;
    }

    private List<Long> getPartitionsMinorFaultsOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> partitionsMinorFaults;
        if (diskStoresInformation.get("partitionsMinorFaults") != null) {
            partitionsMinorFaults = diskStoresInformation.get("partitionsMinorFaults");
        } else {
            partitionsMinorFaults = new ArrayList<>();
        }
        for (HWPartition partition : diskStore.getPartitions()) {
            partitionsMinorFaults.add((long) partition.getMinor());
        }
        return partitionsMinorFaults;
    }

    private Map<String, List<Object>> getPowerSourcesInformation(List<PowerSource> powerSources) {
        Map<String, List<Object>> powerSourcesInformation = new HashMap<>();
        for (PowerSource powerSource : powerSources) {
            List<Object> names = addPowersourceNameToList(powerSourcesInformation.get("names"), powerSource.getName());
            powerSourcesInformation.put("names", names);

            List<Object> charging = addPowerSourceChargingToList(powerSourcesInformation.get("charging"), powerSource.isCharging());
            powerSourcesInformation.put("charging", charging);

            List<Object> discharging = addPowerSourceDischargingToList(powerSourcesInformation.get("discharging"), powerSource.isDischarging());
            powerSourcesInformation.put("discharging", discharging);

            List<Object> powerOnLine = addPowerSourcePowerOnLineToList(powerSourcesInformation.get("powerOnLine"), powerSource.isPowerOnLine());
            powerSourcesInformation.put("powerOnLine", powerOnLine);

            List<Object> remainingCapacityPercent = addPowerSourceRemainingCapacityPercentToList(powerSourcesInformation.get("remainingCapacityPercent"), powerSource.getRemainingCapacityPercent());
            powerSourcesInformation.put("remainingCapacityPercent", remainingCapacityPercent);
        }
        return powerSourcesInformation;
    }

    private List<Object> addPowersourceNameToList(List<Object> powerSourcesNames, String name) {
        List<Object> names;
        names = Objects.requireNonNullElseGet(powerSourcesNames, ArrayList::new);
        names.add(name);
        return names;
    }

    private List<Object> addPowerSourceChargingToList(List<Object> powerSourcesCharging, boolean isCharging) {
        List<Object> charging;
        charging = Objects.requireNonNullElseGet(powerSourcesCharging, ArrayList::new);
        charging.add(isCharging);
        return charging;
    }

    private List<Object> addPowerSourceDischargingToList(List<Object> powerSourcesDischarging, boolean isDischarging) {
        List<Object> discharging;
        discharging = Objects.requireNonNullElseGet(powerSourcesDischarging, ArrayList::new);
        discharging.add(isDischarging);
        return discharging;
    }

    private List<Object> addPowerSourcePowerOnLineToList(List<Object> powerSourcesPowerOnLine, boolean isPowerOnLine) {
        List<Object> powerOnLine;
        powerOnLine = Objects.requireNonNullElseGet(powerSourcesPowerOnLine, ArrayList::new);
        powerOnLine.add(isPowerOnLine);
        return powerOnLine;
    }

    private List<Object> addPowerSourceRemainingCapacityPercentToList(List<Object> powerSourcesRemainingCapacityPercent, double remainingCapacityPercent) {
        List<Object> remainingCapacityPercents;
        remainingCapacityPercents = Objects.requireNonNullElseGet(powerSourcesRemainingCapacityPercent, ArrayList::new);
        remainingCapacityPercents.add(remainingCapacityPercent);
        return remainingCapacityPercents;
    }

    public List<NetworkInterface> monitorNetworkInterfaces() {
        List<NetworkInterface> networkInterfaces = new ArrayList<>();

        List<NetworkIF> networkIFList = this.hardware.getNetworkIFs();
        if (networkIFList != null) {
            for (NetworkIF networkIF : this.hardware.getNetworkIFs()) {
                NetworkInterface networkInterface = new NetworkInterface();
                networkInterface.setDisplayName(networkIF.getDisplayName());
                networkInterface.setName(networkIF.getName());
                networkInterface.setIpv4Addresses(convertStringArrayToIpAddressList(networkIF.getIPv4addr()));
                networkInterface.setIpv6Addresses(convertStringArrayToIpAddressList(networkIF.getIPv6addr()));
                networkInterface.setMacAddress(networkIF.getMacaddr());
                networkInterface.setSubnetMasks(networkIF.getSubnetMasks());
                networkInterface.setBytesReceived(networkIF.getBytesRecv());
                networkInterface.setBytesSent(networkIF.getBytesSent());
                networkInterface.setPacketsReceived(networkIF.getPacketsRecv());
                networkInterface.setPacketsSent(networkIF.getPacketsSent());
                networkInterfaces.add(networkInterface);
            }
        } else {
            LOGGER.error("Error while monitoring the network interfaces: the list of network interfaces is null. Therefore the information about the network interfaces can not be collected.");
        }
        return networkInterfaces;
    }

    private List<InetAddress> convertStringArrayToIpAddressList(String[] ipAddressesAsStrings) {
        List<InetAddress> ipAddresses = new ArrayList<>();
        for (String ipAddress : ipAddressesAsStrings) {
            try {
                ipAddresses.add(InetAddress.getByName(ipAddress));
            } catch (UnknownHostException e) {
                throw new RuntimeException(e);
            }
        }
        return ipAddresses;
    }

    public List<Connection> monitorIpConnections() {
        List<Connection> connections = new ArrayList<>();

        List<InternetProtocolStats.IPConnection> ipConnections = this.operatingSystem.getInternetProtocolStats().getConnections();
        if (ipConnections != null) {
            for (InternetProtocolStats.IPConnection connection : ipConnections) {
                Connection connectionData = new Connection();
                connectionData.setLocalPort(connection.getLocalPort());
                connectionData.setForeignPort(connection.getForeignPort());
                connectionData.setState(connection.getState());
                connectionData.setType(connection.getType());
                connectionData.setOwningProcessID(connection.getowningProcessId());

                try {
                    connectionData.setLocalAddress(InetAddress.getByAddress(connection.getLocalAddress()));
                } catch (UnknownHostException e) {
                    LOGGER.error("Error while monitoring the IP connections: the local address of the IP connection could not be parsed to an InetAddress. Therefore the local address attribute of the IP connection will be null.");
                }

                try {
                    connectionData.setForeignAddress(InetAddress.getByAddress(connection.getForeignAddress()));
                } catch (UnknownHostException e) {
                    LOGGER.error("Error while monitoring the IP connections: the foreign address of the IP connection could not be parsed to an InetAddress. Therefore the foreign address attribute of the IP connection will be null.");
                }

                connections.add(connectionData);
            }
        } else {
            LOGGER.error("Error while monitoring the IP connections: the list of IP connections is null. Therefore the information about the IP connections can not be collected.");
        }

        return connections;
    }

    public Client monitorClientData() {
        List<String> monitoringErrors = new ArrayList<>();
        Client client = new Client();

        ComputerSystem computerSystem = this.hardware.getComputerSystem();
        if (computerSystem != null) {
            client.setComputer(getComputerData(computerSystem));
        } else {
            monitoringErrors.add("computer system");
        }

        GlobalMemory globalMemory = this.hardware.getMemory();
        if (globalMemory != null) {
            client.setMemory(getMemoryData(globalMemory));
        } else {
            monitoringErrors.add("global memory");
        }

        CentralProcessor centralProcessor = this.hardware.getProcessor();
        if (centralProcessor != null) {
            CentralProcessor.ProcessorIdentifier processorIdentifier = centralProcessor.getProcessorIdentifier();
            if (processorIdentifier != null) {
                client.setProcessor(getProcessorData(centralProcessor, processorIdentifier));
            } else {
                monitoringErrors.add("processor");
            }
        } else {
            monitoringErrors.add("processor");
        }

        if (monitoringErrors.size() > 0) {
            LOGGER.error("Error while monitoring the client data: " + monitoringErrors + "is / are null. Therefore the information about the client can not be collected.");
        }

        return client;
    }

    private Computer getComputerData(ComputerSystem computerSystem) {
        Computer computer = new Computer();
        computer.setHardwareUUID(computerSystem.getHardwareUUID());
        computer.setManufacturer(computerSystem.getManufacturer());
        computer.setModel(computerSystem.getModel());
        return computer;
    }

    private Memory getMemoryData(GlobalMemory globalMemory) {
        Memory memory = new Memory();
        memory.setTotalSize(globalMemory.getTotal());
        memory.setPageSize(globalMemory.getPageSize());
        return memory;
    }

    private Processor getProcessorData(CentralProcessor centralProcessor, CentralProcessor.ProcessorIdentifier processorIdentifier) {
        Processor processor = new Processor();
        processor.setName(processorIdentifier.getName());
        processor.setIdentifier(processorIdentifier.getIdentifier());
        processor.setID(processorIdentifier.getProcessorID());
        processor.setVendor(processorIdentifier.getVendor());

        if (processorIdentifier.isCpu64bit()) {
            processor.setBitness(64);
        } else {
            processor.setBitness(32);
        }

        processor.setPhysicalPackageCount(centralProcessor.getPhysicalPackageCount());
        processor.setPhysicalProcessorCount(centralProcessor.getPhysicalProcessorCount());
        processor.setLogicalProcessorCount(centralProcessor.getLogicalProcessorCount());
        return processor;
    }

    public List<DiskStore> monitorDiskStores() {
        List<HWDiskStore> hwDiskStoreList = this.hardware.getDiskStores();
        List<DiskStore> diskStores = new ArrayList<>();

        if (hwDiskStoreList != null) {
            for (HWDiskStore diskStore : hwDiskStoreList) {
                DiskStore diskStoreData = new DiskStore();
                diskStoreData.setModel(diskStore.getModel());
                diskStoreData.setName(diskStore.getName());
                diskStoreData.setSize(diskStore.getSize());
                diskStores.add(diskStoreData);
            }
        } else {
            LOGGER.error("Error while monitoring the disk stores: the list of HW disk stores is null. Therefore the information about the disk stores can not be collected.");
        }

        return diskStores;
    }

    public List<Partition> monitorPartitions() {
        List<Partition> partitions = new ArrayList<>();

        List<HWDiskStore> hwDiskStoreList = this.hardware.getDiskStores();
        if (hwDiskStoreList != null) {
            for (HWDiskStore diskStore : hwDiskStoreList) {
                List<HWPartition> hwPartitionList = diskStore.getPartitions();
                if (hwPartitionList != null) {
                    for (HWPartition partition : hwPartitionList) {
                        Partition partitionData = new Partition();
                        partitionData.setDiskStoreName(diskStore.getName());
                        partitionData.setIdentification(partition.getIdentification());
                        partitionData.setName(partition.getName());
                        partitionData.setType(partition.getType());
                        partitionData.setMountPoint(partition.getMountPoint());
                        partitionData.setSize(partition.getSize());
                        partitionData.setMajorFaults(partition.getMajor());
                        partitionData.setMinorFaults(partition.getMinor());
                        partitions.add(partitionData);
                    }
                } else {
                    LOGGER.error("Error while monitoring the partitions: the list of HW partitions of the disk store " + diskStore.getName() + " is null. Therefore the information about the partitions of this disk store can not be collected.");
                }
            }
        } else {
            LOGGER.error("Error while monitoring the partitions: the list of HW disk stores is null. Therefore the information about the partitions of the disk stores can not be collected.");
        }
        return partitions;
    }
}
