package org.example.model;

import java.util.Objects;

public record Computer(
        String hardwareUUID,
        String manufacturer,
        String model
) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Computer computer = (Computer) o;
        return Objects.equals(hardwareUUID, computer.hardwareUUID) && Objects.equals(manufacturer, computer.manufacturer) && Objects.equals(model, computer.model);
    }
}
