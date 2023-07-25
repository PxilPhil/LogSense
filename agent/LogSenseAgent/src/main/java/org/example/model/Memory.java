package org.example.model;

public class Memory {
    private long totalSize;
    private long pageSize;

    public Memory() {
    }

    public Memory(long totalSize, long pageSize) {
        this.totalSize = totalSize;
        this.pageSize = pageSize;
    }

    public long getTotalSize() {
        return totalSize;
    }

    public void setTotalSize(long totalSize) {
        this.totalSize = totalSize;
    }

    public long getPageSize() {
        return pageSize;
    }

    public void setPageSize(long pageSize) {
        this.pageSize = pageSize;
    }
}