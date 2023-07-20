package org.example.model;

import java.util.List;

public class Resources {
    private long freeDiskSpace;
    private List<Long> readBytesDiskStores;
    private List<Long> readsDiskStores;
    private List<Long> writeBytesDiskStores;

    private List<Long> writesDiskStores;
    private List<Long> partitionsMajorFaults;   //numbers are sorted by disk store then by partition
    private List<Long> partitionsMinorFaults;   //numbers are sorted by disk store then by partition
    private long availableMemory;
    private List<String> powerSourcesNames;
    private List<Boolean> powerSourcesCharging;
    private List<Boolean> powerSourcesDischarging;
    private List<Boolean> powerSourcesPowerOnLine;
    private List<Double> powerSourcesRemainingCapacityPercent;
    private long processorContextSwitches;
    private long processorInterrupts;

    public Resources() {
    }

    public Resources(long freeDiskSpace, List<Long> readBytesDiskStores, List<Long> readsDiskStores, List<Long> writeBytesDiskStores, List<Long> writesDiskStores, List<Long> partitionsMajorFaults, List<Long> partitionsMinorFaults, long availableMemory, List<String> powerSourcesNames, List<Boolean> powerSourcesCharging, List<Boolean> powerSourcesDischarging, List<Boolean> powerSourcesPowerOnLine, List<Double> powerSourcesRemainingCapacityPercent, long processorContextSwitches, long processorInterrupts) {
        this.freeDiskSpace = freeDiskSpace;
        this.readBytesDiskStores = readBytesDiskStores;
        this.readsDiskStores = readsDiskStores;
        this.writeBytesDiskStores = writeBytesDiskStores;
        this.writesDiskStores = writesDiskStores;
        this.partitionsMajorFaults = partitionsMajorFaults;
        this.partitionsMinorFaults = partitionsMinorFaults;
        this.availableMemory = availableMemory;
        this.powerSourcesNames = powerSourcesNames;
        this.powerSourcesCharging = powerSourcesCharging;
        this.powerSourcesDischarging = powerSourcesDischarging;
        this.powerSourcesPowerOnLine = powerSourcesPowerOnLine;
        this.powerSourcesRemainingCapacityPercent = powerSourcesRemainingCapacityPercent;
        this.processorContextSwitches = processorContextSwitches;
        this.processorInterrupts = processorInterrupts;
    }

    public long getFreeDiskSpace() {
        return freeDiskSpace;
    }

    public void setFreeDiskSpace(long freeDiskSpace) {
        this.freeDiskSpace = freeDiskSpace;
    }

    public List<Long> getReadBytesDiskStores() {
        return readBytesDiskStores;
    }

    public void setReadBytesDiskStores(List<Long> readBytesDiskStores) {
        this.readBytesDiskStores = readBytesDiskStores;
    }

    public List<Long> getReadsDiskStores() {
        return readsDiskStores;
    }

    public void setReadsDiskStores(List<Long> readsDiskStores) {
        this.readsDiskStores = readsDiskStores;
    }

    public List<Long> getWriteBytesDiskStores() {
        return writeBytesDiskStores;
    }

    public void setWriteBytesDiskStores(List<Long> writeBytesDiskStores) {
        this.writeBytesDiskStores = writeBytesDiskStores;
    }

    public List<Long> getWritesDiskStores() {
        return writesDiskStores;
    }

    public void setWritesDiskStores(List<Long> writesDiskStores) {
        this.writesDiskStores = writesDiskStores;
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

    public List<String> getPowerSourcesNames() {
        return powerSourcesNames;
    }

    public void setPowerSourcesNames(List<String> powerSourcesNames) {
        this.powerSourcesNames = powerSourcesNames;
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
