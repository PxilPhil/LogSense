package org.example.controller;

import org.example.analysis.StatService;
import org.example.api.ApiClient;
import org.example.converter.CSVDataConverter;
import org.example.model.*;
import org.example.monitor.Monitor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import oshi.software.os.OSProcess;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Agent {
    private static final Logger LOGGER = LoggerFactory.getLogger(Agent.class);
    private final Monitor monitor;
    private final StatService statService;
    private final CSVDataConverter csvDataConverter;
    private final ApiClient apiClient;
    private int stateId;
    private SessionComputerData sessionComputerData;
    private long measuringCount;

    public Agent() {
        this.statService = new StatService();
        this.monitor = new Monitor();
        this.csvDataConverter = new CSVDataConverter();
        this.apiClient = new ApiClient();
        this.sessionComputerData = null;
        this.measuringCount = 0;
    }

    public void monitor() {
        long timestamp = Instant.now().toEpochMilli();
        monitorSessionComputerData();

        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(() -> monitorData(timestamp), 0, 10, TimeUnit.SECONDS);
    }

    private void monitorData(long timestamp) {
        this.measuringCount++;
        getAndIngestOSProcesses(timestamp);
        if (this.measuringCount % 6 == 0) {     // if 60 seconds passed --> get running data + send data to rest api
            List<Application> analysedApplications = this.statService.analyseApplicationMeasurements(timestamp);
            monitorRunningData(analysedApplications, timestamp);
            monitorSessionComputerData();
        }
    }

    private void getAndIngestOSProcesses(long timestamp) {
        List<OSProcess> osProcesses = this.monitor.monitorProcesses();
        this.statService.ingestData(timestamp, osProcesses);
    }

    private void monitorSessionComputerData() {
        Client client = getClientData();
        List<DiskStore> diskStores = getDiskStores();
        List<Partition> partitions = getPartitions();

        if (this.sessionComputerData == null || hasClientDataChanged(client) || haveDiskStoresChanged(diskStores) || havePartitionsChanged(partitions)) {     // session computer data has never been set --> initial data that starts a new "session"
            SessionComputerData sessionComputerData = new SessionComputerData();
            sessionComputerData.setClient_data(this.csvDataConverter.convertClientData(client));
            sessionComputerData.setDisks(this.csvDataConverter.convertDiskStoreData(diskStores));
            sessionComputerData.setPartition(this.csvDataConverter.convertPartitionData(partitions));

            int stateId = this.apiClient.postSessionComputerData(sessionComputerData);
            if (stateId > 0) {
                this.stateId = stateId;
            } else {
                //TODO: stop agent --> there is no computer in the system with the same hardwareUUID --> user has to register first via the frontend
            }

            this.sessionComputerData = sessionComputerData;
        }
    }

    private Client getClientData() {
        Client client = this.monitor.monitorClientData();
        if (client == null) {
            LOGGER.error("Error while monitoring the client data: the client data object is null. Therefore the data can not be sent to the server.");
        }
        return client;
    }

    private List<DiskStore> getDiskStores() {
        List<DiskStore> diskStores = this.monitor.monitorDiskStores();
        if (diskStores == null) {
            LOGGER.error("Error while monitoring the disk stores: the list of disk stores is null. Therefore the data can not be sent to the server.");
        }
        return diskStores;
    }

    private List<Partition> getPartitions() {
        List<Partition> partitions = this.monitor.monitorPartitions();
        if (partitions == null) {
            LOGGER.error("Error while monitoring the partitions: the list of partitions is null. Therefore the data can not be sent to the server");
        }
        return partitions;
    }

    private boolean hasClientDataChanged(Client client) {
        String clientCSV = this.csvDataConverter.convertClientData(client);
        return !clientCSV.equals(this.sessionComputerData.getClient_data());
    }

    private boolean haveDiskStoresChanged(List<DiskStore> diskStores) {
        String diskStoresCSV = this.csvDataConverter.convertDiskStoreData(diskStores);
        return !diskStoresCSV.equals(this.sessionComputerData.getDisks());
    }

    private boolean havePartitionsChanged(List<Partition> partitions) {
        String partitionsCSV = this.csvDataConverter.convertPartitionData(partitions);
        return !partitionsCSV.equals(this.sessionComputerData.getPartition());
    }

    private void monitorRunningData(List<Application> analysedApplications, long timestamp) {
        Resources resources = getResources();
        List<NetworkInterface> networkInterfaces = getNetworkInterfaces();
        List<Connection> connections = getIpConnections();

        RunningData runningData = new RunningData();
        runningData.setApplication_data(this.csvDataConverter.convertApplicationData(timestamp, analysedApplications));
        runningData.setPc_resources(this.csvDataConverter.convertResourceData(timestamp, resources));
        runningData.setNetwork_interface(this.csvDataConverter.convertNetworkInterfacesData(timestamp, networkInterfaces));
        runningData.setConnection_data(this.csvDataConverter.convertConnectionData(timestamp, connections));

        this.apiClient.postRunningData(runningData, this.stateId);
    }

    private Resources getResources() {
        Resources resourceData = this.monitor.monitorResources();
        if (resourceData == null) {
            LOGGER.error("Error while monitoring the resources: the resources data object is null. Therefore the data can not be sent to the server.");
        }
        return resourceData;
    }

    private List<NetworkInterface> getNetworkInterfaces() {
        List<NetworkInterface> networkInterfaces = this.monitor.monitorNetworkInterfaces();
        if (networkInterfaces == null) {
            LOGGER.error("Error while monitoring the network interfaces: the list of network interfaces is null. Therefore the data can not be sent to the server.");
        }
        return networkInterfaces;
    }

    private List<Connection> getIpConnections() {
        List<Connection> connectionData = this.monitor.monitorIpConnections();
        if (connectionData == null) {
            LOGGER.error("Error while monitoring the IP connections: the list of connections is null. Therefore the data can not be sent to the server.");
        }
        return connectionData;
    }
}
