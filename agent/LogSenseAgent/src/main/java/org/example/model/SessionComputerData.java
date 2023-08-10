package org.example.model;

import java.util.List;

public record SessionComputerData(
        Client client,
        List<DiskStore> diskStores,
        List<Partition> partitions
) {
}
