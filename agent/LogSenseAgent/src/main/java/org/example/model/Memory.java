package org.example.model;

import java.util.Objects;

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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Memory memory = (Memory) o;
        return totalSize == memory.totalSize && pageSize == memory.pageSize;
    }
}
