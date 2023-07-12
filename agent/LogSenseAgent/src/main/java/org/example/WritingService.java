package org.example;

import com.opencsv.CSVWriter;
import org.example.model.ProcessData;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

import java.io.FileWriter;
import java.io.IOException;
import java.sql.Timestamp;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class WritingService { //this class is used to write csv files from other services (where data is further processed)
    public void writeProcessDataToCsv(long timestamp, List<ProcessData> processData) {
        //unknown if upTime is working that well
        System.out.println("writeProcessDataToCsv");
        List<String[]> processDataString = new ArrayList<>();
        String[] processHeaders = {"timestamp", "contextSwitches", "majorFaults", "bytesRead", "bytesWritten", "kernelTime", "minorFaults", "name", "path", "residentSetSize", "upTime", "user", "userTime"};
        processDataString.add(processHeaders);


        for (ProcessData process : processData) {
            String[] record = {String.valueOf(timestamp), String.valueOf(process.getContextSwitches()), String.valueOf(process.getMajorFaults()), String.valueOf(process.getBytesRead()), String.valueOf(process.getBytesWritten()), String.valueOf(process.getKernelTime()), String.valueOf(process.getMinorFaults()), process.getName(), process.getPath(), String.valueOf(process.getResidentSetSize()), String.valueOf(process.getUpTime()), process.getUser(), String.valueOf(process.getUserTime())};
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
