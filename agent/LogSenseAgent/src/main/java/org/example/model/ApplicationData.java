package org.example.model;

import java.util.HashMap;
import java.util.Map;

public class ApplicationData {
    private long contextSwitches;
    private long majorFaults;
    private long processID;
    private int bitness;
    private long bytesRead;
    private long bytesWritten;
    private String commandLine;
    private String currentWorkingDirectory;
    private long kernelTime;
    private long minorFaults;
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
    private long userTime;
    private double cpuUsage;
    private final Map<Long, Double> containedProcessesMap = new HashMap<>(); //saves all contained processes, if a new processes is added or one is removed, processCounter should be changed
    private int processCountDifference;
    private long timestamp;

    public ApplicationData() {
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

    public long getProcessID() {
        return processID;
    }

    public void setProcessID(long processID) {
        this.processID = processID;
    }

    public int getBitness() {
        return bitness;
    }

    public void setBitness(int bitness) {
        this.bitness = bitness;
    }

    public long getBytesRead() {
        return bytesRead;
    }

    public void setBytesRead(long bytesRead) {
        this.bytesRead = bytesRead;
    }

    public long getBytesWritten() {
        return bytesWritten;
    }

    public void setBytesWritten(long bytesWritten) {
        this.bytesWritten = bytesWritten;
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

    public long getKernelTime() {
        return kernelTime;
    }

    public void setKernelTime(int kernelTime) {
        this.kernelTime = kernelTime;
    }

    public void setKernelTime(long kernelTime) {
        this.kernelTime = kernelTime;
    }

    public long getMinorFaults() {
        return minorFaults;
    }

    public void setMinorFaults(long minorFaults) {
        this.minorFaults = minorFaults;
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

    public long getUserTime() {
        return userTime;
    }

    public void setUserTime(long userTime) {
        this.userTime = userTime;
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

    public void addProcess(long processID, double cpuUsage) {
        System.out.println("adding process");
        System.out.println(cpuUsage);
        this.containedProcessesMap.put(processID, cpuUsage);
    }

    public double getProcessValueByID(long processID) {
        if (this.containedProcessesMap.containsKey(processID)) {
            return containedProcessesMap.get(processID);
        }
        return 0;
    }

    public Map<Long, Double> getContainedProcessesMap() {
        return containedProcessesMap;
    }

    public void mergeData(long residentSetSize, long bytesRead, long bytesWritten, long kernelTime, long majorFaults, long minorFaults, long threadCount, long contextSwitches, long upTime, long userTime) {
        this.residentSetSize += residentSetSize;
        this.bytesRead += bytesRead;
        this.bytesWritten += bytesWritten;
        this.kernelTime += kernelTime;
        this.majorFaults += majorFaults;
        this.minorFaults += minorFaults;
        this.threadCount += threadCount;
        this.contextSwitches += contextSwitches;
        this.upTime += upTime;
        this.userTime += userTime;
    }

    public void calculateAverage(int amount) {
        this.residentSetSize = residentSetSize / amount;
        this.bytesRead = bytesRead / amount;
        this.bytesWritten = bytesWritten / amount;
        this.kernelTime = kernelTime / amount;
        this.majorFaults = majorFaults / amount;
        this.minorFaults = minorFaults / amount;
        this.threadCount = threadCount / amount;
        this.contextSwitches = contextSwitches / amount;
        this.upTime = upTime / amount;
        this.userTime = userTime / amount;
        this.cpuUsage = cpuUsage / amount;
    }
}
