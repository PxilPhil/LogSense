package org.example.analysis;

import org.example.model.Application;
import org.example.model.Process;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Instant;
import java.util.*;

import static java.util.Objects.requireNonNull;

public class StatService {
    private static final Logger LOGGER = LoggerFactory.getLogger(StatService.class);
    private final Map<String, List<Application>> applicationMeasurements = new HashMap<>();
    private int dataAmount = 0; //saves how many times data was measured

    public void ingestData(long timestamp, List<Process> processes) {
        requireNonNull(processes);
        if (!processes.isEmpty() && timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
            this.dataAmount++;
            List<Process> filteredOsProcesses = filterSystemProcesses(processes);
            Map<String, Application> mergedApplications = mergeProcessesIntoApplications(timestamp, filteredOsProcesses);
            insertApplicationDataIntoApplicationMeasurements(mergedApplications);
        } else {
            LOGGER.error("Error while ingesting the data: either the list of processes is null or the list is empty" +
                    "or the timestamp is not between epoch and now. Therefore the data can not be ingested.");
        }
    }

    public List<Application> analyseApplicationMeasurements(long timestamp) {
        List<Application> evaluatedApplicationData = new ArrayList<>();
        if (timestamp >= 0 && timestamp <= Instant.now().toEpochMilli()) {
            evaluatedApplicationData = evaluateApplicationMeasurements(timestamp);
            this.applicationMeasurements.clear();
            this.dataAmount = 0;
        } else {
            LOGGER.error("Error while analysing the application measurements: the timestamp is not between epoch " +
                    "and now. Therefore the application measurements can not be analysed.");
        }
        return evaluatedApplicationData;
    }

    private List<Process> filterSystemProcesses(List<Process> processes) {
        List<Process> filteredProcesses = new ArrayList<>();
        for (Process process : processes) {
            if (process.commandLine() != null && !process.commandLine().equalsIgnoreCase("") &&
                    !process.commandLine().equalsIgnoreCase("C:\\Windows") &&
                    !process.commandLine().equalsIgnoreCase("C:\\Windows\\system32")) {
                filteredProcesses.add(process);
            }
        }
        return filteredProcesses;
    }

    private Map<String, Application> mergeProcessesIntoApplications(long timestamp, List<Process> processList) {
        Map<String, Application> mergedApplications = new TreeMap<>();
        for (Process process : processList) {
            String name = process.name();

            Application application;
            if (mergedApplications.containsKey(name)) {
                application = mergedApplications.get(name);
            } else {
                application = new Application();
                application.setTimestamp(timestamp);
                application.setBitness(process.bitness());
                application.setCommandLine(process.commandLine());
                application.setCurrentWorkingDirectory(process.currentWorkingDirectory());
                application.setName(name);
                application.setPath(process.path());
                application.setState(process.state());
                application.setUser(process.user());
            }
            application.addProcess(process);

            application.mergeData(process.contextSwitches(), process.majorFaults(), process.openFiles(),
                    process.residentSetSize(), process.threadCount(), process.upTime());
            mergedApplications.put(name, application);
        }
        return mergedApplications;
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
            averageApplication.setProcessCountDifference(compareProcessesAmount(applicationList));
            averageApplication.calculateAverage(applicationList.size());

            evaluatedApplicationData.add(averageApplication);
        }
        return evaluatedApplicationData;
    }

    private Application performStatisticalAnalysis(List<Application> applicationList, long timestamp) {
        Application averageApplication = new Application();
        for (Application application : applicationList) {
            averageApplication.setCpuUsage(averageApplication.getCpuUsage()
                    + calcTotalApplicationCpuUsage(application.getContainedProcesses()));
            averageApplication.mergeData(application.getContextSwitches(), application.getMajorFaults(),
                    application.getOpenFiles(), application.getResidentSetSize(), application.getThreadCount(),
                    application.getUpTime());
        }
        return setApplicationState(applicationList, averageApplication, timestamp);
    }

    private double calcTotalApplicationCpuUsage(List<Process> processes) {
        double cpuUsage = 0;
        for (Process process : processes) {
            cpuUsage += process.cpuUsage();
        }
        return cpuUsage;
    }

    private Application setApplicationState(List<Application> applicationMeasurements, Application averageApplication,
                                            long timestamp) {
        if (applicationMeasurements.size() < this.dataAmount
                && applicationMeasurements.get(applicationMeasurements.size() - 1).getTimestamp() < timestamp) { //indicates that an application was closed during measuring
            averageApplication.setState("STOPPED");
        } else if (applicationMeasurements.size() < this.dataAmount
                && applicationMeasurements.get(applicationMeasurements.size() - 1).getTimestamp() == timestamp) { //indicates that an application was opened during measuring
            averageApplication.setState("STARTED");
        } else {
            averageApplication.setState("RUNNING");
        }
        return averageApplication;
    }

    private int compareProcessesAmount(List<Application> applicationList) {
        Application firstAppData = applicationList.get(0);
        Application lastAppData = applicationList.get(applicationList.size() - 1);
        return lastAppData.getContainedProcesses().size() - firstAppData.getContainedProcesses().size();
    }
}
