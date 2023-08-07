package org.example.model;

import java.util.Objects;

public class Computer {
    private String hardwareUUID;
    private String manufacturer;
    private String model;

    public Computer() {
    }

    public Computer(String hardwareUUID, String manufacturer, String model) {
        this.hardwareUUID = hardwareUUID;
        this.manufacturer = manufacturer;
        this.model = model;
    }

    public String getHardwareUUID() {
        return hardwareUUID;
    }

    public void setHardwareUUID(String hardwareUUID) {
        this.hardwareUUID = hardwareUUID;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Computer computer = (Computer) o;
        return Objects.equals(hardwareUUID, computer.hardwareUUID) && Objects.equals(manufacturer, computer.manufacturer) && Objects.equals(model, computer.model);
    }
}
