package org.example.model;

public class Client {
    private Computer computer;
    private Memory memory;
    private Processor processor;

    public Client() {
    }

    public Client(Computer computer, Memory memory, Processor processor) {
        this.computer = computer;
        this.memory = memory;
        this.processor = processor;
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
}
