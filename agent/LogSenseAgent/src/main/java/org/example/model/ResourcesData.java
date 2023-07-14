package org.example.model;

import java.util.List;

public class ResourcesData {
    private long freeDiskSpace;
    private List<Long> diskStoresReadBytes;
    private List<Long> diskStoresReads;
    private List<Long> diskStoresWriteBytes;
    private List<Long> diskStoresWrites;
    private List<Long> partitionsMajorFaults; //numbers are sorted by disk store then by partition
    private List<Long> partitionsMinorFaults;
    private long availableMemory;
    private List<Long> networkInterfacesBytesReceived;
    private List<Long> networkInterfacesBytesSent;
    private List<Long> networkInterfacesCollisions;
    private List<Long> networkInterfacesPacketsReceived;
    private List<Long> networkInterfacesPacketsSent;
    private List<Boolean> powerSourcesCharging;
    private List<Boolean> powerSourcesDischarging;
    private List<Boolean> powerSourcesPowerOnLine;
    private List<Double> powerSourcesPowerUsageRate;
    private List<Double> powerSourcesRemainingCapacityPercent;
    private long processorContextSwitches;
    private long processorInterrupts;

    public long getFreeDiskSpace() {
        return freeDiskSpace;
    }

    public void setFreeDiskSpace(long freeDiskSpace) {
        this.freeDiskSpace = freeDiskSpace;
    }

    public List<Long> getDiskStoresReadBytes() {
        return diskStoresReadBytes;
    }

    public void setDiskStoresReadBytes(List<Long> diskStoresReadBytes) {
        this.diskStoresReadBytes = diskStoresReadBytes;
    }

    public List<Long> getDiskStoresReads() {
        return diskStoresReads;
    }

    public void setDiskStoresReads(List<Long> diskStoresReads) {
        this.diskStoresReads = diskStoresReads;
    }

    public List<Long> getDiskStoresWriteBytes() {
        return diskStoresWriteBytes;
    }

    public void setDiskStoresWriteBytes(List<Long> diskStoresWriteBytes) {
        this.diskStoresWriteBytes = diskStoresWriteBytes;
    }

    public List<Long> getDiskStoresWrites() {
        return diskStoresWrites;
    }

    public void setDiskStoresWrites(List<Long> diskStoresWrites) {
        this.diskStoresWrites = diskStoresWrites;
    }

    public List<Long> getPartitionsMajorFaults() {
        return partitionsMajorFaults;
    }

    public void setPartitionsMajorFaults(List<Long> partitionsMajorFaults) {
        this.partitionsMajorFaults = partitionsMajorFaults;
    }

    public List<Long> getPartitionsMinorFaults() {
        return partitionsMinorFaults;
    }

    public void setPartitionsMinorFaults(List<Long> partitionsMinorFaults) {
        this.partitionsMinorFaults = partitionsMinorFaults;
    }

    public long getAvailableMemory() {
        return availableMemory;
    }

    public void setAvailableMemory(long availableMemory) {
        this.availableMemory = availableMemory;
    }

    public List<Long> getNetworkInterfacesBytesReceived() {
        return networkInterfacesBytesReceived;
    }

    public void setNetworkInterfacesBytesReceived(List<Long> networkInterfacesBytesReceived) {
        this.networkInterfacesBytesReceived = networkInterfacesBytesReceived;
    }

    public List<Long> getNetworkInterfacesBytesSent() {
        return networkInterfacesBytesSent;
    }

    public void setNetworkInterfacesBytesSent(List<Long> networkInterfacesBytesSent) {
        this.networkInterfacesBytesSent = networkInterfacesBytesSent;
    }

    public List<Long> getNetworkInterfacesCollisions() {
        return networkInterfacesCollisions;
    }

    public void setNetworkInterfacesCollisions(List<Long> networkInterfacesCollisions) {
        this.networkInterfacesCollisions = networkInterfacesCollisions;
    }

    public List<Long> getNetworkInterfacesPacketsReceived() {
        return networkInterfacesPacketsReceived;
    }

    public void setNetworkInterfacesPacketsReceived(List<Long> networkInterfacesPacketsReceived) {
        this.networkInterfacesPacketsReceived = networkInterfacesPacketsReceived;
    }

    public List<Long> getNetworkInterfacesPacketsSent() {
        return networkInterfacesPacketsSent;
    }

    public void setNetworkInterfacesPacketsSent(List<Long> networkInterfacesPacketsSent) {
        this.networkInterfacesPacketsSent = networkInterfacesPacketsSent;
    }

    public List<Boolean> getPowerSourcesCharging() {
        return powerSourcesCharging;
    }

    public void setPowerSourcesCharging(List<Boolean> powerSourcesCharging) {
        this.powerSourcesCharging = powerSourcesCharging;
    }

    public List<Boolean> getPowerSourcesDischarging() {
        return powerSourcesDischarging;
    }

    public void setPowerSourcesDischarging(List<Boolean> powerSourcesDischarging) {
        this.powerSourcesDischarging = powerSourcesDischarging;
    }

    public List<Boolean> getPowerSourcesPowerOnLine() {
        return powerSourcesPowerOnLine;
    }

    public void setPowerSourcesPowerOnLine(List<Boolean> powerSourcesPowerOnLine) {
        this.powerSourcesPowerOnLine = powerSourcesPowerOnLine;
    }

    public List<Double> getPowerSourcesPowerUsageRate() {
        return powerSourcesPowerUsageRate;
    }

    public void setPowerSourcesPowerUsageRate(List<Double> powerSourcesPowerUsageRate) {
        this.powerSourcesPowerUsageRate = powerSourcesPowerUsageRate;
    }

    public List<Double> getPowerSourcesRemainingCapacityPercent() {
        return powerSourcesRemainingCapacityPercent;
    }

    public void setPowerSourcesRemainingCapacityPercent(List<Double> powerSourcesRemainingCapacityPercent) {
        this.powerSourcesRemainingCapacityPercent = powerSourcesRemainingCapacityPercent;
    }

    public long getProcessorContextSwitches() {
        return processorContextSwitches;
    }

    public void setProcessorContextSwitches(long processorContextSwitches) {
        this.processorContextSwitches = processorContextSwitches;
    }

    public long getProcessorInterrupts() {
        return processorInterrupts;
    }

    public void setProcessorInterrupts(long processorInterrupts) {
        this.processorInterrupts = processorInterrupts;
    }
}
