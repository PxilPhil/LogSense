package org.example.controller;

import org.example.analysis.StatService;
import org.example.api.ApiClient;
import org.example.converter.CSVDataConverter;
import org.example.converter.CSVsToJSONConverter;
import org.example.model.*;
import org.example.monitor.Monitor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import oshi.software.os.OSProcess;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Agent {
    private static final Logger LOGGER = LoggerFactory.getLogger(Agent.class);
    private final Monitor monitor;
    private final StatService statService;
    private final CSVDataConverter csvDataConverter;
    private final CSVsToJSONConverter csvsToJSONConverter;
    private final ApiClient apiClient;
    private SessionComputerData sessionComputerData;
    private long nextMeasuringTimestamp;

    public Agent() {
        this.statService = new StatService();
        this.monitor = new Monitor();
        this.csvDataConverter = new CSVDataConverter();
        this.nextMeasuringTimestamp = System.currentTimeMillis();
        this.csvsToJSONConverter = new CSVsToJSONConverter();
        this.sessionComputerData = null;
        this.apiClient = new ApiClient();
    }

    public void monitor() {
        monitorSessionComputerData();

        while (true) {
            long timestampNow = System.currentTimeMillis();
            if (timestampNow >= this.nextMeasuringTimestamp) {
                List<Application> analysedApplications = getAnalysedApplications(timestampNow);
                if (analysedApplications != null) {     // 60 seconds passed & applications got merged and analysed
                    monitorRunningData(analysedApplications);
                    monitorSessionComputerData();   // check for changes of disk stores and partitions, send session computer data again when the data changed
                }
                this.nextMeasuringTimestamp += 10000;
            }

            try {
                TimeUnit.MILLISECONDS.sleep(10);
            } catch (InterruptedException e) {
                LOGGER.error("Error while waiting until next measurement in the agent:\n" + e);
            }
        }
    }

    private void monitorSessionComputerData() {
        long timestamp = Instant.now().toEpochMilli();

        Client client = getClientData();
        List<DiskStore> diskStores = getDiskStores();
        List<Partition> partitions = getPartitions();

        if (this.sessionComputerData == null || diskStoresChanged(diskStores)) {     // session computer data has never been set --> initial data that starts a new "session"
            SessionComputerData sessionComputerData = new SessionComputerData();
            sessionComputerData.setClient_data(this.csvDataConverter.convertClientData(timestamp, client));
            sessionComputerData.setDisks(this.csvDataConverter.convertDiskStoreData(diskStores));
            sessionComputerData.setPartition(this.csvDataConverter.convertPartitionData(partitions));
            this.sessionComputerData = sessionComputerData;

            String sessionComputerDataJSON = this.csvsToJSONConverter.convertSessionComputerDataToJson(sessionComputerData);

            this.apiClient.postSessionComputerData(sessionComputerDataJSON);
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

    private boolean diskStoresChanged(List<DiskStore> diskStores) {
        String diskStoresCSV = this.csvDataConverter.convertDiskStoreData(diskStores);
        return !diskStoresCSV.equals(this.sessionComputerData.getDisks());
    }

    private void monitorRunningData(List<Application> analysedApplications) {
        long timestamp = Instant.now().toEpochMilli();

        Resources resources = getResources();
        List<NetworkInterface> networkInterfaces = getNetworkInterfaces();
        List<Connection> connections = getIpConnections();

        RunningData runningData = new RunningData();
        runningData.setApplication_data(this.csvDataConverter.convertApplicationData(timestamp, analysedApplications));
        runningData.setPc_resources(this.csvDataConverter.convertResourceData(timestamp, resources));
        runningData.setNetwork_interface(this.csvDataConverter.convertNetworkInterfacesData(timestamp, networkInterfaces));
        runningData.setConnection_data(this.csvDataConverter.convertConnectionData(timestamp, connections));

        String runningDataJSON = this.csvsToJSONConverter.convertRunningData(runningData);

        this.apiClient.postRunningData(runningDataJSON);
    }

    private List<Application> getAnalysedApplications(long timestamp) {
        List<Application> analysedApplications = null;

        List<OSProcess> osProcesses = this.monitor.monitorProcesses();
        if (osProcesses != null) {
            analysedApplications = this.statService.ingestData(timestamp, osProcesses);
        } else {
            LOGGER.error("Error while monitoring the applications: the list of OS processes is null. Therefore the data can not be analysed and sent to the server.");
        }
        return analysedApplications;
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
