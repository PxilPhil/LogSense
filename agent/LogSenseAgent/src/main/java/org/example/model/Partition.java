package org.example.model;

import java.util.Objects;

public class Partition {
    private long timestamp;
    private String diskStoreName;
    private String identification;
    private String name;
    private String type;
    private String mountPoint;
    private long size;
    private long majorFaults;
    private long minorFaults;

    public Partition() {
    }

    public Partition(long timestamp, String diskStoreName, String identification, String name, String type, String mountPoint, long size, long majorFaults, long minorFaults) {
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

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public String getDiskStoreName() {
        return diskStoreName;
    }

    public void setDiskStoreName(String diskStoreName) {
        this.diskStoreName = diskStoreName;
    }

    public String getIdentification() {
        return identification;
    }

    public void setIdentification(String identification) {
        this.identification = identification;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getMountPoint() {
        return mountPoint;
    }

    public void setMountPoint(String mountPoint) {
        this.mountPoint = mountPoint;
    }

    public long getSize() {
        return size;
    }

    public void setSize(long size) {
        this.size = size;
    }

    public long getMajorFaults() {
        return majorFaults;
    }

    public void setMajorFaults(long majorFaults) {
        this.majorFaults = majorFaults;
    }

    public long getMinorFaults() {
        return minorFaults;
    }

    public void setMinorFaults(long minorFaults) {
        this.minorFaults = minorFaults;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Partition partition = (Partition) o;
        return size == partition.size && majorFaults == partition.majorFaults && minorFaults == partition.minorFaults && Objects.equals(diskStoreName, partition.diskStoreName) && Objects.equals(identification, partition.identification) && Objects.equals(name, partition.name) && Objects.equals(type, partition.type) && Objects.equals(mountPoint, partition.mountPoint);
    }
}
