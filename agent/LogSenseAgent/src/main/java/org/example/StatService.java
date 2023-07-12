package org.example;

import org.example.model.ApplicationData;
import oshi.software.os.OSProcess;

import java.util.*;

public class StatService {
    //private ArrayList<OSProcess> osProcessList=new ArrayList<>(); //only for processes for now
    private Map<String, List<ApplicationData>> processDataMap = new TreeMap<>();
    private int dataAmount = 0; //saves how many times data was measured
    private int timeDifference = 60; //performs operations every 60 seconds
    private long lastTimestamp; //last timestamp of last request
    private WritingService writingService = new WritingService();

    public StatService() {

    }

    public void ingestData(long timestamp, List<OSProcess> osProcesses) {
        this.dataAmount++;
        System.out.println(dataAmount);

        //this calculates statistical stuff every minute, however slight differences can occur
        //problem: data is not always exactly minute
        //solution: artificial delay, deal with it, split up data

        //this.osProcessMap.put(timestamp, osProcesses);
        this.processDataMap = performMerging(timestamp, osProcesses);


        if (timestamp >= (lastTimestamp + this.timeDifference * 1000)) { //if X amount has passed since the last timeStamp
            List<ApplicationData> stats = calculateStats(timestamp);
            //write into csv and view in console
            writingService.writeProcessDataToCsv(lastTimestamp, stats);
            processDataMap.clear();
            lastTimestamp = timestamp;
            dataAmount = 0;
        }

    }


    private Map<String, List<ApplicationData>> performMerging(long timestamp, List<OSProcess> processList) { //merges processes into applications
        System.out.println("performing merging");
        //create map to assign and access values better, then turn that into a normal list
        Map<String, ApplicationData> osProcessMapTemp = new TreeMap<>();
        for (OSProcess process : processList) {
            int processID = process.getProcessID();
            String name = process.getName();

            ApplicationData applicationData;
            if (osProcessMapTemp.containsKey(name)) {
                applicationData = osProcessMapTemp.get(name);
            } else {
                applicationData = new ApplicationData();
                applicationData.setUser(process.getUser());
                applicationData.setPath(process.getPath());
            }

            if (this.processDataMap.containsKey(name)) { //if already has entry get previous cpu usage of respective process
                List<ApplicationData> applicationDataList = this.processDataMap.get(name);
                ApplicationData previousAppData = applicationDataList.get(applicationDataList.size()-1);
                applicationData.addProcess(processID, calculateCPUUsage(process, previousAppData.getProcessValueByID(processID)));
            } else {
                applicationData.addProcess(process.getProcessID(), calculateCPUUsage(process, 0));
            }
            applicationData.setTimestamp(timestamp);

            applicationData.mergeData(process.getResidentSetSize(), process.getBytesRead(), process.getBytesWritten(), process.getKernelTime(), process.getMajorFaults(), process.getMinorFaults(), process.getThreadCount(), process.getContextSwitches(), process.getUpTime(), process.getUserTime());
            osProcessMapTemp.put(name, applicationData);
        }


        //insert into existing map
        for(Map.Entry<String, ApplicationData> current : osProcessMapTemp.entrySet()) {
            List<ApplicationData> applicationDataList;
            String key = current.getKey();
            if (processDataMap.containsKey(key)) { //if it contains key just get ProcessData
                applicationDataList = processDataMap.get(key);
            } else {
                applicationDataList = new ArrayList<>();
            }
            applicationDataList.add(current.getValue());
            processDataMap.put(key, applicationDataList);
        }

        return processDataMap;
    }

    private double calculateCPUUsage(OSProcess osProcess, double prev) { //calculates cpu usage per proces
        System.out.println("calculateCPUUsage");
        double timeDiff = (osProcess.getKernelTime()+osProcess.getUserTime()) - prev;
        System.out.println(timeDiff);
        double cpuUsage = (100 * (timeDiff/osProcess.getUpTime()));
        System.out.println(cpuUsage);
        return cpuUsage;
    }

    private int compareProcessesAmount(List<ApplicationData> applicationDataList) {
        ApplicationData firstAppData = applicationDataList.get(0);
        ApplicationData lastAppData = applicationDataList.get(applicationDataList.size()-1);

        System.out.println("size of maps");
        System.out.println(firstAppData.getContainedProcessesMap().size());
        System.out.println(lastAppData.getContainedProcessesMap().size());
        return lastAppData.getContainedProcessesMap().size() - firstAppData.getContainedProcessesMap().size();
    }

    private double calcTotalCPUUsage(Map<Integer, Double> processes) {
        double sum = 0;
        for (Map.Entry<Integer, Double> current : processes.entrySet()) {
            sum+=current.getValue();
            System.out.println("sum");
            System.out.println(sum);
        }
        return sum;
    }




    private List<ApplicationData> calculateStats(long timestamp) { //does statistical calculations on minutely data (keep in mind that everything not transfered here will be lost)
        List<ApplicationData> applicationDataList = new ArrayList<>();
        for(Map.Entry<String, List<ApplicationData>> current : this.processDataMap.entrySet()) {

            List<ApplicationData> currentList = current.getValue();
            ApplicationData sumProcess = new ApplicationData();
            for(ApplicationData process : currentList) {
                sumProcess.setCpuUsage(calcTotalCPUUsage(process.getContainedProcessesMap()));
                sumProcess.mergeData(process.getResidentSetSize(), process.getBytesRead(), process.getBytesWritten(), process.getKernelTime(), process.getMajorFaults(), process.getMinorFaults(), process.getThreadCount(), process.getContextSwitches(), process.getUpTime(), process.getUserTime()); //put cpu here
            }
            System.out.println("Application Amount List");
            System.out.println(currentList.size());
            System.out.println(dataAmount);
            if (currentList.size() < dataAmount && currentList.get(currentList.size()-1).getTimestamp()<timestamp) { //indicates that an application was closed during measuring
                //save by number value or string, you could compare first and last or loop through everything
                System.out.println("SOMETHING WAS CLOSED");
                sumProcess.setState("STOPPED");
            } else if (currentList.size() < dataAmount && currentList.get(currentList.size()-1).getTimestamp()==timestamp) { //indicates that an application was opened during measuring
                System.out.println("SOMETHING WAS OPENED");
                sumProcess.setState("STARTED");
            } else {
                sumProcess.setState("RUNNING");
            }
            sumProcess.setName(current.getKey());
            sumProcess.setPath(currentList.get(0).getPath());
            sumProcess.setUser(currentList.get(0).getUser());
            sumProcess.calculateAverage(currentList.size());
            sumProcess.setProcessCounter(compareProcessesAmount(currentList)); //TODO: does this work or is nothing saved??????????
            //have to implement way to detect applications themselves closing too (just look if list is different than max value in list)
            applicationDataList.add(sumProcess);
        }
        return applicationDataList;
    }



}
