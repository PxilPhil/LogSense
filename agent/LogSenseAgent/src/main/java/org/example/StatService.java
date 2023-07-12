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

    /*
    private void writeProcessDataToCsv(OperatingSystem operatingSystem) {
        List<String[]> processData = new ArrayList<>();
        String[] processHeaders = {"timestamp", "contextSwitches", "majorFaults", "processID", "bitness", "bytesRead", "bytesWritten", "commandLine", "currentWorkingDirectory", "kernelTime", "minorFaults", "name", "openFiles", "parentProcessID", "path", "residentSetSize", "startTime", "state", "threadCount", "upTime", "user", "userTime", "virtualSize"};
        processData.add(processHeaders);

        long timestamp = Instant.now().toEpochMilli();
        for (OSProcess process : operatingSystem.getProcesses()) {
            String[] record = {String.valueOf(timestamp), String.valueOf(process.getContextSwitches()), String.valueOf(process.getMajorFaults()), String.valueOf(process.getProcessID()), String.valueOf(process.getBitness()), String.valueOf(process.getBytesRead()), String.valueOf(process.getBytesWritten()), process.getCommandLine(), process.getCurrentWorkingDirectory(), String.valueOf(process.getKernelTime()), String.valueOf(process.getMinorFaults()), process.getName(), String.valueOf(process.getOpenFiles()), String.valueOf(process.getParentProcessID()), process.getPath(), String.valueOf(process.getResidentSetSize()), String.valueOf(process.getStartTime()), process.getState().toString(), String.valueOf(process.getThreadCount()), String.valueOf(process.getUpTime()), process.getUser(), String.valueOf(process.getUserTime()), String.valueOf(process.getVirtualSize())};
            processData.add(record);
        }

        try {
            CSVWriter writer = new CSVWriter(new FileWriter("C:\\test\\process_" + timestamp + ".csv"));
            writer.writeAll(processData);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

     */

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
