package org.example.monitor;

import org.example.analysis.StatService;
import oshi.SystemInfo;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.util.List;

public class Monitor {
    private final SystemInfo systemInfo;
    private final OperatingSystem operatingSystem;
    private final StatService statService;

    public Monitor() {
        this.systemInfo = new SystemInfo();
        this.operatingSystem = this.systemInfo.getOperatingSystem();
        this.statService = new StatService();
    }

    public List<OSProcess> getProcesses() {
        return this.operatingSystem.getProcesses();
    }
}
