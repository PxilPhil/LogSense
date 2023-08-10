package org.example.model;

import java.util.Objects;

public record Partition(
        long timestamp,
        String diskStoreName,
        String identification,
        String name,
        String type,
        String mountPoint,
        long size,
        long majorFaults,
        long minorFaults
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Partition partition = (Partition) o;
        return size == partition.size && majorFaults == partition.majorFaults && minorFaults == partition.minorFaults && Objects.equals(diskStoreName, partition.diskStoreName) && Objects.equals(identification, partition.identification) && Objects.equals(name, partition.name) && Objects.equals(type, partition.type) && Objects.equals(mountPoint, partition.mountPoint);
    }
}
