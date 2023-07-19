package org.example.analysis;

import org.example.model.Application;
import oshi.software.os.OSProcess;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class StatService {
    private final Map<String, List<Application>> applicationMeasurements = new TreeMap<>();
    private int dataAmount = 0; //saves how many times data was measured
    private final int analysisInterval = 60;
    private long lastAnalysis;

    public StatService() {

    }

    public List<Application> ingestData(long timestamp, List<OSProcess> osProcesses) {
        this.dataAmount++;
        List<OSProcess> filteredOsProcesses = filterSystemProcesses(osProcesses);
        Map<String, Application> mergedApplications = mergeProcessesIntoApplications(timestamp, filteredOsProcesses);
        insertApplicationDataIntoApplicationMeasurements(mergedApplications);

        if (timestamp >= (this.lastAnalysis + this.analysisInterval * 1000L)) { //if X amount has passed since the last timeStamp / analysis
            List<Application> evaluatedApplicationData = evaluateApplicationMeasurements(timestamp);
            this.applicationMeasurements.clear();
            this.lastAnalysis = timestamp;
            this.dataAmount = 0;
            return evaluatedApplicationData;
        }
        return null;
    }

    private List<OSProcess> filterSystemProcesses(List<OSProcess> osProcesses) {
        List<OSProcess> filteredOsProcesses = new ArrayList<>();
        for (OSProcess process : osProcesses) {
            if (process.getCommandLine() != null && !process.getCommandLine().equalsIgnoreCase("") && !process.getCommandLine().equalsIgnoreCase("C:\\Windows") && !process.getCommandLine().equalsIgnoreCase("C:\\Windows\\system32")) {
                filteredOsProcesses.add(process);
            }
        }
        return filteredOsProcesses;
    }

    private Map<String, Application> mergeProcessesIntoApplications(long timestamp, List<OSProcess> processList) {
        Map<String, Application> mergedApplications = new TreeMap<>();
        for (OSProcess process : processList) {
            String name = process.getName();

            Application application;
            if (mergedApplications.containsKey(name)) {
                application = mergedApplications.get(name);
            } else {
                application = new Application();
                application.setTimestamp(timestamp);
                application.setBitness(process.getBitness());
                application.setCommandLine(process.getCommandLine());
                application.setCurrentWorkingDirectory(process.getCurrentWorkingDirectory());
                application.setName(name);
                application.setPath(process.getPath());
                application.setState(process.getState().toString());
                application.setUser(process.getUser());
            }
            addProcessAndCpuUsageToApplication(application, process);

            application.mergeData(process.getContextSwitches(), process.getMajorFaults(), process.getOpenFiles(), process.getResidentSetSize(), process.getThreadCount());
            mergedApplications.put(name, application);
        }
        return mergedApplications;
    }

    private void addProcessAndCpuUsageToApplication(Application application, OSProcess process) {
        if (this.applicationMeasurements.containsKey(process.getName())) { //if already has entry get previous cpu usage of respective process
            List<Application> applicationList = this.applicationMeasurements.get(process.getName());
            Application previousAppData = applicationList.get(applicationList.size() - 1);
            for (OSProcess previousProcess : previousAppData.getContainedProcessesMap().keySet()) {
                if (previousProcess.getProcessID() == process.getProcessID()) {
                    application.addProcess(process, calculateCpuUsage(process, previousProcess));
                }
            }
        } else {
            application.addProcess(process, calculateCpuUsage(process, null));
        }
    }

    private double calculateCpuUsage(OSProcess osProcess, OSProcess previousProcess) {
        return osProcess.getProcessCpuLoadBetweenTicks(previousProcess);
    }

    private void insertApplicationDataIntoApplicationMeasurements(Map<String, Application> mergedApplications) {
        for (Map.Entry<String, Application> applicationMeasurementsEntry : mergedApplications.entrySet()) {
            List<Application> applicationList;
            String applicationName = applicationMeasurementsEntry.getKey();
            if (this.applicationMeasurements.containsKey(applicationName)) { //if it contains key just get ProcessData
                applicationList = this.applicationMeasurements.get(applicationName);
            } else {
                applicationList = new ArrayList<>();
            }
            applicationList.add(applicationMeasurementsEntry.getValue());
            this.applicationMeasurements.put(applicationName, applicationList);
        }
    }

    private List<Application> evaluateApplicationMeasurements(long timestamp) { //does statistical calculations on minutely data (keep in mind that everything not transferred here will be lost)
        List<Application> evaluatedApplicationData = new ArrayList<>();
        for (Map.Entry<String, List<Application>> applicationMeasurementEntry : this.applicationMeasurements.entrySet()) {
            List<Application> applicationList = applicationMeasurementEntry.getValue();

            Application averageApplication = performStatisticalAnalysis(applicationList, timestamp);

            averageApplication.setBitness(applicationList.get(0).getBitness());
            averageApplication.setCommandLine(applicationList.get(0).getCommandLine());
            averageApplication.setCurrentWorkingDirectory(applicationList.get(0).getCurrentWorkingDirectory());
            averageApplication.setName(applicationMeasurementEntry.getKey());
            averageApplication.setPath(applicationList.get(0).getPath());
            averageApplication.setUser(applicationList.get(0).getUser());
            averageApplication.setProcessCountDifference(compareProcessesAmount(applicationList)); //TODO: detect applications themselves closing too (just look if list is different from max value in list)

            averageApplication.calculateAverage(applicationList.size());

            evaluatedApplicationData.add(averageApplication);
        }
        return evaluatedApplicationData;
    }

    private Application performStatisticalAnalysis(List<Application> applicationList, long timestamp) {
        Application averageApplication = new Application();
        for (Application application : applicationList) {
            averageApplication.setCpuUsage(averageApplication.getCpuUsage() + calcTotalApplicationCpuUsage(application.getContainedProcessesMap()));
            averageApplication.mergeData(application.getContextSwitches(), application.getMajorFaults(), application.getOpenFiles(), application.getResidentSetSize(), application.getThreadCount());
        }
        return setApplicationState(applicationList, averageApplication, timestamp);
    }

    private double calcTotalApplicationCpuUsage(Map<OSProcess, Double> processes) {
        double sum = 0;
        for (Map.Entry<OSProcess, Double> current : processes.entrySet()) {
            sum += current.getValue();
        }
        return sum;
    }

    private Application setApplicationState(List<Application> applicationMeasurements, Application averageApplication, long timestamp) {
        if (applicationMeasurements.size() < this.dataAmount && applicationMeasurements.get(applicationMeasurements.size() - 1).getTimestamp() < timestamp) { //indicates that an application was closed during measuring
            averageApplication.setState("STOPPED");
        } else if (applicationMeasurements.size() < this.dataAmount && applicationMeasurements.get(applicationMeasurements.size() - 1).getTimestamp() == timestamp) { //indicates that an application was opened during measuring
            averageApplication.setState("STARTED");
        } else {
            averageApplication.setState("RUNNING");
        }
        return averageApplication;
    }

    private int compareProcessesAmount(List<Application> applicationList) {
        Application firstAppData = applicationList.get(0);
        Application lastAppData = applicationList.get(applicationList.size() - 1);
        return lastAppData.getContainedProcessesMap().size() - firstAppData.getContainedProcessesMap().size();
    }
}
