package org.example;

import org.example.controller.Agent;

public class Main {

    private static final String CLIENT_BASE_URL = "http://localhost:8000";

    public static void main(String[] args) {
        Agent agent = new Agent(CLIENT_BASE_URL);
        agent.monitor();
    }
}
