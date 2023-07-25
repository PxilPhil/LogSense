package org.example.model;

public class RunningData {
    private String pc_resources;
    private String connection_data;
    private String application_data;
    private String network_interface;

    public RunningData() {
    }

    public String getPc_resources() {
        return pc_resources;
    }

    public void setPc_resources(String pc_resources) {
        this.pc_resources = pc_resources;
    }

    public String getConnection_data() {
        return connection_data;
    }

    public void setConnection_data(String connection_data) {
        this.connection_data = connection_data;
    }

    public String getApplication_data() {
        return application_data;
    }

    public void setApplication_data(String application_data) {
        this.application_data = application_data;
    }

    public String getNetwork_interface() {
        return network_interface;
    }

    public void setNetwork_interface(String network_interface) {
        this.network_interface = network_interface;
    }
}
