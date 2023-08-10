package org.example.model;

import java.util.List;

public record Resources(
        Long freeDiskSpace,
        List<Long> readBytesDiskStores,
        List<Long> readsDiskStores,
        List<Long> writeBytesDiskStores,

        List<Long> writesDiskStores,
        List<Long> partitionsMajorFaults,   //numbers are sorted by disk store then by partition
        List<Long> partitionsMinorFaults,   //numbers are sorted by disk store then by partition
        Long availableMemory,
        List<String> powerSourcesNames,
        List<Boolean> powerSourcesCharging,
        List<Boolean> powerSourcesDischarging,
        List<Boolean> powerSourcesPowerOnLine,
        List<Double> powerSourcesRemainingCapacityPercent,
        Long processorContextSwitches,
        Long processorInterrupts
) {
}
