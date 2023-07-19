package org.example.model;

public class DiskStore {
    private String model;
    private String name;
    private long size;
    private long readBytes;
    private long reads;
    private long writeBytes;
    private long writes;

    public DiskStore() {
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

    public long getReadBytes() {
        return readBytes;
    }

    public void setReadBytes(long readBytes) {
        this.readBytes = readBytes;
    }

    public long getReads() {
        return reads;
    }

    public void setReads(long reads) {
        this.reads = reads;
    }

    public long getWriteBytes() {
        return writeBytes;
    }

    public void setWriteBytes(long writeBytes) {
        this.writeBytes = writeBytes;
    }

    public long getWrites() {
        return writes;
    }

    public void setWrites(long writes) {
        this.writes = writes;
    }
}
