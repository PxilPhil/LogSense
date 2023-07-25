package org.example.api;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ApiClient {
    private static final Logger LOGGER = LoggerFactory.getLogger(ApiClient.class);
    private final HttpClient httpClient;

    public ApiClient() {
        this.httpClient = HttpClient.newHttpClient();
    }

    public void postSessionComputerData(String sessionComputerDataJSON) {
        try {
            URI uri = new URI("http://127.0.0.1:8000/data/initial");
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .header("Content-type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(sessionComputerDataJSON))
                    .build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            int statusCode = response.statusCode();
            String responseBody = response.body();
            System.out.println("Status code: " + statusCode);
            System.out.println("Response: " + responseBody);
        } catch (URISyntaxException | IOException | InterruptedException e) {
            LOGGER.error("Error while sending a POST request with the session computer data to the REST API of the server: " + e);
        }
    }

    public void postRunningData(String monitoredDataJSON) {
        try {
            URI uri = new URI("http://127.0.0.1:8000/data");
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .header("Content-type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(monitoredDataJSON))
                    .build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            int statusCode = response.statusCode();
            String responseBody = response.body();
            System.out.println("Status code: " + statusCode);
            System.out.println("Response: " + responseBody);
        } catch (URISyntaxException | IOException | InterruptedException e) {
            LOGGER.error("Error while sending a POST request with the monitored data to the REST API of the server: " + e);
        }
    }
}
