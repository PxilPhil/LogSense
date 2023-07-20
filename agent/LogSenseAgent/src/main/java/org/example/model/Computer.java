package org.example.model;

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
}
