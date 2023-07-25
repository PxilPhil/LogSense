package org.example.model;

public class SessionComputerData {
    private String client_data;
    private String disks;
    private String partition;

    public SessionComputerData() {
    }

    public String getClient_data() {
        return client_data;
    }

    public void setClient_data(String client_data) {
        this.client_data = client_data;
    }

    public String getDisks() {
        return disks;
    }

    public void setDisks(String disks) {
        this.disks = disks;
    }

    public String getPartition() {
        return partition;
    }

    public void setPartition(String partition) {
        this.partition = partition;
    }
}
