package org.example.model;

import java.util.Objects;

public record DiskStore(
        long timestamp,
        String serialNumber,
        String model,
        String name,
        long size
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DiskStore diskStore = (DiskStore) o;
        return size == diskStore.size && Objects.equals(serialNumber, diskStore.serialNumber) && Objects.equals(model, diskStore.model) && Objects.equals(name, diskStore.name);
    }
}
