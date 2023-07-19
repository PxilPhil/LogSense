package org.example.model;

import oshi.software.os.OSProcess;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Application {
    private long contextSwitches;
    private long majorFaults;
    private List<Long> processIDs;
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
    private int threadCount;
    private long upTime;
    private String user;
    private double cpuUsage;
    private final Map<OSProcess, Double> containedProcessesMap = new HashMap<>(); //saves all contained processes, if a new processes is added or one is removed, processCounter should be changed
    private int processCountDifference;
    private long timestamp;

    public Application() {
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

    public List<Long> getProcessIDs() {
        return processIDs;
    }

    public void setProcessIDs(List<Long> processIDs) {
        this.processIDs = processIDs;
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

    public int getThreadCount() {
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

    public void addProcess(OSProcess process, double cpuUsage) {
        this.containedProcessesMap.put(process, cpuUsage);
    }

    public double getProcessValueByID(long processID) {
        if (this.containedProcessesMap.containsKey(processID)) {
            return containedProcessesMap.get(processID);
        }
        return 0;
    }

    public Map<OSProcess, Double> getContainedProcessesMap() {
        return containedProcessesMap;
    }

    public void mergeData(long contextSwitches, long majorFaults, long openFiles, long residentSetSize, long threadCount) {
        this.contextSwitches += contextSwitches;
        this.majorFaults += majorFaults;
        this.openFiles += openFiles;
        this.residentSetSize += residentSetSize;
        this.threadCount += threadCount;
    }

    public void calculateAverage(int amount) {
        this.residentSetSize /= amount;
        this.majorFaults /= amount;
        this.threadCount /= amount;
        this.contextSwitches /= amount;
        this.upTime /= amount;
        this.cpuUsage /= amount;
    }
}
