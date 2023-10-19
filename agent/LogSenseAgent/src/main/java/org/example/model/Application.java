package org.example.model;

import java.util.ArrayList;
import java.util.List;

public class Application {
    private long contextSwitches;
    private long majorFaults;
    private int bitness;
    private String commandLine;
    private String currentWorkingDirectory;
    private String name;
    private long openFiles;
    private long parentProcessID;
    private String path;
    private long residentSetSize;
    private long startTime;
    private String state;
    private long threadCount;
    private long upTime;
    private String user;
    private double cpuUsage;
    private int processCountDifference;
    private long timestamp;
    private List<Process> containedProcesses; //saves all contained processes, if a new processes is added or one is removed, processCounter should be changed

    public Application() {
    }

    public Application(long contextSwitches, long majorFaults, int bitness, String commandLine, String currentWorkingDirectory, String name, long openFiles, long parentProcessID, String path, long residentSetSize, long startTime, String state, int threadCount, long upTime, String user, double cpuUsage, int processCountDifference, long timestamp) {
        this.contextSwitches = contextSwitches;
        this.majorFaults = majorFaults;
        this.bitness = bitness;
        this.commandLine = commandLine;
        this.currentWorkingDirectory = currentWorkingDirectory;
        this.name = name;
        this.openFiles = openFiles;
        this.parentProcessID = parentProcessID;
        this.path = path;
        this.residentSetSize = residentSetSize;
        this.startTime = startTime;
        this.state = state;
        this.threadCount = threadCount;
        this.upTime = upTime;
        this.user = user;
        this.cpuUsage = cpuUsage;
        this.processCountDifference = processCountDifference;
        this.timestamp = timestamp;
        this.containedProcesses = new ArrayList<>();
    }

    public long getContextSwitches() {
        return contextSwitches;
    }

    public void setContextSwitches(long contextSwitches) {
        this.contextSwitches = contextSwitches;
    }

    public long getMajorFaults() {
        return majorFaults;
    }

    public void setMajorFaults(long majorFaults) {
        this.majorFaults = majorFaults;
    }

    public int getBitness() {
        return bitness;
    }

    public void setBitness(int bitness) {
        this.bitness = bitness;
    }

    public String getCommandLine() {
        return commandLine;
    }

    public void setCommandLine(String commandLine) {
        this.commandLine = commandLine;
    }

    public String getCurrentWorkingDirectory() {
        return currentWorkingDirectory;
    }

    public void setCurrentWorkingDirectory(String currentWorkingDirectory) {
        this.currentWorkingDirectory = currentWorkingDirectory;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public long getOpenFiles() {
        return openFiles;
    }

    public void setOpenFiles(long openFiles) {
        this.openFiles = openFiles;
    }

    public long getParentProcessID() {
        return parentProcessID;
    }

    public void setParentProcessID(long parentProcessID) {
        this.parentProcessID = parentProcessID;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public long getResidentSetSize() {
        return residentSetSize;
    }

    public void setResidentSetSize(long residentSetSize) {
        this.residentSetSize = residentSetSize;
    }

    public long getStartTime() {
        return startTime;
    }

    public void setStartTime(long startTime) {
        this.startTime = startTime;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public long getThreadCount() {
        return threadCount;
    }

    public void setThreadCount(int threadCount) {
        this.threadCount = threadCount;
    }

    public long getUpTime() {
        return upTime;
    }

    public void setUpTime(long upTime) {
        this.upTime = upTime;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public int getProcessCountDifference() {
        return processCountDifference;
    }

    public void setProcessCountDifference(int processCountDifference) {
        this.processCountDifference = processCountDifference;
    }

    public double getCpuUsage() {
        return cpuUsage;
    }

    public void setCpuUsage(double cpuUsage) {
        this.cpuUsage = cpuUsage;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public List<Process> getContainedProcesses() {
        return containedProcesses;
    }

    public void addProcess(Process process) {
        if (process != null) {
            this.containedProcesses.add(process);
        }
    }

    public void mergeData(long contextSwitches, long majorFaults, long openFiles, long residentSetSize, long threadCount, long upTime) {
        this.contextSwitches += contextSwitches >= 0 ? contextSwitches : 0;
        this.majorFaults += majorFaults >= 0 ? majorFaults : 0;
        this.openFiles += openFiles >= 0 ? openFiles : 0;
        this.residentSetSize += residentSetSize >= 0 ? residentSetSize : 0;
        this.threadCount += threadCount >= 0 ? threadCount : 0;

        if (upTime >= 0 && upTime > this.upTime) {
            this.upTime = upTime;
        }
    }

    public void calculateAverage(int amount) {
        if (amount > 0) {
            this.contextSwitches /= amount;
            this.majorFaults /= amount;
            this.openFiles /= amount;
            this.residentSetSize /= amount;
            this.threadCount /= amount;
            this.cpuUsage /= amount;
        }
    }
}