package org.example.model;

import java.util.HashMap;
import java.util.Map;

public class ApplicationData {
    private int contextSwitches;
    private int majorFaults;
    private int processID;
    private int bitness;
    private long bytesRead;
    private long bytesWritten;
    private String commandLine;
    private String currentWorkingDirectory;
    private long kernelTime;
    private int minorFaults;
    private String name;
    private int openFiles;
    private int parentProcessID;
    private String path;
    private long residentSetSize;
    private long startTime;
    private String state;
    private int threadCount;
    private int upTime;
    private String user;
    private int userTime;
    private double cpuUsage;
    private Map<Integer, Double> containedProcessesMap = new HashMap<>(); //saves all contained processes, if a new processes is added or one is removed, processCounter should be changed
    private int processCounter;
    private long timestamp;

    public ApplicationData() {
    }

    // Getters
    public int getContextSwitches() {
        return contextSwitches;
    }

    public int getMajorFaults() {
        return majorFaults;
    }

    public int getProcessID() {
        return processID;
    }

    public int getBitness() {
        return bitness;
    }

    public long getBytesRead() {
        return bytesRead;
    }

    public long getBytesWritten() {
        return bytesWritten;
    }

    public String getCommandLine() {
        return commandLine;
    }

    public String getCurrentWorkingDirectory() {
        return currentWorkingDirectory;
    }

    public long getKernelTime() {
        return kernelTime;
    }

    public int getMinorFaults() {
        return minorFaults;
    }

    public String getName() {
        return name;
    }

    public int getOpenFiles() {
        return openFiles;
    }

    public int getParentProcessID() {
        return parentProcessID;
    }

    public String getPath() {
        return path;
    }

    public long getResidentSetSize() {
        return residentSetSize;
    }

    public long getStartTime() {
        return startTime;
    }

    public String getState() {
        return state;
    }

    public int getThreadCount() {
        return threadCount;
    }

    public int getUpTime() {
        return upTime;
    }

    public String getUser() {
        return user;
    }

    public int getUserTime() {
        return userTime;
    }

    // Setters
    public void setContextSwitches(int contextSwitches) {
        this.contextSwitches = contextSwitches;
    }

    public void setMajorFaults(int majorFaults) {
        this.majorFaults = majorFaults;
    }

    public void setProcessID(int processID) {
        this.processID = processID;
    }

    public void setBitness(int bitness) {
        this.bitness = bitness;
    }

    public void setBytesRead(long bytesRead) {
        this.bytesRead = bytesRead;
    }

    public void setBytesWritten(long bytesWritten) {
        this.bytesWritten = bytesWritten;
    }

    public void setCommandLine(String commandLine) {
        this.commandLine = commandLine;
    }

    public void setCurrentWorkingDirectory(String currentWorkingDirectory) {
        this.currentWorkingDirectory = currentWorkingDirectory;
    }

    public void setKernelTime(int kernelTime) {
        this.kernelTime = kernelTime;
    }

    public void setMinorFaults(int minorFaults) {
        this.minorFaults = minorFaults;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setOpenFiles(int openFiles) {
        this.openFiles = openFiles;
    }

    public void setParentProcessID(int parentProcessID) {
        this.parentProcessID = parentProcessID;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public void setResidentSetSize(long residentSetSize) {
        this.residentSetSize = residentSetSize;
    }

    public void setStartTime(long startTime) {
        this.startTime = startTime;
    }

    public void setState(String state) {
        this.state = state;
    }

    public void setThreadCount(int threadCount) {
        this.threadCount = threadCount;
    }

    public void setUpTime(int upTime) {
        this.upTime = upTime;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public void setUserTime(int userTime) {
        this.userTime = userTime;
    }

    public int getProcessCounter() {
        return processCounter;
    }

    public double getCpuUsage() {
        return cpuUsage;
    }

    public void setCpuUsage(double cpuUsage) {
        this.cpuUsage = cpuUsage;
    }

    public void setKernelTime(long kernelTime) {
        this.kernelTime = kernelTime;
    }

    public void setProcessCounter(int processCounter) {
        this.processCounter = processCounter;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void addProcess(int processID, double cpuUsage) {
        System.out.println("adding process");
        System.out.println(cpuUsage);
        this.containedProcessesMap.put(processID, cpuUsage);
    }

    public double getProcessValueByID(int processID) {
        if (this.containedProcessesMap.containsKey(processID)) {
            return containedProcessesMap.get(processID);
        }
        return 0;
    }


    public Map<Integer, Double> getContainedProcessesMap() {
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
