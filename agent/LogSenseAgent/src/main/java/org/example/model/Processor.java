package org.example.model;

public class Processor {
    private String name;
    private String identifier;
    private String ID;
    private String vendor;
    private int bitness;
    private int physicalPackageCount;
    private int physicalProcessorCount;
    private int logicalProcessorCount;

    public Processor() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIdentifier() {
        return identifier;
    }

    public void setIdentifier(String identifier) {
        this.identifier = identifier;
    }

    public String getID() {
        return ID;
    }

    public void setID(String ID) {
        this.ID = ID;
    }

    public String getVendor() {
        return vendor;
    }

    public void setVendor(String vendor) {
        this.vendor = vendor;
    }

    public int getBitness() {
        return bitness;
    }

    public void setBitness(int bitness) {
        this.bitness = bitness;
    }

    public int getPhysicalPackageCount() {
        return physicalPackageCount;
    }

    public void setPhysicalPackageCount(int physicalPackageCount) {
        this.physicalPackageCount = physicalPackageCount;
    }

    public int getPhysicalProcessorCount() {
        return physicalProcessorCount;
    }

    public void setPhysicalProcessorCount(int physicalProcessorCount) {
        this.physicalProcessorCount = physicalProcessorCount;
    }

    public int getLogicalProcessorCount() {
        return logicalProcessorCount;
    }

    public void setLogicalProcessorCount(int logicalProcessorCount) {
        this.logicalProcessorCount = logicalProcessorCount;
    }
}
