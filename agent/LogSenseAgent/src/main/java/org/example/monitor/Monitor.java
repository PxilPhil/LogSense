package org.example.monitor;

import org.example.analysis.StatService;
import org.example.converter.ObjectListConverter;
import org.example.model.ResourcesData;
import oshi.SystemInfo;
import oshi.hardware.*;
import oshi.software.os.OSFileStore;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Monitor {
    private final SystemInfo systemInfo;
    private final OperatingSystem operatingSystem;
    private final HardwareAbstractionLayer hardware;
    private final StatService statService;

    public Monitor() {
        this.systemInfo = new SystemInfo();
        this.operatingSystem = this.systemInfo.getOperatingSystem();
        this.hardware = this.systemInfo.getHardware();
        this.statService = new StatService();
    }

    public List<OSProcess> monitorProcesses() {
        return this.operatingSystem.getProcesses();
    }

    public ResourcesData monitorResources() {
        ResourcesData resourcesData = new ResourcesData();
        resourcesData.setFreeDiskSpace(calculateFreeDiskSpace(this.operatingSystem.getFileSystem().getFileStores()));

        List<HWDiskStore> diskStores = this.hardware.getDiskStores();
        Map<String, List<Long>> diskStoresInformation = getDiskStoresInformation(diskStores);
        resourcesData.setDiskStoresReadBytes(diskStoresInformation.get("readBytes"));
        resourcesData.setDiskStoresReads(diskStoresInformation.get("reads"));
        resourcesData.setDiskStoresWriteBytes(diskStoresInformation.get("writeBytes"));
        resourcesData.setDiskStoresWrites(diskStoresInformation.get("writes"));
        resourcesData.setPartitionsMajorFaults(diskStoresInformation.get("partitionsMajorFaults"));
        resourcesData.setPartitionsMinorFaults(diskStoresInformation.get("partitionsMinorFaults"));

        resourcesData.setAvailableMemory(this.hardware.getMemory().getAvailable());

        Map<String, List<Long>> networkInterfacesInformation = getNetworkInterfacesInformation(this.hardware.getNetworkIFs());
        resourcesData.setNetworkInterfacesBytesReceived(networkInterfacesInformation.get("bytesReceived"));
        resourcesData.setNetworkInterfacesBytesSent(networkInterfacesInformation.get("bytesSent"));
        resourcesData.setNetworkInterfacesCollisions(networkInterfacesInformation.get("collisions"));
        resourcesData.setNetworkInterfacesPacketsReceived(networkInterfacesInformation.get("packetsReceived"));
        resourcesData.setNetworkInterfacesPacketsSent(networkInterfacesInformation.get("packetsSent"));

        ObjectListConverter<Boolean> booleanObjectListConverter = new ObjectListConverter<>();
        ObjectListConverter<Double> doubleObjectListConverter = new ObjectListConverter<>();
        Map<String, List<Object>> powerSourcesInformation = getPowerSourcesInformation(this.hardware.getPowerSources());
        resourcesData.setPowerSourcesCharging(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("charging"), Boolean.class));
        resourcesData.setPowerSourcesDischarging(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("discharging"), Boolean.class));
        resourcesData.setPowerSourcesPowerOnLine(booleanObjectListConverter.convertObjectList(powerSourcesInformation.get("powerOnLine"), Boolean.class));
        resourcesData.setPowerSourcesPowerUsageRate(doubleObjectListConverter.convertObjectList(powerSourcesInformation.get("powerUsageRate"), Double.class));
        resourcesData.setPowerSourcesRemainingCapacityPercent(doubleObjectListConverter.convertObjectList(powerSourcesInformation.get("remainingCapacityPercent"), Double.class));

        CentralProcessor processor = this.hardware.getProcessor();
        resourcesData.setProcessorContextSwitches(processor.getContextSwitches());
        resourcesData.setProcessorInterrupts(processor.getInterrupts());

        return resourcesData;
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
            List<Long> readBytes = getReadBytesOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("readBytes", readBytes);

            List<Long> reads = getReadsOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("reads", reads);

            List<Long> writeBytes = getWriteBytesOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("writeBytes", writeBytes);

            List<Long> writes = getWritesOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("writes", writes);

            List<Long> partitionsMajorFaults = getPartitionsMajorFaultsOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("partitionsMajorFaults", partitionsMajorFaults);

            List<Long> partitionsMinorFaults = getPartitionsMinorFaultsOfDiskStore(diskStoresInformation, diskStore);
            diskStoresInformation.put("partitionsMinorFaults", partitionsMinorFaults);
        }
        return diskStoresInformation;
    }

    private List<Long> getReadBytesOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> readBytes;
        if (diskStoresInformation.get("readBytes") != null) {
            readBytes = diskStoresInformation.get("readBytes");
        } else {
            readBytes = new ArrayList<>();
        }
        readBytes.add(diskStore.getReadBytes());
        return readBytes;
    }

    private List<Long> getReadsOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> reads;
        if (diskStoresInformation.get("reads") != null) {
            reads = diskStoresInformation.get("reads");
        } else {
            reads = new ArrayList<>();
        }
        reads.add(diskStore.getReads());
        return reads;
    }

    private List<Long> getWriteBytesOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> writeBytes;
        if (diskStoresInformation.get("writeBytes") != null) {
            writeBytes = diskStoresInformation.get("writeBytes");
        } else {
            writeBytes = new ArrayList<>();
        }
        writeBytes.add(diskStore.getWriteBytes());
        return writeBytes;
    }

    private List<Long> getWritesOfDiskStore(Map<String, List<Long>> diskStoresInformation, HWDiskStore diskStore) {
        List<Long> writes;
        if (diskStoresInformation.get("writes") != null) {
            writes = diskStoresInformation.get("writes");
        } else {
            writes = new ArrayList<>();
        }
        writes.add(diskStore.getWrites());
        return writes;
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

    private Map<String, List<Long>> getNetworkInterfacesInformation(List<NetworkIF> networkInterfaces) {
        Map<String, List<Long>> networkInterfacesInformation = new HashMap<>();
        for (NetworkIF networkInterface : networkInterfaces) {
            List<Long> bytesReceived = getBytesReceivedOfNetworkInterface(networkInterfacesInformation, networkInterface);
            networkInterfacesInformation.put("bytesReceived", bytesReceived);

            List<Long> bytesSent = getBytesSentOfNetworkInterface(networkInterfacesInformation, networkInterface);
            networkInterfacesInformation.put("bytesSent", bytesSent);

            List<Long> collisions = getCollisionsOfNetworkInterface(networkInterfacesInformation, networkInterface);
            networkInterfacesInformation.put("collisions", collisions);

            List<Long> packetsReceived = getPacketsReceivedOfNetworkInterface(networkInterfacesInformation, networkInterface);
            networkInterfacesInformation.put("packetsReceived", packetsReceived);

            List<Long> packetsSent = getPacketsSentOfNetworkInterface(networkInterfacesInformation, networkInterface);
            networkInterfacesInformation.put("packetsSent", packetsSent);
        }
        return networkInterfacesInformation;
    }

    private List<Long> getBytesReceivedOfNetworkInterface(Map<String, List<Long>> networkInterfacesInformation, NetworkIF networkInterface) {
        List<Long> bytesReceived;
        if (networkInterfacesInformation.get("bytesReceived") != null) {
            bytesReceived = networkInterfacesInformation.get("bytesReceived");
        } else {
            bytesReceived = new ArrayList<>();
        }
        bytesReceived.add(networkInterface.getBytesRecv());
        return bytesReceived;
    }

    private List<Long> getBytesSentOfNetworkInterface(Map<String, List<Long>> networkInterfacesInformation, NetworkIF networkInterface) {
        List<Long> bytesSent;
        if (networkInterfacesInformation.get("bytesSent") != null) {
            bytesSent = networkInterfacesInformation.get("bytesSent");
        } else {
            bytesSent = new ArrayList<>();
        }
        bytesSent.add(networkInterface.getBytesSent());
        return bytesSent;
    }

    private List<Long> getCollisionsOfNetworkInterface(Map<String, List<Long>> networkInterfacesInformation, NetworkIF networkInterface) {
        List<Long> collisions;
        if (networkInterfacesInformation.get("collisions") != null) {
            collisions = networkInterfacesInformation.get("collisions");
        } else {
            collisions = new ArrayList<>();
        }
        collisions.add(networkInterface.getCollisions());
        return collisions;
    }

    private List<Long> getPacketsReceivedOfNetworkInterface(Map<String, List<Long>> networkInterfacesInformation, NetworkIF networkInterface) {
        List<Long> packetsReceived;
        if (networkInterfacesInformation.get("packetsReceived") != null) {
            packetsReceived = networkInterfacesInformation.get("packetsReceived");
        } else {
            packetsReceived = new ArrayList<>();
        }
        packetsReceived.add(networkInterface.getPacketsRecv());
        return packetsReceived;
    }

    private List<Long> getPacketsSentOfNetworkInterface(Map<String, List<Long>> networkInterfacesInformation, NetworkIF networkInterface) {
        List<Long> packetsSent;
        if (networkInterfacesInformation.get("packetsSent") != null) {
            packetsSent = networkInterfacesInformation.get("packetsSent");
        } else {
            packetsSent = new ArrayList<>();
        }
        packetsSent.add(networkInterface.getPacketsSent());
        return packetsSent;
    }

    private Map<String, List<Object>> getPowerSourcesInformation(List<PowerSource> powerSources) {
        Map<String, List<Object>> powerSourcesInformation = new HashMap<>();
        for (PowerSource powerSource : powerSources) {
            List<Object> charging = getChargingOfPowerSource(powerSourcesInformation, powerSource);
            powerSourcesInformation.put("charging", charging);

            List<Object> discharging = getDischargingOfPowerSource(powerSourcesInformation, powerSource);
            powerSourcesInformation.put("discharging", discharging);

            List<Object> powerOnLine = getPowerOnLineOfPowerSource(powerSourcesInformation, powerSource);
            powerSourcesInformation.put("powerOnLine", powerOnLine);

            List<Object> powerUsageRate = getPowerUsageRateOfPowerSource(powerSourcesInformation, powerSource);
            powerSourcesInformation.put("powerUsageRate", powerUsageRate);

            List<Object> remainingCapacityPercent = getRemainingCapacityPercentOfPowerSource(powerSourcesInformation, powerSource);
            powerSourcesInformation.put("remainingCapacityPercent", remainingCapacityPercent);
        }
        return powerSourcesInformation;
    }

    private List<Object> getChargingOfPowerSource(Map<String, List<Object>> powerSourcesInformation, PowerSource powerSource) {
        List<Object> charging;
        if (powerSourcesInformation.get("charging") != null) {
            charging = powerSourcesInformation.get("charging");
        } else {
            charging = new ArrayList<>();
        }
        charging.add(powerSource.isCharging());
        return charging;
    }

    private List<Object> getDischargingOfPowerSource(Map<String, List<Object>> powerSourcesInformation, PowerSource powerSource) {
        List<Object> discharging;
        if (powerSourcesInformation.get("discharging") != null) {
            discharging = powerSourcesInformation.get("discharging");
        } else {
            discharging = new ArrayList<>();
        }
        discharging.add(powerSource.isDischarging());
        return discharging;
    }

    private List<Object> getPowerOnLineOfPowerSource(Map<String, List<Object>> powerSourcesInformation, PowerSource powerSource) {
        List<Object> powerOnLine;
        if (powerSourcesInformation.get("powerOnLine") != null) {
            powerOnLine = powerSourcesInformation.get("powerOnLine");
        } else {
            powerOnLine = new ArrayList<>();
        }
        powerOnLine.add(powerSource.isPowerOnLine());
        return powerOnLine;
    }

    private List<Object> getPowerUsageRateOfPowerSource(Map<String, List<Object>> powerSourcesInformation, PowerSource powerSource) {
        List<Object> powerUsageRate;
        if (powerSourcesInformation.get("powerUsageRate") != null) {
            powerUsageRate = powerSourcesInformation.get("powerUsageRate");
        } else {
            powerUsageRate = new ArrayList<>();
        }
        powerUsageRate.add(powerSource.getPowerUsageRate());
        return powerUsageRate;
    }

    private List<Object> getRemainingCapacityPercentOfPowerSource(Map<String, List<Object>> powerSourcesInformation, PowerSource powerSource) {
        List<Object> remainingCapacityPercent;
        if (powerSourcesInformation.get("remainingCapacityPercent") != null) {
            remainingCapacityPercent = powerSourcesInformation.get("remainingCapacityPercent");
        } else {
            remainingCapacityPercent = new ArrayList<>();
        }
        remainingCapacityPercent.add(powerSource.getRemainingCapacityPercent());
        return remainingCapacityPercent;
    }
}
