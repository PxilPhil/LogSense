package org.example.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ClassicHttpResponse;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.ParseException;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.example.model.RunningData;
import org.example.model.SessionComputerData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Map;

public class ApiClient {
    private static final Logger LOGGER = LoggerFactory.getLogger(ApiClient.class);
    private final CloseableHttpClient httpClient;

    public ApiClient() {
        this.httpClient = HttpClients.createDefault();
    }

    public int postSessionComputerData(SessionComputerData sessionComputerData) {
        MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
        multipartEntityBuilder.addBinaryBody("files", sessionComputerData.getClient_data().getBytes(), ContentType.TEXT_PLAIN, "client");
        multipartEntityBuilder.addBinaryBody("files", sessionComputerData.getDisks().getBytes(), ContentType.TEXT_PLAIN, "disk");
        multipartEntityBuilder.addBinaryBody("files", sessionComputerData.getPartition().getBytes(), ContentType.TEXT_PLAIN, "partition");

        HttpPost httpPost = new HttpPost("http://127.0.0.1:8000/data/initial");
        httpPost.setEntity(multipartEntityBuilder.build());

        try {
            ClassicHttpResponse response = this.httpClient.execute(httpPost);
            int statusCode = response.getCode();
            HttpEntity responseEntity = response.getEntity();
            String responseContent = EntityUtils.toString(responseEntity, StandardCharsets.UTF_8);

            String logMessage = "API POST request to /data/initial: " + statusCode + " - " + responseContent;
            if (statusCode == 200) {
                LOGGER.info(logMessage);
            } else {
                LOGGER.error(logMessage);
            }

            //TODO: remove prints
            System.out.println(statusCode);
            System.out.println(responseContent);

            return retrieveStateIdFromResponseContent(responseContent);
        } catch (IOException e) {
            LOGGER.error("Error while executing the HTTP POST request for the session computer data: " + e);
            return -1;
        } catch (ParseException e) {
            LOGGER.error("Error while getting the response content from the HTTP response: " + e);
            return -1;
        }
    }

    private int retrieveStateIdFromResponseContent(String responseContent) {
        ObjectMapper objectMapper = new ObjectMapper();
        Map<String, Object> jsonObject;
        try {
            jsonObject = objectMapper.readValue(responseContent, Map.class);
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

    public void postRunningData(RunningData runningData, long stateId) {
        MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
        multipartEntityBuilder.addBinaryBody("files", runningData.getApplication_data().getBytes(), ContentType.TEXT_PLAIN, "application");
        multipartEntityBuilder.addBinaryBody("files", runningData.getPc_resources().getBytes(), ContentType.TEXT_PLAIN, "resources");
        multipartEntityBuilder.addBinaryBody("files", runningData.getNetwork_interface().getBytes(), ContentType.TEXT_PLAIN, "network");
        multipartEntityBuilder.addBinaryBody("files", runningData.getConnection_data().getBytes(), ContentType.TEXT_PLAIN, "connection");

        HttpPost httpPost = new HttpPost("http://127.0.0.1:8000/data?stateId=" + stateId);
        httpPost.setEntity(multipartEntityBuilder.build());

        try {
            ClassicHttpResponse response = this.httpClient.execute(httpPost);
            int statusCode = response.getCode();
            HttpEntity httpEntity = response.getEntity();
            String responseContent = EntityUtils.toString(httpEntity, StandardCharsets.UTF_8);

            String logMessage = "API POST request to /data: " + statusCode + " - " + responseContent;
            if (statusCode == 200) {
                LOGGER.info(logMessage);
            } else {
                LOGGER.error(logMessage);
            }

            //TODO: remove prints
            System.out.println(statusCode);
            System.out.println(responseContent);
        } catch (IOException e) {
            LOGGER.error("Error while executing the HTTP POST request for the running data: " + e);
        } catch (ParseException e) {
            LOGGER.error("Error while getting the response content from the HTTP response: " + e);
        }
    }
}
