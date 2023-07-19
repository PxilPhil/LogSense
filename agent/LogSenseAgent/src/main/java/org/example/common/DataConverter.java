package org.example.common;

import org.example.model.*;

import java.util.List;

public interface DataConverter {
    String convertApplicationData(long timestamp, List<Application> applications);

    String convertResourceData(long timestamp, Resources resources);

    String convertConnectionData(long timestamp, List<Connection> connectionData);

    String convertNetworkInterfacesData(long timestamp, List<NetworkInterface> networkInterfaces);

    String convertClientData(long timestamp, Client client);

    String convertDiskStoreData(List<DiskStore> diskStores);

    String convertPartitionData(List<Partition> partitions);
}
