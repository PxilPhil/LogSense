package org.example;

import org.example.controller.Agent;

public class Main {
    private static final String CLIENT_BASE_URL = "http://localhost:8000";
    private static final String SUPPORTED_OPERATING_SYSTEM = "Windows";

    public static void main(String[] args) {
        Agent agent = new Agent(CLIENT_BASE_URL, SUPPORTED_OPERATING_SYSTEM);
        agent.monitor();
    }
}
