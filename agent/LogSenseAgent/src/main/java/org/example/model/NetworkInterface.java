package org.example.model;

import java.net.InetAddress;
import java.util.List;

public record NetworkInterface(
        String displayName,
        String name,
        List<InetAddress> ipv4Addresses,
        List<InetAddress> ipv6Addresses,
        String macAddress,
        Short[] subnetMasks,
        long bytesReceived,
        long bytesSent,
        long collisions,
        long packetsReceived,
        long packetsSent
) {
}
