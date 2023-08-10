package org.example.model;

public class RunningData {
    
    private final String pc_resources;
    private final String connection_data;
    private final String application_data;
    private final String network_interface;

    public RunningData(String pc_resources, String connection_data, String application_data, String network_interface) {
        this.pc_resources = pc_resources;
        this.connection_data = connection_data;
        this.application_data = application_data;
        this.network_interface = network_interface;
    }

    // JR: use camelCase instead of snake_case ?
    public String getPc_resources() {
        return pc_resources;
    }

    public String getConnection_data() {
        return connection_data;
    }

    public String getApplication_data() {
        return application_data;
    }

    public String getNetwork_interface() {
        return network_interface;
    }
}
