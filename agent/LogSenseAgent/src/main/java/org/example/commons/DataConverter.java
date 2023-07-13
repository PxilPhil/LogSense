package org.example.commons;

import org.example.model.ApplicationData;

import java.util.List;

public interface DataConverter {
    String convertApplicationData(long timestamp, List<ApplicationData> applications);
}
