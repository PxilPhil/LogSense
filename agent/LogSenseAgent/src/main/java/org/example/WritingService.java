package org.example;

import com.opencsv.CSVWriter;
import org.example.model.ApplicationData;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class WritingService { //this class is used to write csv files from other services (where data is further processed)
    public void writeProcessDataToCsv(long timestamp, List<ApplicationData> applicationData) {
        //unknown if upTime is working that well
        System.out.println("writeProcessDataToCsv");
        List<String[]> processDataString = new ArrayList<>();
        String[] processHeaders = {"timestamp", "contextSwitches", "majorFaults", "bytesRead", "bytesWritten", "kernelTime", "minorFaults", "name", "path", "residentSetSize", "upTime", "user", "userTime", "eventHeader", "cpu"};
        processDataString.add(processHeaders);


        for (ApplicationData process : applicationData) {
            String[] record = {String.valueOf(timestamp), String.valueOf(process.getContextSwitches()), String.valueOf(process.getMajorFaults()), String.valueOf(process.getBytesRead()), String.valueOf(process.getBytesWritten()), String.valueOf(process.getKernelTime()), String.valueOf(process.getMinorFaults()), process.getName(), process.getPath(), String.valueOf(process.getResidentSetSize()), String.valueOf(process.getUpTime()), process.getUser(), String.valueOf(process.getUserTime()), String.valueOf(process.getProcessCounter()), String.valueOf(process.getCpuUsage())};
            processDataString.add(record);
        }

        try {
            CSVWriter writer = new CSVWriter(new FileWriter("C:\\service\\process_" + timestamp + ".csv"));
            writer.writeAll(processDataString);
            writer.flush();
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
