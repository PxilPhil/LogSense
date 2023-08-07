package org.example.model;

import java.util.Objects;

public class DiskStore {
    private long timestamp;
    private String serialNumber;
    private String model;
    private String name;
    private long size;

    public DiskStore() {
    }

    public DiskStore(long timestamp, String serialNumber, String model, String name, long size) {
        this.timestamp = timestamp;
        this.serialNumber = serialNumber;
        this.model = model;
        this.name = name;
        this.size = size;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public String getSerialNumber() {
        return serialNumber;
    }

    public void setSerialNumber(String serialNumber) {
        this.serialNumber = serialNumber;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public long getSize() {
        return size;
    }

    public void setSize(long size) {
        this.size = size;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DiskStore diskStore = (DiskStore) o;
        return size == diskStore.size && Objects.equals(serialNumber, diskStore.serialNumber) && Objects.equals(model, diskStore.model) && Objects.equals(name, diskStore.name);
    }
}
