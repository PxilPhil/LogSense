package org.example.analysis;

import org.example.model.ApplicationData;
import oshi.software.os.OSProcess;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class StatService {
    private final Map<String, List<ApplicationData>> applicationMeasurementPoints = new TreeMap<>();
    private int dataAmount = 0; //saves how many times data was measured
    private final int analysisInterval = 60;
    private long lastAnalysis;

    public StatService() {

    }

    public List<ApplicationData> ingestData(long timestamp, List<OSProcess> osProcesses) {
        this.dataAmount++;

        //this calculates statistical stuff every minute, however slight differences can occur
        //problem: data is not always exactly minute
        //solution: artificial delay, deal with it, split up data

        //this.osProcessMap.put(timestamp, osProcesses);
        Map<String, ApplicationData> applications = mergeProcessesIntoApplications(timestamp, osProcesses);
        insertApplicationDataIntoMeasurementPointMap(applications);

        if (timestamp >= (this.lastAnalysis + this.analysisInterval * 1000L)) { //if X amount has passed since the last timeStamp / analysis
            List<ApplicationData> evaluatedApplicationData = evaluateApplicationMeasurementPoints(timestamp);
            this.applicationMeasurementPoints.clear();
            this.lastAnalysis = timestamp;
            this.dataAmount = 0;
            return evaluatedApplicationData;
        }
        return null;
    }


    private Map<String, ApplicationData> mergeProcessesIntoApplications(long timestamp, List<OSProcess> processList) { //merges processes into applications
        //create map to assign and access values better, then turn that into a normal list
        Map<String, ApplicationData> osProcessMapTemp = new TreeMap<>();
        for (OSProcess process : processList) {
            String name = process.getName();

            ApplicationData applicationData;
            if (osProcessMapTemp.containsKey(name)) {
                applicationData = osProcessMapTemp.get(name);
            } else {
                applicationData = new ApplicationData();
                applicationData.setUser(process.getUser());
                applicationData.setPath(process.getPath());
            }

            applicationData.setTimestamp(timestamp);
            addProcessAndCpuUsageToApplication(process, applicationData);

            applicationData.mergeData(process.getResidentSetSize(), process.getBytesRead(), process.getBytesWritten(), process.getKernelTime(), process.getMajorFaults(), process.getMinorFaults(), process.getThreadCount(), process.getContextSwitches(), process.getUpTime(), process.getUserTime());
            osProcessMapTemp.put(name, applicationData);
        }
        return osProcessMapTemp;
    }

    private void addProcessAndCpuUsageToApplication(OSProcess process, ApplicationData applicationData) {
        if (this.applicationMeasurementPoints.containsKey(process.getName())) { //if already has entry get previous cpu usage of respective process
            List<ApplicationData> applicationDataList = this.applicationMeasurementPoints.get(process.getName());
            ApplicationData previousAppData = applicationDataList.get(applicationDataList.size() - 1);
            applicationData.addProcess(process.getProcessID(), calculateCPUUsage(process, previousAppData.getProcessValueByID(process.getProcessID())));
        } else {
            applicationData.addProcess(process.getProcessID(), calculateCPUUsage(process, 0));
        }
    }

    private void insertApplicationDataIntoMeasurementPointMap(Map<String, ApplicationData> osProcessMapTemp) {
        for (Map.Entry<String, ApplicationData> current : osProcessMapTemp.entrySet()) {
            List<ApplicationData> applicationDataList;
            String key = current.getKey();
            if (applicationMeasurementPoints.containsKey(key)) { //if it contains key just get ProcessData
                applicationDataList = applicationMeasurementPoints.get(key);
            } else {
                applicationDataList = new ArrayList<>();
            }
            applicationDataList.add(current.getValue());
            applicationMeasurementPoints.put(key, applicationDataList);
        }
    }

    private double calculateCPUUsage(OSProcess osProcess, double prev) { //calculates cpu usage per process
        System.out.println("calculateCPUUsage");
        double timeDiff = (osProcess.getKernelTime() + osProcess.getUserTime()) - prev;
        System.out.println(timeDiff);
        double cpuUsage = (100 * (timeDiff / osProcess.getUpTime()));
        System.out.println(cpuUsage);
        return cpuUsage;
    }

    private int compareProcessesAmount(List<ApplicationData> applicationDataList) {
        ApplicationData firstAppData = applicationDataList.get(0);
        ApplicationData lastAppData = applicationDataList.get(applicationDataList.size() - 1);

        System.out.println("size of maps");
        System.out.println(firstAppData.getContainedProcessesMap().size());
        System.out.println(lastAppData.getContainedProcessesMap().size());
        return lastAppData.getContainedProcessesMap().size() - firstAppData.getContainedProcessesMap().size();
    }

    private double calcTotalCPUUsage(Map<Integer, Double> processes) {
        double sum = 0;
        for (Map.Entry<Integer, Double> current : processes.entrySet()) {
            sum += current.getValue();
            System.out.println("sum");
            System.out.println(sum);
        }
        return sum;
    }


    private List<ApplicationData> evaluateApplicationMeasurementPoints(long timestamp) { //does statistical calculations on minutely data (keep in mind that everything not transferred here will be lost)
        List<ApplicationData> evaluatedApplicationData = new ArrayList<>();
        for (Map.Entry<String, List<ApplicationData>> currentApplication : this.applicationMeasurementPoints.entrySet()) {
            List<ApplicationData> applicationDataList = currentApplication.getValue();

            ApplicationData sumApplication = performStatisticalAnalysis(applicationDataList, timestamp);

            sumApplication.setName(currentApplication.getKey());
            sumApplication.setPath(applicationDataList.get(0).getPath());
            sumApplication.setUser(applicationDataList.get(0).getUser());
            sumApplication.calculateAverage(applicationDataList.size());
            sumApplication.setProcessCounter(compareProcessesAmount(applicationDataList)); //TODO: does this work or is nothing saved??????????
            //have to implement way to detect applications themselves closing too (just look if list is different from max value in list)
            evaluatedApplicationData.add(sumApplication);
        }
        return evaluatedApplicationData;
    }

    private ApplicationData setSumApplicationState(List<ApplicationData> applicationDataList, ApplicationData sumApplication, long timestamp) {
        if (applicationDataList.size() < this.dataAmount && applicationDataList.get(applicationDataList.size() - 1).getTimestamp() < timestamp) { //indicates that an application was closed during measuring
            //save by number value or string, you could compare first and last or loop through everything
            sumApplication.setState("STOPPED");
        } else if (applicationDataList.size() < this.dataAmount && applicationDataList.get(applicationDataList.size() - 1).getTimestamp() == timestamp) { //indicates that an application was opened during measuring
            sumApplication.setState("STARTED");
        } else {
            sumApplication.setState("RUNNING");
        }
        return sumApplication;
    }

    private ApplicationData performStatisticalAnalysis(List<ApplicationData> applicationDataList, long timestamp) {
        ApplicationData sumApplication = new ApplicationData();
        for (ApplicationData application : applicationDataList) {
            sumApplication.setCpuUsage(calcTotalCPUUsage(application.getContainedProcessesMap()));
            sumApplication.mergeData(application.getResidentSetSize(), application.getBytesRead(), application.getBytesWritten(), application.getKernelTime(), application.getMajorFaults(), application.getMinorFaults(), application.getThreadCount(), application.getContextSwitches(), application.getUpTime(), application.getUserTime()); //put cpu here
        }

        return setSumApplicationState(applicationDataList, sumApplication, timestamp);
    }
}
