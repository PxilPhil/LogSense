package org.example.monitor;

import org.example.common.Monitor;
import org.example.converter.ObjectListConverter;
import org.example.model.Process;
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
import java.time.Instant;
import java.util.*;

public class OshiMonitor implements Monitor {
    private static final Logger LOGGER = LoggerFactory.getLogger(OshiMonitor.class);
    private final OperatingSystem operatingSystem;
    private final HardwareAbstractionLayer hardware;
    private List<OSProcess> previousOsProcesses;

    public OshiMonitor() {
        SystemInfo systemInfo = new SystemInfo();
        this.operatingSystem = systemInfo.getOperatingSystem();
        this.hardware = systemInfo.getHardware();
    }

    public String monitorOperatingSystem() {
        return this.operatingSystem.getFamily();
    }

    public List<Process> monitorProcesses() throws NullPointerException {
        List<OSProcess> osProcesses = this.operatingSystem.getProcesses();
        if (osProcesses == null) {
            throw new NullPointerException("The list of operating system processes is null because the processes could not be collected");
        }

        List<Process> processes = new ArrayList<>();
        for (OSProcess osProcess : osProcesses) {
            double cpuUsage = calculateCpuUsage(osProcess);
            processes.add(new Process(osProcess.getProcessID(), osProcess.getName(), osProcess.getBitness(), osProcess.getCommandLine(), osProcess.getCurrentWorkingDirectory(), osProcess.getPath(), osProcess.getState().toString(), osProcess.getUser(), osProcess.getContextSwitches(), osProcess.getMajorFaults(), osProcess.getOpenFiles(), osProcess.getResidentSetSize(), osProcess.getThreadCount(), osProcess.getUpTime(), cpuUsage));
        }
        this.previousOsProcesses = osProcesses;
        return processes;
    }

    private double calculateCpuUsage(OSProcess osProcess) {
        double cpuUsage = 0;
        for (OSProcess previousOsProcess : this.previousOsProcesses) {
            if (previousOsProcess.getProcessID() == osProcess.getProcessID()) {
                cpuUsage = osProcess.getProcessCpuLoadBetweenTicks(previousOsProcess);
            } else {
                cpuUsage = osProcess.getProcessCpuLoadBetweenTicks(null);
            }
        }
        return cpuUsage;
    }

