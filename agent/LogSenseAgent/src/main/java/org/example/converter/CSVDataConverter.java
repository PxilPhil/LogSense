package org.example.converter;

import org.example.commons.DataConverter;
import org.example.model.ApplicationData;

import java.util.List;

public class CSVDataConverter implements DataConverter {
    public String convertApplicationData(long timestamp, List<ApplicationData> applicationData) {
        StringBuilder csv = new StringBuilder();
        csv.append("timestamp,contextSwitches,majorFaults,bytesRead,bytesWritten,kernelTime,minorFaults,name,path,residentSetSize,upTime,user,userTime,eventHeader,cpu,state");

        for (ApplicationData application : applicationData) {
            csv.append("\n");
            csv.append(timestamp).append(",");
            csv.append(application.getContextSwitches()).append(",");
            csv.append(application.getMajorFaults()).append(",");
            csv.append(application.getBytesRead()).append(",");
            csv.append(application.getBytesWritten()).append(",");
            csv.append(application.getKernelTime()).append(",");
            csv.append(application.getMinorFaults()).append(",");
            csv.append(application.getName()).append(",");
            csv.append(application.getPath()).append(",");
            csv.append(application.getResidentSetSize()).append(",");
            csv.append(application.getUpTime()).append(",");
            csv.append(application.getUser()).append(",");
            csv.append(application.getUserTime()).append(",");
            csv.append(application.getProcessCounter()).append(",");
            csv.append(application.getCpuUsage()).append(",");
            csv.append(application.getState()).append(",");
        }
        return csv.toString();
    }
}
