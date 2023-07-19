package org.example.controller;

import org.example.analysis.StatService;
import org.example.converter.CSVDataConverter;
import org.example.model.*;
import org.example.monitor.Monitor;
import oshi.software.os.OSProcess;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Agent {
    private final Monitor monitor;
    private final StatService statService;
    private final CSVDataConverter csvDataConverter;
    private long nextApplicationMeasuring;
    private long nextResourceMeasuring;
    private long nextNetworkInterfacesMeasuring;
    private long nextIpConnectionMeasuring;

    public Agent() {
        this.statService = new StatService();
        this.monitor = new Monitor();
        this.csvDataConverter = new CSVDataConverter();
        this.nextApplicationMeasuring = System.currentTimeMillis();
        this.nextResourceMeasuring = System.currentTimeMillis();
        this.nextNetworkInterfacesMeasuring = System.currentTimeMillis();
        this.nextIpConnectionMeasuring = System.currentTimeMillis();
    }

    public void monitor() {
        monitorClientData();
        monitorDiskStores();
        monitorPartitions();

        while (true) {
            long timestampNow = System.currentTimeMillis();
            if (timestampNow >= this.nextApplicationMeasuring) {
                monitorApplications();
                this.nextApplicationMeasuring += 10000;
            }

            if (timestampNow >= this.nextResourceMeasuring) {
                monitorResources();
                this.nextResourceMeasuring += 60000;
            }

            if (timestampNow >= this.nextNetworkInterfacesMeasuring) {
                monitorNetworkInterfaces();
                this.nextNetworkInterfacesMeasuring += 60000;
            }

            if (timestampNow >= this.nextIpConnectionMeasuring) {
                monitorIpConnections();
                this.nextIpConnectionMeasuring += 60000;
            }

            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private void monitorApplications() {
        long timestamp = Instant.now().toEpochMilli();
        List<OSProcess> osProcesses = this.monitor.monitorProcesses();
        List<Application> evaluatedApplicationData = this.statService.ingestData(timestamp, osProcesses);
        if (evaluatedApplicationData != null) {
            String csv = this.csvDataConverter.convertApplicationData(timestamp, evaluatedApplicationData);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\application_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorResources() {
        long timestamp = Instant.now().toEpochMilli();
        Resources resourceData = this.monitor.monitorResources();
        if (resourceData != null) {
            String csv = this.csvDataConverter.convertResourceData(timestamp, resourceData);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\resource_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorNetworkInterfaces() {
        long timestamp = Instant.now().toEpochMilli();
        List<NetworkInterface> networkInterfaces = this.monitor.monitorNetworkInterfaces();
        if (networkInterfaces != null) {
            String csv = this.csvDataConverter.convertNetworkInterfacesData(timestamp, networkInterfaces);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\networkInterfaces_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorIpConnections() {
        long timestamp = Instant.now().toEpochMilli();
        List<Connection> connectionData = this.monitor.monitorIpConnections();
        if (connectionData != null) {
            String csv = this.csvDataConverter.convertConnectionData(timestamp, connectionData);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\connection_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorClientData() {
        long timestamp = Instant.now().toEpochMilli();
        Client client = this.monitor.monitorClientData();
        if (client != null) {
            String csv = this.csvDataConverter.convertClientData(timestamp, client);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\clientData_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorDiskStores() {
        long timestamp = Instant.now().toEpochMilli();
        List<DiskStore> diskStores = this.monitor.monitorDiskStores();
        if (diskStores != null) {
            String csv = this.csvDataConverter.convertDiskStoreData(diskStores);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\diskStore_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }

    private void monitorPartitions() {
        long timestamp = Instant.now().toEpochMilli();
        List<Partition> partitions = this.monitor.monitorPartitions();
        if (partitions != null) {
            String csv = this.csvDataConverter.convertPartitionData(partitions);
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter("C:\\test\\partition_" + timestamp + ".csv"));
                writer.write(csv);
                writer.close();
            } catch (IOException e) {
                System.out.println(csv);
            }
        }
    }
}
