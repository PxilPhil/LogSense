package org.example.model;

import java.util.Objects;

public record Client(
        long timestamp,
        Computer computer,
        Memory memory,
        Processor processor
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Client client = (Client) o;
        return Objects.equals(computer, client.computer) && Objects.equals(memory, client.memory) && Objects.equals(processor, client.processor);
    }
}

