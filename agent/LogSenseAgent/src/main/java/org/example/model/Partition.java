package org.example.model;

import java.util.Objects;

public class Partition {

    private final long timestamp;
    private final String diskStoreName;
    private final String identification;
    private final String name;
    private final String type;
    private final String mountPoint;
    private final long size;
    private final long majorFaults;
    private final long minorFaults;

    public Partition(long timestamp, String diskStoreName, String identification, String name, String type,
                     String mountPoint, long size, long majorFaults, long minorFaults) {
        this.timestamp = timestamp;
        this.diskStoreName = diskStoreName;
        this.identification = identification;
        this.name = name;
        this.type = type;
        this.mountPoint = mountPoint;
        this.size = size;
        this.majorFaults = majorFaults;
        this.minorFaults = minorFaults;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public String getDiskStoreName() {
        return diskStoreName;
    }

    public String getIdentification() {
        return identification;
    }

    public String getName() {
        return name;
    }

    public String getType() {
        return type;
    }

    public String getMountPoint() {
        return mountPoint;
    }

    public long getSize() {
        return size;
    }

    public long getMajorFaults() {
        return majorFaults;
    }

    public long getMinorFaults() {
        return minorFaults;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Partition partition = (Partition) o;
        return size == partition.size
                && majorFaults == partition.majorFaults
                && minorFaults == partition.minorFaults
                && Objects.equals(diskStoreName, partition.diskStoreName)
                && Objects.equals(identification, partition.identification)
                && Objects.equals(name, partition.name)
                && Objects.equals(type, partition.type)
                && Objects.equals(mountPoint, partition.mountPoint);
    }
}
