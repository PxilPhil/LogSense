package org.example.model;

import java.util.Objects;

public class Client {
    private long timestamp;
    private Computer computer;
    private Memory memory;
    private Processor processor;

    public Client() {
    }

    public Client(long timestamp, Computer computer, Memory memory, Processor processor) {
        this.timestamp = timestamp;
        this.computer = computer;
        this.memory = memory;
        this.processor = processor;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public Computer getComputer() {
        return computer;
    }

    public void setComputer(Computer computer) {
        this.computer = computer;
    }

    public Memory getMemory() {
        return memory;
    }

    public void setMemory(Memory memory) {
        this.memory = memory;
    }

    public Processor getProcessor() {
        return processor;
    }

    public void setProcessor(Processor processor) {
        this.processor = processor;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Client client = (Client) o;
        return Objects.equals(computer, client.computer) && Objects.equals(memory, client.memory) && Objects.equals(processor, client.processor);
    }

}
