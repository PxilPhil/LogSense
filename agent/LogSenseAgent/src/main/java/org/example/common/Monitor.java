package org.example.common;

import org.example.model.Process;
import org.example.model.*;

import java.util.List;

public interface Monitor {
    String monitorOperatingSystem();

    List<Process> monitorProcesses();

    Resources monitorResources();

    List<NetworkInterface> monitorNetworkInterfaces();

    List<Connection> monitorIpConnections();

    Client monitorClientData();

    List<DiskStore> monitorDiskStores();

    List<Partition> monitorPartitions();
}
