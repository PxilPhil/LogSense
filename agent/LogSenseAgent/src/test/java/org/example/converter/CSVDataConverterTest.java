package org.example.converter;

import org.example.common.DataConverter;
import org.example.model.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import oshi.software.os.InternetProtocolStats;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CSVDataConverterTest {
    private DataConverter converter;

    @BeforeEach
    void setUp() {
        this.converter = new CSVDataConverter();
    }

    @Test
    void convertApplicationDataCorrectly() {
        List<Application> applications = getTestApplications();

        String expectedResult = """
                timestamp|contextSwitches|majorFaults|bitness|commandLine|currentWorkingDirectory|name|openFiles|parentProcessID|path|residentSetSize|state|threadCount|upTime|user|processCountDifference|cpuUsage
                1689854981|1|0|64|TestCommandLine|TestCurrentWorkingDirectory|TestName|12|217|TestPath|12051|RUNNING|4|37|TestUser|1|1.07
                1689854981|4|2|64|TestCommandLine2|TestCurrentWorkingDirectory2|TestName2|5|1951|TestPath2|9871|RUNNING|7|60|TestUser2|3|0.54
                """;
        String actualResult = this.converter.convertApplicationData(1689854981, applications);

        assertEquals(expectedResult, actualResult);
    }

    private List<Application> getTestApplications() {
        List<Application> applications = new ArrayList<>();
        Application application = new Application(1,0,64,"TestCommandLine",
                "TestCurrentWorkingDirectory","TestName",12,217,
                "TestPath",12051,1689854901,"RUNNING",4,37,
                "TestUser",1.07,1,1689854981);
        Application application2 = new Application(4,2, 64,
                "TestCommandLine2","TestCurrentWorkingDirectory2","TestName2",
                5,1951,"TestPath2",9871,1689854901,"RUNNING",
                7,60,"TestUser2",0.54,3,1689854981);
        applications.add(application);
        applications.add(application2);
        return applications;
    }

    @Test
    void convertApplicationDataWithTimestampInTheFutureReturnsNull() {
        List<Application> applications = getTestApplications();

        String result = this.converter.convertApplicationData(Instant.now().toEpochMilli() + 50, applications);

        assertNull(result);
    }

    @Test
    void convertApplicationDataWithNullApplicationListThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.converter.convertApplicationData(Instant.now().toEpochMilli(), null));
    }

    @Test
    void convertApplicationDataWithEmptyApplicationListReturnsOnlyHeader() {
        String expectedResult = "timestamp|contextSwitches|majorFaults|bitness|commandLine|currentWorkingDirectory|" +
                "name|openFiles|parentProcessID|path|residentSetSize|state|threadCount|upTime|user|" +
                "processCountDifference|cpuUsage\n";
        String actualResult = this.converter.convertApplicationData(Instant.now().toEpochMilli(), new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertResourceDataCorrectly() {
        Resources resources = getTestResources();

        String expectedResult = """
                timestamp|freeDiskSpace|readBytesDiskStores|readsDiskStores|writeBytesDiskStores|writesDiskStores|partitionsMajorFaults|partitionsMinorFaults|availableMemory|namesPowerSources|chargingPowerSources|dischargingPowerSources|powerOnLinePowerSources|remainingCapacityPercentPowerSources|contextSwitchesProcessor|interruptsProcessor
                1689853788|100000000000|241541|241541|241541|241541|241541|241541|12000000000|TestPowerSourceName|true|true|true|82.5|8171|131
                """;
        String actualResult = this.converter.convertResourceData(1689853788, resources);

        assertEquals(expectedResult, actualResult);
    }

    private Resources getTestResources() {
        List<Long> diskStoresTestData = new ArrayList<>();
        diskStoresTestData.add(241541L);

        List<String> powerSourcesNames = new ArrayList<>();
        powerSourcesNames.add("TestPowerSourceName");

        List<Boolean> powerSourcesTestData = new ArrayList<>();
        powerSourcesTestData.add(true);

        List<Double> powerSourcesRemainingCapacityPercent = new ArrayList<>();
        powerSourcesRemainingCapacityPercent.add(82.5);

        return new Resources(100000000000L, diskStoresTestData, diskStoresTestData,
                diskStoresTestData, diskStoresTestData, diskStoresTestData, diskStoresTestData,
                12000000000L, powerSourcesNames, powerSourcesTestData, powerSourcesTestData,
                powerSourcesTestData, powerSourcesRemainingCapacityPercent, 8171L,
                131L);
    }

    @Test
    void convertResourceDataWithTimestampInTheFutureReturnsNull() {
        Resources resources = getTestResources();

        String result = this.converter.convertResourceData(Instant.now().toEpochMilli() + 50, resources);

        assertNull(result);
    }

    @Test
    void convertResourceDataWithNullResourcesThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.converter.convertResourceData(Instant.now().toEpochMilli(),
                null));
    }

    @Test
    void convertConnectionDataCorrectly() throws UnknownHostException {
        List<Connection> connections = new ArrayList<>();
        Connection connection = new Connection(InetAddress.getByName("127.0.0.1"), 443,
                InetAddress.getByName("145.2.93.14"), 3219, InternetProtocolStats.TcpState.ESTABLISHED,
                "tcp4", 310);
        Connection connection2 = new Connection(InetAddress.getByName("127.0.0.1"), 22,
                InetAddress.getByName("175.0.5.165"), 19515, InternetProtocolStats.TcpState.ESTABLISHED,
                "tcp4", 4191);
        connections.add(connection);
        connections.add(connection2);

        String expectedResult = """
                timestamp|localAddress|localPort|foreignAddress|foreignPort|state|type|owningProcessID
                1689852778|/127.0.0.1|443|/145.2.93.14|3219|ESTABLISHED|tcp4|310
                1689852778|/127.0.0.1|22|/175.0.5.165|19515|ESTABLISHED|tcp4|4191
                """;
        String actualResult = this.converter.convertConnectionData(1689852778, connections);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertConnectionDataWithTimestampInTheFutureReturnsNull() throws UnknownHostException {
        List<Connection> connections = new ArrayList<>();
        Connection connection = new Connection(InetAddress.getByName("127.0.0.1"), 443,
                InetAddress.getByName("145.2.93.14"), 3219, InternetProtocolStats.TcpState.ESTABLISHED,
                "tcp4", 310);
        Connection connection2 = new Connection(InetAddress.getByName("127.0.0.1"), 22,
                InetAddress.getByName("175.0.5.165"), 19515, InternetProtocolStats.TcpState.ESTABLISHED,
                "tcp4", 4191);
        connections.add(connection);
        connections.add(connection2);

        String result = this.converter.convertConnectionData(Instant.now().toEpochMilli() + 50, connections);

        assertNull(result);
    }

    @Test
    void convertConnectionDataWithNullConnectionListReturnsNull() {
        String result = this.converter.convertConnectionData(Instant.now().toEpochMilli(), null);

        assertNull(result);
    }

    @Test
    void convertConnectionDataWithEmptyConnectionListReturnsOnlyHeader() {
        String expectedResult = "timestamp|localAddress|localPort|foreignAddress|foreignPort|state|type|" +
                "owningProcessID\n";
        String actualResult = this.converter.convertConnectionData(Instant.now().toEpochMilli(), new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertNetworkInterfacesDataCorrectly() throws UnknownHostException {
        List<NetworkInterface> networkInterfaces = new ArrayList<>();

        List<InetAddress> ipv4Addresses = new ArrayList<>();
        InetAddress ipv4Address = InetAddress.getByName("172.10.0.1");
        ipv4Addresses.add(ipv4Address);

        List<InetAddress> ipv6Addresses = new ArrayList<>();
        InetAddress ipv6Address = InetAddress.getByName("2001:0db8:85a3:0000:0000:8a2e:0370:7334");
        ipv6Addresses.add(ipv6Address);

        Short[] subnetMasks = {24};

        NetworkInterface networkInterface = new NetworkInterface("TestDisplayName", "TestName",
                ipv4Addresses, ipv6Addresses, "TestMacAddress", subnetMasks, 4105,
                14341, 3, 41, 12);
        NetworkInterface networkInterface2 = new NetworkInterface("TestDisplayName2", "TestName2",
                ipv4Addresses, ipv6Addresses, "TestMacAddress2", subnetMasks, 1491,
                319, 1, 13, 14);

        networkInterfaces.add(networkInterface);
        networkInterfaces.add(networkInterface2);

        String expectedResult = """
                timestamp|displayName|name|ipv4Address|ipv6Address|macAddress|subnetMask|bytesReceived|bytesSent|collisions|packetsReceived|packetsSent
                1689851203|TestDisplayName|TestName|/172.10.0.1|/2001:db8:85a3:0:0:8a2e:370:7334|TestMacAddress|24|4105|14341|3|41|12
                1689851203|TestDisplayName2|TestName2|/172.10.0.1|/2001:db8:85a3:0:0:8a2e:370:7334|TestMacAddress2|24|1491|319|1|13|14
                """;
        String actualResult = this.converter.convertNetworkInterfacesData(1689851203, networkInterfaces);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertNetworkInterfacesDataWithTimestampInTheFutureReturnsNull() throws UnknownHostException {
        List<NetworkInterface> networkInterfaces = new ArrayList<>();

        List<InetAddress> ipv4Addresses = new ArrayList<>();
        InetAddress ipv4Address = InetAddress.getByName("172.10.0.1");
        ipv4Addresses.add(ipv4Address);

        List<InetAddress> ipv6Addresses = new ArrayList<>();
        InetAddress ipv6Address = InetAddress.getByName("2001:0db8:85a3:0000:0000:8a2e:0370:7334");
        ipv6Addresses.add(ipv6Address);

        Short[] subnetMasks = {24};

        NetworkInterface networkInterface = new NetworkInterface("TestDisplayName", "TestName",
                ipv4Addresses, ipv6Addresses, "TestMacAddress", subnetMasks, 4105,
                14341, 3, 41, 12);
        NetworkInterface networkInterface2 = new NetworkInterface("TestDisplayName2", "TestName2",
                ipv4Addresses, ipv6Addresses, "TestMacAddress2", subnetMasks, 1491,
                319, 1, 13, 14);

        networkInterfaces.add(networkInterface);
        networkInterfaces.add(networkInterface2);

        String result = this.converter.convertNetworkInterfacesData(Instant.now().toEpochMilli() + 50,
                networkInterfaces);

        assertNull(result);
    }

    @Test
    void convertNetworkInterfacesDataWithNullNetworkInterfaceListThrowsNPE() {
        assertThrows(NullPointerException.class,
                () -> this.converter.convertNetworkInterfacesData(Instant.now().toEpochMilli(), null));
    }

    @Test
    void convertNetworkInterfacesDataWithEmptyNetworkInterfaceListReturnsOnlyHeader() {
        String expectedResult = "timestamp|displayName|name|ipv4Address|ipv6Address|macAddress|subnetMask|" +
                "bytesReceived|bytesSent|collisions|packetsReceived|packetsSent\n";
        String actualResult = this.converter.convertNetworkInterfacesData(Instant.now().toEpochMilli(), new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertClientDataCorrectly() {
        long timestamp = Instant.now().toEpochMilli();

        Computer computer = new Computer("TestHardwareUUID", "TestManufacturer",
                "TestModel");
        Memory memory = new Memory(16000000000L, 4096000L);
        Processor processor = new Processor("TestName", "TestIdentifier", "TestID",
                "TestVendor", 64, 1, 8, 16);
        Client client = new Client(timestamp, computer, memory, processor);

        String expectedResult = "measurement_time|computerHardwareUUID|computerManufacturer|computerModel|memoryTotalSize|memoryPageSize|processorName|processorIdentifier|processorID|processorVendor|processorBitness|physicalPackageCount|physicalProcessorCount|logicalProcessorCount\n" +
                timestamp + "|TestHardwareUUID|TestManufacturer|TestModel|16000000000|4096000|TestName|TestIdentifier|TestID|TestVendor|64|1|8|16\n";
        String actualResult = this.converter.convertClientData(client);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertClientDataWithNullClientThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.converter.convertClientData(null));
    }

    @Test
    void convertDiskStoreDataCorrectly() {
        long timestamp = Instant.now().toEpochMilli();
        List<DiskStore> diskStores = new ArrayList<>();
        DiskStore diskStore = new DiskStore(timestamp, "Test Serial number",
                "TestModel", "TestName", 1024000000000L);
        DiskStore diskStore2 = new DiskStore(timestamp, "Test Serial number",
                "TestModel2", "TestName2", 128000000000L);
        diskStores.add(diskStore);
        diskStores.add(diskStore2);

        String expectedResult = "measurement_time|serialNumber|model|name|size\n"
                + timestamp + "|Test Serial number|TestModel|TestName|1024000000000\n" +
                timestamp + "|Test Serial number|TestModel2|TestName2|128000000000\n";
        String actualResult = this.converter.convertDiskStoreData(diskStores);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertDiskStoreDataWithNullDiskStoreListThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.converter.convertDiskStoreData(null));
    }

    @Test
    void convertDiskStoreDataWithEmptyDiskStoreListReturnsOnlyHeader() {
        String expectedResult = "measurement_time|serialNumber|model|name|size\n";
        String actualResult = this.converter.convertDiskStoreData(new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertPartitionDataCorrectly() {
        long timestamp = Instant.now().toEpochMilli();
        List<Partition> partitions = new ArrayList<>();
        Partition partition = new Partition(timestamp, "TestDiskStoreName",
                "TestIdentifier", "TestName", "TestType", "TestMountPoint",
                1024000000000L, 3L, 522L);
        Partition partition2 = new Partition(timestamp, "TestDiskStoreName2",
                "TestIdentifier2", "TestName2", "TestType2", "TestMountPoint2",
                512000000000L, 0L, 12L);
        partitions.add(partition);
        partitions.add(partition2);

        String expectedResult = "measurement_time|diskStoreName|identification|name|type|mountPoint|size|" +
                "majorFaults|minorFaults\n"
                + timestamp + "|TestDiskStoreName|TestIdentifier|TestName|TestType|TestMountPoint|1024000000000|3|522\n"
                + timestamp + "|TestDiskStoreName2|TestIdentifier2|TestName2|TestType2|TestMountPoint2|512000000000|0|12\n";
        String actualResult = this.converter.convertPartitionData(partitions);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertPartitionDataWithNullPartitionListThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.converter.convertPartitionData(null));
    }

    @Test
    void convertPartitionDataWithEmptyPartitionListReturnsOnlyHeader() {
        String expectedResult = "measurement_time|diskStoreName|identification|name|type|mountPoint|size|majorFaults|minorFaults\n";
        String actualResult = this.converter.convertPartitionData(new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }
}