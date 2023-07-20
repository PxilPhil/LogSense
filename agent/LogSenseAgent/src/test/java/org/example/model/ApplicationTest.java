package org.example.model;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import oshi.software.os.OSProcess;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;

class ApplicationTest {
    private Application application;

    @BeforeEach
    void setUp() {
        this.application = new Application();
    }

    @Test
    void addProcessCorrectly() {
        OSProcess osProcessMock = mock(OSProcess.class);

        this.application.addProcess(osProcessMock, 20.0);

        assertEquals(1, this.application.getContainedProcessesMap().size());
    }

    @Test
    void addProcessWithNullOsProcessDoesNotAddProcess() {
        this.application.addProcess(null, 20.0);
        assertEquals(0, this.application.getContainedProcessesMap().size());
    }

    @Test
    void addProcessWithNegativeCpuUsageDoesNotAddProcess() {
        OSProcess osProcessMock = mock(OSProcess.class);

        this.application.addProcess(osProcessMock, -10.0);

        assertEquals(0, this.application.getContainedProcessesMap().size());
    }

    @Test
    void mergeDataCorrectly() {
        this.application.mergeData(1, 2, 3, 4, 5, 6);

        assertEquals(1, this.application.getContextSwitches());
        assertEquals(2, this.application.getMajorFaults());
        assertEquals(3, this.application.getOpenFiles());
        assertEquals(4, this.application.getResidentSetSize());
        assertEquals(5, this.application.getThreadCount());
        assertEquals(6, this.application.getUpTime());
    }

    @Test
    void mergeDataWithNegativeParamsAddsZero() {
        this.application.mergeData(-1, -2, -3, -4, -5, -6);

        assertEquals(0, this.application.getContextSwitches());
        assertEquals(0, this.application.getMajorFaults());
        assertEquals(0, this.application.getOpenFiles());
        assertEquals(0, this.application.getResidentSetSize());
        assertEquals(0, this.application.getThreadCount());
        assertEquals(0, this.application.getUpTime());
    }

    @Test
    void calculateAverageCorrectly() {
        this.application.setContextSwitches(5);
        this.application.setMajorFaults(10);
        this.application.setOpenFiles(15);
        this.application.setResidentSetSize(20);
        this.application.setThreadCount(25);
        this.application.setCpuUsage(30);

        this.application.calculateAverage(5);

        assertEquals(1, this.application.getContextSwitches());
        assertEquals(2, this.application.getMajorFaults());
        assertEquals(3, this.application.getOpenFiles());
        assertEquals(4, this.application.getResidentSetSize());
        assertEquals(5, this.application.getThreadCount());
        assertEquals(6, this.application.getCpuUsage());
    }

    @Test
    void calculateAverageWithZeroAmountDoesNotCalculateAverage() {
        this.application.setContextSwitches(5);
        this.application.setMajorFaults(10);
        this.application.setOpenFiles(15);
        this.application.setResidentSetSize(20);
        this.application.setThreadCount(25);
        this.application.setCpuUsage(30);

        this.application.calculateAverage(0);

        assertEquals(5, this.application.getContextSwitches());
        assertEquals(10, this.application.getMajorFaults());
        assertEquals(15, this.application.getOpenFiles());
        assertEquals(20, this.application.getResidentSetSize());
        assertEquals(25, this.application.getThreadCount());
        assertEquals(30, this.application.getCpuUsage());
    }

    @Test
    void calculateAverageWithNegativeAmountDoesNotCalculateAverage() {
        this.application.setContextSwitches(5);
        this.application.setMajorFaults(10);
        this.application.setOpenFiles(15);
        this.application.setResidentSetSize(20);
        this.application.setThreadCount(25);
        this.application.setCpuUsage(30);

        this.application.calculateAverage(-2);

        assertEquals(5, this.application.getContextSwitches());
        assertEquals(10, this.application.getMajorFaults());
        assertEquals(15, this.application.getOpenFiles());
        assertEquals(20, this.application.getResidentSetSize());
        assertEquals(25, this.application.getThreadCount());
        assertEquals(30, this.application.getCpuUsage());
    }
}