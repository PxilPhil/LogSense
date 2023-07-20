package org.example.model;

import java.net.InetAddress;
import java.util.List;

public class NetworkInterface {
    private String displayName;
    private String name;
    private List<InetAddress> ipv4Addresses;
    private List<InetAddress> ipv6Addresses;
    private String macAddress;
    private Short[] subnetMasks;
    private long bytesReceived;
    private long bytesSent;
    private long collisions;
    private long packetsReceived;
    private long packetsSent;

    public NetworkInterface() {
    }

    public NetworkInterface(String displayName, String name, List<InetAddress> ipv4Addresses, List<InetAddress> ipv6Addresses, String macAddress, Short[] subnetMasks, long bytesReceived, long bytesSent, long collisions, long packetsReceived, long packetsSent) {
        this.displayName = displayName;
        this.name = name;
        this.ipv4Addresses = ipv4Addresses;
        this.ipv6Addresses = ipv6Addresses;
        this.macAddress = macAddress;
        this.subnetMasks = subnetMasks;
        this.bytesReceived = bytesReceived;
        this.bytesSent = bytesSent;
        this.collisions = collisions;
        this.packetsReceived = packetsReceived;
        this.packetsSent = packetsSent;
    }

    public String getDisplayName() {
        return displayName;
    }

    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<InetAddress> getIpv4Addresses() {
        return ipv4Addresses;
    }

    public void setIpv4Addresses(List<InetAddress> ipv4Addresses) {
        this.ipv4Addresses = ipv4Addresses;
    }

    public List<InetAddress> getIpv6Addresses() {
        return ipv6Addresses;
    }

    public void setIpv6Addresses(List<InetAddress> ipv6Addresses) {
        this.ipv6Addresses = ipv6Addresses;
    }

    public String getMacAddress() {
        return macAddress;
    }

    public void setMacAddress(String macAddress) {
        this.macAddress = macAddress;
    }

    public Short[] getSubnetMasks() {
        return subnetMasks;
    }

    public void setSubnetMasks(Short[] subnetMasks) {
        this.subnetMasks = subnetMasks;
    }

    public long getBytesReceived() {
        return bytesReceived;
    }

    public void setBytesReceived(long bytesReceived) {
        this.bytesReceived = bytesReceived;
    }

    public long getBytesSent() {
        return bytesSent;
    }

    public void setBytesSent(long bytesSent) {
        this.bytesSent = bytesSent;
    }

    public long getCollisions() {
        return collisions;
    }

    public void setCollisions(long collisions) {
        this.collisions = collisions;
    }

    public long getPacketsReceived() {
        return packetsReceived;
    }

    public void setPacketsReceived(long packetsReceived) {
        this.packetsReceived = packetsReceived;
    }

    public long getPacketsSent() {
        return packetsSent;
    }

    public void setPacketsSent(long packetsSent) {
        this.packetsSent = packetsSent;
    }
}
