package org.example.model;

public record Memory(
        long totalSize,
        long pageSize
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Memory memory = (Memory) o;
        return totalSize == memory.totalSize && pageSize == memory.pageSize;
    }
}