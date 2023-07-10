package org.example;

import org.example.model.ProcessData;
import oshi.software.os.OSProcess;

import java.util.*;

public class StatService {
    //private ArrayList<OSProcess> osProcessList=new ArrayList<>(); //only for processes for now
    private Map<String, List<ProcessData>> processDataMap = new TreeMap<>();
    private int dataAmount = 0;
    private int timeDifference = 60; //performs operations every 10 seconds
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
            System.out.println("Stats for ");
            //write into csv and view in console
            for(ProcessData processData : stats) {
                System.out.println(processData.getName()+" "+processData.getResidentSetSize());
            }
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
            }
            processData.setResidentSetSize(processData.getResidentSetSize()+process.getResidentSetSize());
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

    private List<ProcessData> calculateStats() { //does statistical calculations on minutely data
        this.dataAmount = 0;
        List<ProcessData> processDataList = new ArrayList<>();
        for(Map.Entry<String, List<ProcessData>> current : this.processDataMap.entrySet()) {

            List<ProcessData> currentList = current.getValue();
            long sum = 0;
            for(ProcessData curr : currentList) {
                sum += curr.getResidentSetSize();
            }
            ProcessData processData = new ProcessData();
            processData.setName(current.getKey());
            processData.setResidentSetSize(sum/currentList.size());
            processDataList.add(processData);
        }
        return processDataList;
    }
}
