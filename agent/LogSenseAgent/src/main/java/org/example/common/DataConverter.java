package org.example.common;

import org.example.model.ApplicationData;
import org.example.model.ResourcesData;

import java.util.List;

public interface DataConverter {
    String convertApplicationData(long timestamp, List<ApplicationData> applications);

    String convertResourceData(long timestamp, ResourcesData resourcesData);
}
