package org.example;

import org.example.model.ProcessData;
import oshi.software.os.OSProcess;

import java.util.*;

public class StatService {
    //private ArrayList<OSProcess> osProcessList=new ArrayList<>(); //only for processes for now
    private Map<String, List<ProcessData>> processDataMap = new TreeMap<>();
    private int dataAmount = 0;
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
        this.processDataMap = performMerging(osProcesses);


        if (timestamp >= (lastTimestamp + this.timeDifference * 1000)) { //if X amount has passed since the last timeStamp
            lastTimestamp = timestamp;
            List<ProcessData> stats = calculateStats();
            //write into csv and view in console
            writingService.writeProcessDataToCsv(lastTimestamp, stats);
            processDataMap.clear();
        }

    }


    private Map<String, List<ProcessData>> performMerging(List<OSProcess> processList) { //merges processes into applications
        //create map to assign and access values better, then turn that into a normal list
        Map<String, ProcessData> osProcessMapTemp = new TreeMap<>();
        for (OSProcess process : processList) {
            String name = process.getName();

            ProcessData processData;
            if (osProcessMapTemp.containsKey(name)) {
                processData = osProcessMapTemp.get(name);
            } else {
                processData = new ProcessData();
                processData.setUser(process.getUser());
                processData.setPath(process.getPath());

            }
            processData.mergeData(process.getResidentSetSize(), process.getBytesRead(), process.getBytesWritten(), process.getKernelTime(), process.getMajorFaults(), process.getMinorFaults(), process.getThreadCount(), process.getContextSwitches(), process.getUpTime(), process.getUserTime());
            osProcessMapTemp.put(name, processData);
        }


        //insert into existing map
        for(Map.Entry<String, ProcessData> current : osProcessMapTemp.entrySet()) {
            List<ProcessData> processDataList;
            String key = current.getKey();
            if (processDataMap.containsKey(key)) { //if it contains key just get ProcessData
                processDataList = processDataMap.get(key);
            } else {
                processDataList = new ArrayList<>();
            }
            processDataList.add(current.getValue());
            processDataMap.put(key, processDataList);
        }

        return processDataMap;
    }

    private long calculateCPUUsage(OSProcess osProcess, long prev) { //calculates cpu usage per proces
        long timeDiff = (osProcess.getKernelTime()+osProcess.getUserTime()) - prev;
        return (100 * (timeDiff/osProcess.getUpTime()));
    }

    private List<ProcessData> calculateStats() { //does statistical calculations on minutely data (keep in mind that everything not transfered here will be lost)
        this.dataAmount = 0;
        List<ProcessData> processDataList = new ArrayList<>();
        for(Map.Entry<String, List<ProcessData>> current : this.processDataMap.entrySet()) {

            List<ProcessData> currentList = current.getValue();
            ProcessData sumProcess = new ProcessData();
            for(ProcessData process : currentList) {
                sumProcess.mergeData(process.getResidentSetSize(), process.getBytesRead(), process.getBytesWritten(), process.getKernelTime(), process.getMajorFaults(), process.getMinorFaults(), process.getThreadCount(), process.getContextSwitches(), process.getUpTime(), process.getUserTime());
            }
            sumProcess.setName(current.getKey());
            sumProcess.setPath(currentList.get(0).getPath());
            sumProcess.setUser(currentList.get(0).getUser());
            sumProcess.calculateAverage(currentList.size());
            processDataList.add(sumProcess);
        }
        return processDataList;
    }



}
