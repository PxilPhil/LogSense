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
import java.util.List;
import java.util.Map;

public class WritingService { //this class is used to write csv files from other services (where data is further processed)
    public void writeProcessDataToCsv(long timestamp, List<ProcessData> processData) {
        System.out.println("writeProcessDataToCsv");
        List<String[]> processDataString = new ArrayList<>();
        String[] processHeaders = {"timestamp", "name", "residentSetSize"}; //TODO: extend for other things
        processDataString.add(processHeaders);


        for (ProcessData process : processData) {
            String[] record = {String.valueOf(timestamp), process.getName(), String.valueOf(process.getResidentSetSize())};
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
