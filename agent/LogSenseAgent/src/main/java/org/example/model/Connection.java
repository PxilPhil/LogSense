package org.example.model;

import oshi.software.os.InternetProtocolStats;

import java.net.InetAddress;

public record Connection (
    InetAddress localAddress,
    int localPort,
    InetAddress foreignAddress,
    int foreignPort,
    InternetProtocolStats.TcpState state,
    String type,
    long owningProcessID
) { }
