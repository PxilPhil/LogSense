package org.example.model;

import org.example.model.ThreadData;

import java.util.ArrayList;

public class ProcessData {
    private int contextSwitches;
    private int majorFaults;
    private double processCpuLoadCumulative;
    private int processID;
    private int affinityMask;
    private ArrayList<Object> arguments;
    private int bitness;
    private int bytesRead;
    private int bytesWritten;
    private String commandLine;
    private String currentWorkingDirectory;
    private Object environmentVariables;
    private String group;
    private String groupID;
    private int hardOpenFileLimit;
    private int kernelTime;
    private int minorFaults;
    private String name;
    private int openFiles;
    private int parentProcessID;
    private String path;
    private int priority;
    private long residentSetSize;
    private int softOpenFileLimit;
    private long startTime;
    private String state;
    private int threadCount;
    private ArrayList<ThreadData> threadDetails;
    private int upTime;
    private String user;
    private String userID;
    private int userTime;
    private int virtualSize;

    public ProcessData() {
    }

    // Getters
    public int getContextSwitches() {
        return contextSwitches;
    }

    public int getMajorFaults() {
        return majorFaults;
    }

    public double getProcessCpuLoadCumulative() {
        return processCpuLoadCumulative;
    }

    public int getProcessID() {
        return processID;
    }

    public int getAffinityMask() {
        return affinityMask;
    }

    public ArrayList<Object> getArguments() {
        return arguments;
    }

    public int getBitness() {
        return bitness;
    }

    public int getBytesRead() {
        return bytesRead;
    }

    public int getBytesWritten() {
        return bytesWritten;
    }

    public String getCommandLine() {
        return commandLine;
    }

    public String getCurrentWorkingDirectory() {
        return currentWorkingDirectory;
    }

    public Object getEnvironmentVariables() {
        return environmentVariables;
    }

    public String getGroup() {
        return group;
    }

    public String getGroupID() {
        return groupID;
    }

    public int getHardOpenFileLimit() {
        return hardOpenFileLimit;
    }

    public int getKernelTime() {
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

    public int getPriority() {
        return priority;
    }

    public long getResidentSetSize() {
        return residentSetSize;
    }

    public int getSoftOpenFileLimit() {
        return softOpenFileLimit;
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

    public ArrayList<ThreadData> getThreadDetails() {
        return threadDetails;
    }

    public int getUpTime() {
        return upTime;
    }

    public String getUser() {
        return user;
    }

    public String getUserID() {
        return userID;
    }

    public int getUserTime() {
        return userTime;
    }

    public int getVirtualSize() {
        return virtualSize;
    }

    // Setters
    public void setContextSwitches(int contextSwitches) {
        this.contextSwitches = contextSwitches;
    }

    public void setMajorFaults(int majorFaults) {
        this.majorFaults = majorFaults;
    }

    public void setProcessCpuLoadCumulative(double processCpuLoadCumulative) {
        this.processCpuLoadCumulative = processCpuLoadCumulative;
    }

    public void setProcessID(int processID) {
        this.processID = processID;
    }

    public void setAffinityMask(int affinityMask) {
        this.affinityMask = affinityMask;
    }

    public void setArguments(ArrayList<Object> arguments) {
        this.arguments = arguments;
    }

    public void setBitness(int bitness) {
        this.bitness = bitness;
    }

    public void setBytesRead(int bytesRead) {
        this.bytesRead = bytesRead;
    }

    public void setBytesWritten(int bytesWritten) {
        this.bytesWritten = bytesWritten;
    }

    public void setCommandLine(String commandLine) {
        this.commandLine = commandLine;
    }

    public void setCurrentWorkingDirectory(String currentWorkingDirectory) {
        this.currentWorkingDirectory = currentWorkingDirectory;
    }

    public void setEnvironmentVariables(Object environmentVariables) {
        this.environmentVariables = environmentVariables;
    }

    public void setGroup(String group) {
        this.group = group;
    }

    public void setGroupID(String groupID) {
        this.groupID = groupID;
    }

    public void setHardOpenFileLimit(int hardOpenFileLimit) {
        this.hardOpenFileLimit = hardOpenFileLimit;
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

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public void setResidentSetSize(long residentSetSize) {
        this.residentSetSize = residentSetSize;
    }

    public void setSoftOpenFileLimit(int softOpenFileLimit) {
        this.softOpenFileLimit = softOpenFileLimit;
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

    public void setThreadDetails(ArrayList<ThreadData> threadDetails) {
        this.threadDetails = threadDetails;
    }

    public void setUpTime(int upTime) {
        this.upTime = upTime;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public void setUserID(String userID) {
        this.userID = userID;
    }

    public void setUserTime(int userTime) {
        this.userTime = userTime;
    }

    public void setVirtualSize(int virtualSize) {
        this.virtualSize = virtualSize;
    }
}
