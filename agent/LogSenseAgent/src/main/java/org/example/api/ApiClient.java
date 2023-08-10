package org.example.api;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.HttpClientResponseHandler;
import org.example.common.DataConverter;
import org.example.converter.CSVDataConverter;
import org.example.model.RunningData;
import org.example.model.SessionComputerData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

public class ApiClient {
    private static final Logger LOGGER = LoggerFactory.getLogger(ApiClient.class);
    private final CloseableHttpClient httpClient;
    private final HttpClientResponseHandler<Integer> sessionComputerDataResponseHandler;
    private final HttpClientResponseHandler<Integer> runningDataResponseHandler;
    private final DataConverter csvDataConverter;

    public ApiClient() {
        this.httpClient = HttpClients.createDefault();
        this.sessionComputerDataResponseHandler = new SessionComputerDataResponseHandler();
        this.runningDataResponseHandler = new RunningDataResponseHandler();
        this.csvDataConverter = new CSVDataConverter();
    }

    public int postSessionComputerData(SessionComputerData sessionComputerData) {
        if (sessionComputerData != null) {
            MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
            multipartEntityBuilder.addBinaryBody("files", this.csvDataConverter.convertClientData(sessionComputerData.client()).getBytes(), ContentType.TEXT_PLAIN, "client");
            multipartEntityBuilder.addBinaryBody("files", this.csvDataConverter.convertDiskStoreData(sessionComputerData.diskStores()).getBytes(), ContentType.TEXT_PLAIN, "disk");
            multipartEntityBuilder.addBinaryBody("files", this.csvDataConverter.convertPartitionData(sessionComputerData.partitions()).getBytes(), ContentType.TEXT_PLAIN, "partition");

            HttpPost httpPost = new HttpPost("http://127.0.0.1:8000/data/initial");
            httpPost.setEntity(multipartEntityBuilder.build());

            try {
                return this.httpClient.execute(httpPost, this.sessionComputerDataResponseHandler);
            } catch (IOException e) {
                LOGGER.error("Error while executing the HTTP POST request for the session computer data: " + e);
                return -1;
            }
        } else {
            return -1;
        }
    }

    public void postRunningData(RunningData runningData, long stateId) {
        if (runningData != null && stateId > 0) {
            MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
            multipartEntityBuilder.addBinaryBody("files", runningData.getApplication_data().getBytes(), ContentType.TEXT_PLAIN, "application");
            multipartEntityBuilder.addBinaryBody("files", runningData.getPc_resources().getBytes(), ContentType.TEXT_PLAIN, "resources");
            multipartEntityBuilder.addBinaryBody("files", runningData.getNetwork_interface().getBytes(), ContentType.TEXT_PLAIN, "network");
            multipartEntityBuilder.addBinaryBody("files", runningData.getConnection_data().getBytes(), ContentType.TEXT_PLAIN, "connection");

            HttpPost httpPost = new HttpPost("http://127.0.0.1:8000/data?stateId=" + stateId);
            httpPost.setEntity(multipartEntityBuilder.build());

            try {
                this.httpClient.execute(httpPost, this.runningDataResponseHandler);
            } catch (IOException e) {
                LOGGER.error("Error while executing the HTTP POST request for the running data: " + e);
            }
        }
    }
}
