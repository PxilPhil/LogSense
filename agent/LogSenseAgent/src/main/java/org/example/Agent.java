package org.example;

import com.opencsv.CSVWriter;
import oshi.SystemInfo;
import oshi.hardware.*;
import oshi.software.os.InternetProtocolStats;
import oshi.software.os.OSFileStore;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Agent {
    StatService statService = new StatService();
    public void monitor() {
        SystemInfo systemInfo = new SystemInfo();
        HardwareAbstractionLayer hal = systemInfo.getHardware();
        OperatingSystem operatingSystem = systemInfo.getOperatingSystem();
        operatingSystem.getSystemUptime();

        while (true) {
            writeProcessDataToCsv(operatingSystem);
            writeResourceDataToCsv(operatingSystem, hal);
            writeIpConnectionsToCsv(operatingSystem);
            try {
                TimeUnit.SECONDS.sleep(10);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private void writeProcessDataToCsv(OperatingSystem operatingSystem) { //TODO: deprecated once its moved to WritingService
        long timestamp = Instant.now().toEpochMilli();
        List<OSProcess> osProcesses = operatingSystem.getProcesses();
        statService.ingestData(timestamp, osProcesses);
    }


    private void writeResourceDataToCsv(OperatingSystem operatingSystem, HardwareAbstractionLayer hal) {
        List<String[]> resourceData = new ArrayList<>();
        String[] processHeaders = {"timestamp", "totalDiskSpace", "freeDiskSpace", "readBytesDiskStores", "readsDiskStores", "writeBytesDiskStores", "writesDiskStores", "partitionsMajorFaults", "partitionsMinorFaults", "totalMemory", "availableMemory", "bytesReceivedNetworkInterfaces", "bytesSentNetworkInterfaces", "collisionsNetworkInterfaces", "packetsReceivedNetworkInterfaces", "packetsSentNetworkInterfaces", "chargingPowerSources", "dischargingPowerSources", "powerOnLinePowerSources", "powerUsageRatePowerSources", "remainingCapacityPercentPowerSources", "contextSwitchesProcessor", "interruptsProcessor"};
        resourceData.add(processHeaders);

        long timestamp = Instant.now().toEpochMilli();

        Map<String, Long> diskInformation = getDiskInformation(operatingSystem.getFileSystem().getFileStores());
        Map<String, String> diskStoresInformation = getDiskStoresInformationAsStrings(hal.getDiskStores());
        Map<String, Long> memoryInformation = getMemoryInformation(hal.getMemory());
        Map<String, String> networkInterfacesInformation = getNetworkInterfacesInformationAsStrings(hal.getNetworkIFs());
        Map<String, String> powerSourcesInformation = getPowerSourcesInformationAsString(hal.getPowerSources());
        Map<String, String> processorInformation = getProcessorInformation(hal.getProcessor());
        String[] record = {String.valueOf(timestamp), String.valueOf(diskInformation.get("totalDiskSpace")), String.valueOf(diskInformation.get("freeDiskSpace")), diskStoresInformation.get("readBytes"), diskStoresInformation.get("reads"), diskStoresInformation.get("writeBytes"), diskStoresInformation.get("writes"), diskStoresInformation.get("partitionsMajorFaults"), diskStoresInformation.get("partitionsMinorFaults"), String.valueOf(memoryInformation.get("totalMemory")), String.valueOf(memoryInformation.get("availableMemory")), networkInterfacesInformation.get("bytesReceived"), networkInterfacesInformation.get("bytesSent"), networkInterfacesInformation.get("collisions"), networkInterfacesInformation.get("packetsReceived"), networkInterfacesInformation.get("packetsSent"), powerSourcesInformation.get("charging"), powerSourcesInformation.get("discharging"), powerSourcesInformation.get("powerOnLine"), powerSourcesInformation.get("powerUsageRate"), powerSourcesInformation.get("remainingCapacityPercent"), processorInformation.get("contextSwitches"), processorInformation.get("interrupts")};
        resourceData.add(record);

        try {
            CSVWriter writer = new CSVWriter(new FileWriter("C:\\test\\resource_" + timestamp + ".csv"));
            writer.writeAll(resourceData);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private Map<String, Long> getDiskInformation(List<OSFileStore> fileStores) {
        Map<String, Long> diskInformation = new HashMap<>();
        for (OSFileStore fileStore : fileStores) {
            diskInformation.put("totalDiskSpace", (diskInformation.get("totalDiskSpace") != null ? diskInformation.get("totalDiskSpace") : 0) + fileStore.getTotalSpace());
            diskInformation.put("freeDiskSpace", (diskInformation.get("freeDiskSpace") != null ? diskInformation.get("freeDiskSpace") : 0) + fileStore.getFreeSpace());
        }
        return diskInformation;
    }

    private Map<String, String> getDiskStoresInformationAsStrings(List<HWDiskStore> diskStores) {
        Map<String, String> diskStoresInformation = new HashMap<>();
        for (HWDiskStore diskStore : diskStores) {
            diskStoresInformation.put("readBytes", (diskStoresInformation.get("readBytes") != null && !diskStoresInformation.get("readBytes").isEmpty() ? diskStoresInformation.get("readBytes") + " " : "") + diskStore.getReadBytes());
            diskStoresInformation.put("reads", (diskStoresInformation.get("reads") != null && !diskStoresInformation.get("reads").isEmpty() ? diskStoresInformation.get("reads") + " " : "") + diskStore.getReads());
            diskStoresInformation.put("writeBytes", (diskStoresInformation.get("writeBytes") != null && !diskStoresInformation.get("writeBytes").isEmpty() ? diskStoresInformation.get("writeBytes") + " " : "") + diskStore.getWriteBytes());
            diskStoresInformation.put("writes", (diskStoresInformation.get("writes") != null && !diskStoresInformation.get("writes").isEmpty() ? diskStoresInformation.get("writes") + " " : "") + diskStore.getWrites());
            for (HWPartition partition : diskStore.getPartitions()) {
                diskStoresInformation.put("partitionsMajorFaults", (diskStoresInformation.get("partitionsMajorFaults") != null && !diskStoresInformation.get("partitionsMajorFaults").isEmpty() ? diskStoresInformation.get("partitionsMajorFaults") + " " : "") + partition.getMajor());
                diskStoresInformation.put("partitionsMinorFaults", (diskStoresInformation.get("partitionsMinorFaults") != null && !diskStoresInformation.get("partitionsMinorFaults").isEmpty() ? diskStoresInformation.get("partitionsMinorFaults") + " " : "") + partition.getMinor());
            }
        }
        return diskStoresInformation;
    }

    private Map<String, Long> getMemoryInformation(GlobalMemory memory) {
        Map<String, Long> memoryInformation = new HashMap<>();
        memoryInformation.put("totalMemory", memory.getTotal());
        memoryInformation.put("availableMemory", memory.getAvailable());
        return memoryInformation;
    }

    private Map<String, String> getNetworkInterfacesInformationAsStrings(List<NetworkIF> networkInterfaces) {
        Map<String, String> networkInterfacesInformation = new HashMap<>();
        for (NetworkIF networkInterface : networkInterfaces) {
            networkInterfacesInformation.put("bytesReceived", (networkInterfacesInformation.get("bytesReceived") != null && !networkInterfacesInformation.get("bytesReceived").isEmpty() ? networkInterfacesInformation.get("bytesReceived") + " " : "") + networkInterface.getBytesRecv());
            networkInterfacesInformation.put("bytesSent", (networkInterfacesInformation.get("bytesSent") != null && !networkInterfacesInformation.get("bytesSent").isEmpty() ? networkInterfacesInformation.get("bytesSent") + " " : "") + networkInterface.getBytesSent());
            networkInterfacesInformation.put("collisions", (networkInterfacesInformation.get("collisions") != null && !networkInterfacesInformation.get("collisions").isEmpty() ? networkInterfacesInformation.get("collisions") + " " : "") + networkInterface.getCollisions());
            networkInterfacesInformation.put("packetsReceived", (networkInterfacesInformation.get("packetsReceived") != null && !networkInterfacesInformation.get("packetsReceived").isEmpty() ? networkInterfacesInformation.get("packetsReceived") + " " : "") + networkInterface.getPacketsRecv());
            networkInterfacesInformation.put("packetsSent", (networkInterfacesInformation.get("packetsSent") != null && !networkInterfacesInformation.get("packetsSent").isEmpty() ? networkInterfacesInformation.get("packetsSent") + " " : "") + networkInterface.getPacketsSent());
        }
        return networkInterfacesInformation;
    }

    private Map<String, String> getPowerSourcesInformationAsString(List<PowerSource> powerSources) {
        Map<String, String> powerSourcesInformation = new HashMap<>();
        for (PowerSource powerSource : powerSources) {
            powerSourcesInformation.put("charging", (powerSourcesInformation.get("charging") != null && !powerSourcesInformation.get("charging").isEmpty() ? powerSourcesInformation.get("charging") + " " : "") + powerSource.isCharging());
            powerSourcesInformation.put("discharging", (powerSourcesInformation.get("discharging") != null && !powerSourcesInformation.get("discharging").isEmpty() ? powerSourcesInformation.get("discharging") + " " : "") + powerSource.isDischarging());
            powerSourcesInformation.put("powerOnLine", (powerSourcesInformation.get("powerOnLine") != null && !powerSourcesInformation.get("powerOnLine").isEmpty() ? powerSourcesInformation.get("powerOnLine") + " " : "") + powerSource.isPowerOnLine());
            powerSourcesInformation.put("powerUsageRate", (powerSourcesInformation.get("powerUsageRate") != null && !powerSourcesInformation.get("powerUsageRate").isEmpty() ? powerSourcesInformation.get("powerUsageRate") + " " : "") + powerSource.getPowerUsageRate());
            powerSourcesInformation.put("remainingCapacityPercent", (powerSourcesInformation.get("remainingCapacityPercent") != null && !powerSourcesInformation.get("remainingCapacityPercent").isEmpty() ? powerSourcesInformation.get("remainingCapacityPercent") + " " : "") + powerSource.getRemainingCapacityPercent());
        }
        return powerSourcesInformation;
    }

    private Map<String, String> getProcessorInformation(CentralProcessor processor) {
        Map<String, String> processorInformation = new HashMap<>();
        processorInformation.put("contextSwitches", String.valueOf(processor.getContextSwitches()));
        processorInformation.put("interrupts", String.valueOf(processor.getInterrupts()));
        return processorInformation;
    }

    private void writeIpConnectionsToCsv(OperatingSystem operatingSystem) {
        List<String[]> ipConnections = new ArrayList<>();
        String[] ipConnectionHeaders = {"timestamp", "localPort", "foreignAddress", "foreignPort", "state", "type"};
        ipConnections.add(ipConnectionHeaders);

        long timestamp = Instant.now().toEpochMilli();
        for (InternetProtocolStats.IPConnection connection : operatingSystem.getInternetProtocolStats().getConnections()) {
            String[] record = new String[0];
            if (connection.getType().equals("tcp4")) {
                try {
                    record = new String[]{String.valueOf(timestamp), String.valueOf(connection.getLocalPort()), InetAddress.getByAddress(connection.getForeignAddress()).toString(), String.valueOf(connection.getForeignPort()), String.valueOf(connection.getState()), connection.getType()};
                } catch (UnknownHostException e) {
                    throw new RuntimeException(e);
                }
            }
            ipConnections.add(record);
        }

        try {
            CSVWriter writer = new CSVWriter(new FileWriter("C:\\test\\connection_" + timestamp + ".csv"));
            writer.writeAll(ipConnections);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
