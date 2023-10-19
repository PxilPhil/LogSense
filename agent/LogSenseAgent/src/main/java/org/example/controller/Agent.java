package org.example.controller;

import org.example.analysis.StatService;
import org.example.api.ApiClient;
import org.example.converter.CSVDataConverter;
import org.example.model.Process;
import org.example.model.*;
import org.example.monitor.OshiMonitor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Agent {
    private static final Logger LOGGER = LoggerFactory.getLogger(Agent.class);

    private final OshiMonitor oshiMonitor;
    private final StatService statService;
    private final CSVDataConverter csvDataConverter;
    private final ApiClient apiClient;
    private final String supportedOperatingSystem;
    private int stateId;
    private SessionComputerData sessionComputerData;
    private long measuringCount;
    private long failedSessionComputerDataPostRequest;

    public Agent(String clientBaseUrl, String supportedOperatingSystem) {
        this.statService = new StatService();
        this.oshiMonitor = new OshiMonitor();
        this.csvDataConverter = new CSVDataConverter();
        this.apiClient = new ApiClient(clientBaseUrl);
        this.sessionComputerData = null;
        this.measuringCount = 0;
        this.failedSessionComputerDataPostRequest = 0;
        this.supportedOperatingSystem = supportedOperatingSystem;
    }

    public void monitor() {
        if (clientHasSupportedOperatingSystem()) {
            monitorSessionComputerData();

            ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
            scheduler.scheduleAtFixedRate(this::monitorData, 0, 10, TimeUnit.SECONDS);
        } else {
            LOGGER.error("The operating system of this client is not supported or could not be detected. " +
                    "Therefore the agent is not able to start and monitor your client.");
        }
    }

    private boolean clientHasSupportedOperatingSystem() {
        String operatingSystemFamily = this.oshiMonitor.monitorOperatingSystem();
        return operatingSystemFamily != null && operatingSystemFamily.equals(this.supportedOperatingSystem);
    }

    private void monitorData() {
        this.measuringCount++;
        long timestamp = Instant.now().toEpochMilli();
        getAndIngestOSProcesses(timestamp);
        if (this.measuringCount % 6 == 0) {     // if 60 seconds passed --> get running data + send data to rest api
            List<Application> analysedApplications = this.statService.analyseApplicationMeasurements(timestamp);

            monitorRunningData(analysedApplications, timestamp);
            monitorSessionComputerData();
        }
    }

    private void getAndIngestOSProcesses(long timestamp) {
        List<Process> processes = this.oshiMonitor.monitorProcesses();
        this.statService.ingestData(timestamp, processes);
    }

    private void monitorSessionComputerData() {
        Client client = getClientData();
        List<DiskStore> diskStores = getDiskStores();
        List<Partition> partitions = getPartitions();

        if (this.sessionComputerData == null || hasClientDataChanged(client) || haveDiskStoresChanged(diskStores)
                || havePartitionsChanged(partitions)) {     // session computer data has never been set --> initial data that starts a new "session"
            SessionComputerData sessionComputerData = new SessionComputerData(client, diskStores, partitions);

            int stateId = this.apiClient.postSessionComputerData(sessionComputerData);
            if (stateId > 0) {
                this.stateId = stateId;
            } else {
                this.failedSessionComputerDataPostRequest += 1;
                LOGGER.error("Error while sending the session computer data to the server: the hardware UUID of " +
                        "your device is not registered as a client on the server. Please register first in the " +
                        "web application.");
                try {
                    TimeUnit.SECONDS.sleep((long) Math.pow(2, this.failedSessionComputerDataPostRequest));
                } catch (InterruptedException e) {
                    LOGGER.error("Error while trying to resend the session computer data: " + e);
                }
                monitorSessionComputerData();
            }
            this.sessionComputerData = sessionComputerData;
        }
    }

    private Client getClientData() {
        Client client = this.oshiMonitor.monitorClientData();
        if (client == null) {
            LOGGER.error("Error while monitoring the client data: the client data object is null. " +
                    "Therefore the data can not be sent to the server.");
        }
        return client;
    }

    private List<DiskStore> getDiskStores() {
        List<DiskStore> diskStores = this.oshiMonitor.monitorDiskStores();
        if (diskStores == null) {
            LOGGER.error("Error while monitoring the disk stores: the list of disk stores is null. " +
                    "Therefore the data can not be sent to the server.");
        }
        return diskStores;
    }

    private List<Partition> getPartitions() {
        List<Partition> partitions = this.oshiMonitor.monitorPartitions();
        if (partitions == null) {
            LOGGER.error("Error while monitoring the partitions: the list of partitions is null. " +
                    "Therefore the data can not be sent to the server");
        }
        return partitions;
    }

    private boolean hasClientDataChanged(Client client) {
        return !client.equals(this.sessionComputerData.client());
    }

    private boolean haveDiskStoresChanged(List<DiskStore> diskStores) {
        return !diskStores.equals(this.sessionComputerData.diskStores());
    }

    private boolean havePartitionsChanged(List<Partition> partitions) {
        return !partitions.equals(this.sessionComputerData.partitions());
    }

    private void monitorRunningData(List<Application> analysedApplications, long timestamp) {
        Resources resources = getResources();
        List<NetworkInterface> networkInterfaces = getNetworkInterfaces();
        List<Connection> connections = getIpConnections();

        RunningData runningData = new RunningData(this.csvDataConverter
                .convertApplicationData(timestamp, analysedApplications),
                this.csvDataConverter.convertResourceData(timestamp, resources),
                this.csvDataConverter.convertNetworkInterfacesData(timestamp, networkInterfaces),
                this.csvDataConverter.convertConnectionData(timestamp, connections));

        this.apiClient.postRunningData(runningData, this.stateId);
    }

    private Resources getResources() {
        Resources resourceData = this.oshiMonitor.monitorResources();
        if (resourceData == null) {
            LOGGER.error("Error while monitoring the resources: the resources data object is null. Therefore the data can not be sent to the server.");
        }
        return resourceData;
    }

    private List<NetworkInterface> getNetworkInterfaces() {
        List<NetworkInterface> networkInterfaces = this.oshiMonitor.monitorNetworkInterfaces();
        if (networkInterfaces == null) {
            LOGGER.error("Error while monitoring the network interfaces: the list of network interfaces is null. Therefore the data can not be sent to the server.");
        }
        return networkInterfaces;
    }

    private List<Connection> getIpConnections() {
        List<Connection> connectionData = this.oshiMonitor.monitorIpConnections();
        if (connectionData == null) {
            LOGGER.error("Error while monitoring the IP connections: the list of connections is null. Therefore the data can not be sent to the server.");
        }
        return connectionData;
    }
}
