package org.example.model;

public class Partition {
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

    public Partition(String diskStoreName, String identification, String name, String type, String mountPoint, long size, long majorFaults, long minorFaults) {
        this.diskStoreName = diskStoreName;
        this.identification = identification;
        this.name = name;
        this.type = type;
        this.mountPoint = mountPoint;
        this.size = size;
        this.majorFaults = majorFaults;
        this.minorFaults = minorFaults;
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
}
