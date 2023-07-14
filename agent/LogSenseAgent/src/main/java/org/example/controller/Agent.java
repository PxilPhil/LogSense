package org.example.controller;

import com.opencsv.CSVWriter;
import org.example.analysis.StatService;
import org.example.converter.CSVDataConverter;
import org.example.model.ApplicationData;
import org.example.model.ResourcesData;
import org.example.monitor.Monitor;
import oshi.SystemInfo;
import oshi.software.os.InternetProtocolStats;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Agent {
    private final Monitor monitor;
    private final StatService statService;
    private final CSVDataConverter csvDataConverter;

    public Agent() {
        this.statService = new StatService();
        this.monitor = new Monitor();
        this.csvDataConverter = new CSVDataConverter();
    }

    public void monitor() {
        while (true) {
            monitorApplications();
            monitorResources();
            writeIpConnectionsToCsv(new SystemInfo().getOperatingSystem());
            try {
                TimeUnit.SECONDS.sleep(10);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

    private void monitorApplications() {
        long timestamp = Instant.now().toEpochMilli();
        List<OSProcess> osProcesses = this.monitor.monitorProcesses();
        List<ApplicationData> evaluatedApplicationData = this.statService.ingestData(timestamp, osProcesses);
        if (evaluatedApplicationData != null) {
            String csv = this.csvDataConverter.convertApplicationData(timestamp, evaluatedApplicationData);
            System.out.println(csv);
        }
    }

    private void monitorResources() {
        long timestamp = Instant.now().toEpochMilli();
        ResourcesData resourceData = this.monitor.monitorResources();
        if (resourceData != null) {
            String csv = this.csvDataConverter.convertResourceData(timestamp, resourceData);
            System.out.println(csv);
        }
    }

    private void writeIpConnectionsToCsv(OperatingSystem operatingSystem) {
        List<String[]> ipConnections = new ArrayList<>();
        String[] ipConnectionHeaders = {"timestamp", "localPort", "foreignAddress", "foreignPort", "state", "type"};
        ipConnections.add(ipConnectionHeaders);

        long timestamp = Instant.now().toEpochMilli();
        for (InternetProtocolStats.IPConnection connection : operatingSystem.getInternetProtocolStats().getConnections()) {
            String[] record = new String[0];
            if (connection.getType().equals("tcp4")) {
                try {
                    record = new String[]{String.valueOf(timestamp), String.valueOf(connection.getLocalPort()), InetAddress.getByAddress(connection.getForeignAddress()).toString(), String.valueOf(connection.getForeignPort()), String.valueOf(connection.getState()), connection.getType()};
                } catch (UnknownHostException e) {
                    throw new RuntimeException(e);
                }
            }
            ipConnections.add(record);
        }

        try {
            CSVWriter writer = new CSVWriter(new FileWriter("C:\\test\\connection_" + timestamp + ".csv"));
            writer.writeAll(ipConnections);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
