package org.example.model;

public record Process(
        long processId,
        String name,
        int bitness,
        String commandLine,
        String currentWorkingDirectory,
        String path,
        String state,
        String user,
        long contextSwitches,
        long majorFaults,
        long openFiles,
        long residentSetSize,
        long threadCount,
        long upTime,
        double cpuUsage
) {
}
