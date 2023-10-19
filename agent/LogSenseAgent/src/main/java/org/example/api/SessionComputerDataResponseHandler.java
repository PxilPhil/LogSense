package org.example.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.hc.core5.http.ClassicHttpResponse;
import org.apache.hc.core5.http.HttpException;
import org.apache.hc.core5.http.io.HttpClientResponseHandler;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Map;

public class SessionComputerDataResponseHandler implements HttpClientResponseHandler<Integer> {
    private static final Logger LOGGER = LoggerFactory.getLogger(SessionComputerDataResponseHandler.class);

    @Override
    public Integer handleResponse(ClassicHttpResponse classicHttpResponse) throws HttpException, IOException {
        int statusCode = classicHttpResponse.getCode();
        String responseContent = EntityUtils.toString(classicHttpResponse.getEntity(), StandardCharsets.UTF_8);

        String logMessage = "API POST request to /data/initial: " + statusCode + " - " + responseContent;
        if (statusCode == 200) {
            LOGGER.info(logMessage);
        } else {
            LOGGER.error(logMessage);
        }

        return retrieveStateIdFromResponseContent(responseContent);
    }

    private int retrieveStateIdFromResponseContent(String responseContent) {
        ObjectMapper objectMapper = new ObjectMapper();
        Map<String, Object> jsonObject;
        try {
            jsonObject = objectMapper.readValue(responseContent, new TypeReference<>() {
            });
        } catch (JsonProcessingException e) {
            LOGGER.error("Error while retrieving the returned state ID from the content of the HTTP request: " + e);
            return -1;
        }

        if (jsonObject != null && jsonObject.get("state_id") != null) {
            return (int) jsonObject.get("state_id");
        } else {
            return -1;
        }
    }
}
