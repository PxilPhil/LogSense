package org.example.api;

import org.apache.hc.core5.http.ClassicHttpResponse;
import org.apache.hc.core5.http.HttpException;
import org.apache.hc.core5.http.io.HttpClientResponseHandler;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class RunningDataResponseHandler implements HttpClientResponseHandler<Integer> {
    private static final Logger LOGGER = LoggerFactory.getLogger(RunningDataResponseHandler.class);

    @Override
    public Integer handleResponse(ClassicHttpResponse classicHttpResponse) throws HttpException, IOException {
        int statusCode = classicHttpResponse.getCode();
        String responseContent = EntityUtils.toString(classicHttpResponse.getEntity(), StandardCharsets.UTF_8);

        String logMessage = "API POST request to /data: " + statusCode + " - " + responseContent;
        if (statusCode == 200) {
            LOGGER.info(logMessage);
        } else {
            LOGGER.error(logMessage);
        }

        //TODO: remove prints
        System.out.println(statusCode);
        System.out.println(responseContent);
        return statusCode;
    }
}
