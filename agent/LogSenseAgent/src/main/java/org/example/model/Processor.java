package org.example.model;

import java.util.Objects;

public record Processor(
        String name,
        String identifier,
        String ID,
        String vendor,
        int bitness,
        int physicalPackageCount,
        int physicalProcessorCount,
        int logicalProcessorCount
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Processor processor = (Processor) o;
        return bitness == processor.bitness && physicalPackageCount == processor.physicalPackageCount && physicalProcessorCount == processor.physicalProcessorCount && logicalProcessorCount == processor.logicalProcessorCount && Objects.equals(name, processor.name) && Objects.equals(identifier, processor.identifier) && Objects.equals(ID, processor.ID) && Objects.equals(vendor, processor.vendor);
    }
}
