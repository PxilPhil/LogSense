package org.example.converter;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.common.JSONConverter;
import org.example.model.RunningData;
import org.example.model.SessionComputerData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CSVsToJSONConverter implements JSONConverter {
    private static final Logger LOGGER = LoggerFactory.getLogger(CSVsToJSONConverter.class);
    private final ObjectMapper objectMapper;

    public CSVsToJSONConverter() {
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public String convertSessionComputerDataToJson(SessionComputerData sessionComputerData) {
        String json = "";
        try {
            json = this.objectMapper.writeValueAsString(sessionComputerData);
        } catch (JsonProcessingException e) {
            LOGGER.error("Error while converting the CSVs of the session computer data to JSON:\n" + e);
        }
        return json;
    }

    @Override
    public String convertRunningData(RunningData runningData) {
        String json = "";
        try {
            json = this.objectMapper.writeValueAsString(runningData);
        } catch (JsonProcessingException e) {
            LOGGER.error("Error while converting the CSVs of the monitored data to JSON:\n" + e);
        }
        return json;
    }
}