    public Resources monitorResources() {
        Long freeDiskSpace = calculateFreeDiskSpace();

        Map<String, List<Long>> diskStoresInformation = new HashMap<>();
        List<HWDiskStore> diskStores = this.hardware.getDiskStores();
        if (diskStores == null) {
            LOGGER.error("The list of hardware disk stores is null because they could not be collected.");
        } else {
            diskStoresInformation = getDiskStoresInformation(diskStores);
        }

        GlobalMemory memory = this.hardware.getMemory();
        Long availableMemory = null;
        if (memory == null) {
            LOGGER.error("The global memory is null.");
        } else {
            availableMemory = memory.getAvailable();
        }

        List<PowerSource> powerSources = this.hardware.getPowerSources();
        List<String> powerSourcesNames = null;
        List<Boolean> powerSourcesCharging = null;
        List<Boolean> powerSourcesDischarging = null;
        List<Boolean> powerSourcesOnLine = null;
        List<Double> powerSourcesRemainingCapacityPercent = null;
        if (powerSources == null) {
            LOGGER.error("The list of power sources is null.");
        } else {
            Map<String, List<Object>> powerSourcesInformation = getPowerSourcesInformation(powerSources);
            ObjectListConverter<Boolean> booleanObjectListConverter = new ObjectListConverter<>();
            ObjectListConverter<Double> doubleObjectListConverter = new ObjectListConverter<>();
            ObjectListConverter<String> stringObjectListConverter = new ObjectListConverter<>();

            powerSourcesNames = stringObjectListConverter.convertObjectList(powerSourcesInformation.get("names"), String.class);
            powerSourcesCharging = booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("charging"), Boolean.class);
            powerSourcesDischarging = booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("discharging"), Boolean.class);
            powerSourcesOnLine = booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("powerOnLine"), Boolean.class);
            powerSourcesRemainingCapacityPercent = doubleObjectListConverter.convertObjectList(powerSourcesInformation.get("remainingCapacityPercent"), Double.class);
        }


        CentralProcessor processor = this.hardware.getProcessor();
        Long processorContextSwitches = null;
        Long processorInterrupts = null;
        if (processor == null) {
            LOGGER.error("The central processor is null.");
        } else {
            processorContextSwitches = processor.getContextSwitches();
            processorInterrupts = processor.getInterrupts();
        }

        return new Resources(freeDiskSpace,
                diskStoresInformation.getOrDefault("readBytesDiskStores", null),
                diskStoresInformation.getOrDefault("readsDiskStores", null),
                diskStoresInformation.getOrDefault("writeBytesDiskStores", null),
                diskStoresInformation.getOrDefault("writesDiskStores", null),
                diskStoresInformation.getOrDefault("partitionsMajorFaults", null),
                diskStoresInformation.getOrDefault("partitionsMinorFaults", null), availableMemory,
                powerSourcesNames, powerSourcesCharging, powerSourcesDischarging, powerSourcesOnLine,
                powerSourcesRemainingCapacityPercent, processorContextSwitches, processorInterrupts);
    }


    private Long calculateFreeDiskSpace() {
        List<OSFileStore> fileStores = this.operatingSystem.getFileSystem().getFileStores();
        if (fileStores == null) {
            LOGGER.error("The list of operating system file stores is null because the file system" +
                    "or the file stores could not be collected.");
            return null;
        }

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
                NetworkInterface networkInterface = new NetworkInterface(networkIF.getDisplayName(), networkIF.getName(), convertStringArrayToIpAddressList(networkIF.getIPv4addr()), convertStringArrayToIpAddressList(networkIF.getIPv6addr()), networkIF.getMacaddr(), networkIF.getSubnetMasks(), networkIF.getBytesRecv(), networkIF.getBytesSent(), networkIF.getCollisions(), networkIF.getPacketsRecv(), networkIF.getPacketsSent());
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
        List<Connection> connections = null;
        List<InternetProtocolStats.IPConnection> ipConnections = this.operatingSystem.getInternetProtocolStats().getConnections();
        if (ipConnections != null) {
            connections = new ArrayList<>();
            for (InternetProtocolStats.IPConnection connection : ipConnections) {
                InetAddress localAddress = null;
                try {
                    localAddress = InetAddress.getByAddress(connection.getLocalAddress());
                } catch (UnknownHostException e) {
                    LOGGER.warn("Error while monitoring the IP connections: the local address of the IP connection could not be parsed to an InetAddress. Therefore the local address attribute of the IP connection will be null.");
                }

                InetAddress foreignAddress = null;
                try {
                    foreignAddress = InetAddress.getByAddress(connection.getForeignAddress());
                } catch (UnknownHostException e) {
                    LOGGER.warn("Error while monitoring the IP connections: the foreign address of the IP connection could not be parsed to an InetAddress. Therefore the foreign address attribute of the IP connection will be null.");
                }

                Connection connectionData = new Connection(localAddress, connection.getLocalPort(), foreignAddress,
                        connection.getForeignPort(), connection.getState(), connection.getType(),
                        connection.getowningProcessId());
                connections.add(connectionData);
            }
        } else {
            LOGGER.error("Error while monitoring the IP connections: the list of IP connections is null. Therefore the information about the IP connections can not be collected.");
        }

        return connections;
    }

    public Client monitorClientData() {
        List<String> monitoringErrors = new ArrayList<>();

        ComputerSystem computerSystem = this.hardware.getComputerSystem();
        Computer computerData = null;
        if (computerSystem == null) {
            monitoringErrors.add("computer system");
        } else {
            computerData = getComputerData(computerSystem);
        }

        GlobalMemory globalMemory = this.hardware.getMemory();
        Memory memoryData = null;
        if (globalMemory == null) {
            monitoringErrors.add("global memory");
        } else {
            memoryData = getMemoryData(globalMemory);
        }

        CentralProcessor centralProcessor = this.hardware.getProcessor();
        Processor processorData = null;
        if (centralProcessor == null) {
            monitoringErrors.add("central processor");
        } else {
            CentralProcessor.ProcessorIdentifier processorIdentifier = centralProcessor.getProcessorIdentifier();
            if (processorIdentifier == null) {
                monitoringErrors.add("processor identifier");
            } else {
                processorData = getProcessorData(centralProcessor, processorIdentifier);
            }
        }

        if (monitoringErrors.size() > 0) {
            LOGGER.error("Error while monitoring the client data: " + monitoringErrors + "is / are null. Therefore the information about the client can not be collected.");
        }

        return new Client(Instant.now().toEpochMilli(), computerData, memoryData, processorData);
    }

    private Computer getComputerData(ComputerSystem computerSystem) {
        return new Computer(computerSystem.getHardwareUUID(), computerSystem.getManufacturer(), computerSystem.getModel());
    }

    private Memory getMemoryData(GlobalMemory globalMemory) {
        return new Memory(globalMemory.getTotal(), globalMemory.getPageSize());
    }

    private Processor getProcessorData(CentralProcessor centralProcessor, CentralProcessor.ProcessorIdentifier processorIdentifier) {
        int bitness;
        if (processorIdentifier.isCpu64bit()) {
            bitness = 64;
        } else {
            bitness = 32;
        }
        return new Processor(processorIdentifier.getName(), processorIdentifier.getIdentifier(), processorIdentifier.getProcessorID(), processorIdentifier.getVendor(), bitness, centralProcessor.getPhysicalPackageCount(), centralProcessor.getPhysicalProcessorCount(), centralProcessor.getLogicalProcessorCount());
    }

    public List<DiskStore> monitorDiskStores() {
        long timestamp = Instant.now().toEpochMilli();
        List<HWDiskStore> hwDiskStoreList = this.hardware.getDiskStores();
        List<DiskStore> diskStores = new ArrayList<>();

        if (hwDiskStoreList != null) {
            for (HWDiskStore diskStore : hwDiskStoreList) {
                DiskStore diskStoreData = new DiskStore(timestamp, diskStore.getSerial(), diskStore.getModel(), diskStore.getName(), diskStore.getSize());
                diskStores.add(diskStoreData);
            }
        } else {
            LOGGER.error("Error while monitoring the disk stores: the list of HW disk stores is null. Therefore the information about the disk stores can not be collected.");
        }

        return diskStores;
    }

    public List<Partition> monitorPartitions() {
        long timestamp = Instant.now().toEpochMilli();
        List<Partition> partitions = new ArrayList<>();

        List<HWDiskStore> hwDiskStoreList = this.hardware.getDiskStores();
        if (hwDiskStoreList != null) {
            for (HWDiskStore diskStore : hwDiskStoreList) {
                List<HWPartition> hwPartitionList = diskStore.getPartitions();
                if (hwPartitionList != null) {
                    for (HWPartition partition : hwPartitionList) {
                        Partition partitionData = new Partition(timestamp, diskStore.getName(),
                                partition.getIdentification(), partition.getName(), partition.getType(),
                                partition.getMountPoint(), partition.getSize(), partition.getMajor(),
                                partition.getMinor());
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
