package org.example.model;

public class DiskStore {
    private String model;
    private String name;
    private long size;

    public DiskStore() {
    }

    public DiskStore(String model, String name, long size) {
        this.model = model;
        this.name = name;
        this.size = size;
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
}
