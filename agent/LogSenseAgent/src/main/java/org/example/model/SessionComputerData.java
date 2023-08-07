package org.example.model;

import java.util.List;

public class SessionComputerData {
    private Client client;
    private List<DiskStore> diskStores;
    private List<Partition> partitions;

    public SessionComputerData() {
    }

    public SessionComputerData(Client client, List<DiskStore> diskStores, List<Partition> partitions) {
        this.client = client;
        this.diskStores = diskStores;
        this.partitions = partitions;
    }

    public Client getClient() {
        return client;
    }

    public void setClient(Client client) {
        this.client = client;
    }

    public List<DiskStore> getDiskStores() {
        return diskStores;
    }

    public void setDiskStores(List<DiskStore> diskStores) {
        this.diskStores = diskStores;
    }

    public List<Partition> getPartitions() {
        return partitions;
    }

    public void setPartitions(List<Partition> partitions) {
        this.partitions = partitions;
    }
}
