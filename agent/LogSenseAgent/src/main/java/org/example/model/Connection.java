package org.example.model;

import oshi.software.os.InternetProtocolStats;

import java.net.InetAddress;

public class Connection {
    private InetAddress localAddress;
    private int localPort;
    private InetAddress foreignAddress;
    private int foreignPort;
    private InternetProtocolStats.TcpState state;
    private String type;

    private long owningProcessID;

    public Connection() {
    }

    public InetAddress getLocalAddress() {
        return localAddress;
    }

    public void setLocalAddress(InetAddress localAddress) {
        this.localAddress = localAddress;
    }

    public int getLocalPort() {
        return localPort;
    }

    public void setLocalPort(int localPort) {
        this.localPort = localPort;
    }

    public InetAddress getForeignAddress() {
        return foreignAddress;
    }

    public void setForeignAddress(InetAddress foreignAddress) {
        this.foreignAddress = foreignAddress;
    }

    public int getForeignPort() {
        return foreignPort;
    }

    public void setForeignPort(int foreignPort) {
        this.foreignPort = foreignPort;
    }

    public InternetProtocolStats.TcpState getState() {
        return state;
    }

    public void setState(InternetProtocolStats.TcpState state) {
        this.state = state;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public long getOwningProcessID() {
        return owningProcessID;
    }

    public void setOwningProcessID(long owningProcessID) {
        this.owningProcessID = owningProcessID;
    }
}
