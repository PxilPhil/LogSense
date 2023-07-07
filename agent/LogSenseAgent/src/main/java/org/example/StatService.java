package org.example;

import oshi.software.os.OSProcess;

import java.util.*;

public class StatService {
    //private ArrayList<OSProcess> osProcessList=new ArrayList<>(); //only for processes for now
    private Map<Long, List<OSProcess>> osProcessMap = new TreeMap<>();
    private int counter = 0;
    private int windowSize = 2; //window for average calculation
    private double sens = 0.5; // how sensible the application should register anomalies (50% for now)
    public StatService() {

    }

    public void ingestData(long timestamp, List<OSProcess> osProcesses) {
        this.osProcessMap.put(timestamp, osProcesses);
        counter++;
        System.out.println(counter);

        if (counter%5==0) {
            System.out.println("should calculate deltas now");
            calculateDeltas();
        }
    }
    public void calculateDeltas() {
        long delta = 0;
        long currentRamSize;
        //long previousRamSize = osProcessList.get(0).getResidentSetSize();
        double rollingMean = 0;
        int index = 0;
        Queue<Long> residentSizes = new LinkedList<>();

        for(Map.Entry<Long, List<OSProcess>> entry : this.osProcessMap.entrySet()) { //loop through map

            ArrayList<OSProcess> osProcessList = (ArrayList<OSProcess>) entry.getValue();
            long totalSum = 0;
            for(int i=0; i<osProcessList.size(); i++) { //loop through all saved data for the timestamp

                OSProcess osProcess = osProcessList.get(i);
                currentRamSize = osProcess.getResidentSetSize();
                totalSum+=currentRamSize;
                //delta = currentRamSize - previousRamSize;
                //previousRamSize=currentRamSize;
            }

            //the below part should be put into the above for loop if it should go per process and not overall

            residentSizes.add(totalSum);

            if (index>=windowSize-1) {
                rollingMean = calculateRollingAVG(residentSizes);
                System.out.println(residentSizes);
                residentSizes.remove();

                if (isAnomaly(totalSum, rollingMean)) {
                    System.out.println("Anomaly detected");
                }
            }


            System.out.println("rollingMean "+rollingMean);
            System.out.println("delta "+delta);
            System.out.println("totalSum "+totalSum);
            index++;
        }


        this.osProcessMap=new TreeMap<>(); //clear map
    }

    private boolean isAnomaly(long currentRamSize, double rollingMean) {
        if (currentRamSize > rollingMean && currentRamSize/rollingMean > (1+sens)) {
            return true;
        } else if (currentRamSize < rollingMean && currentRamSize/rollingMean < sens) {
            return true;
        } else {
            return false;
        }
    }

    private double calculateRollingAVG(Queue<Long> residentSizes) {
        long sum = 0;
        for(Long curr : residentSizes) {
            sum+=curr;
        }
        return ((double) sum /windowSize);
    }
}
