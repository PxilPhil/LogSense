package org.example.api;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ApiClientTest {
    private static final String CLIENT_BASE_URL = "http://localhost:8000";
    private ApiClient apiClient;

    @BeforeEach
    void setUp() {
        this.apiClient = new ApiClient(CLIENT_BASE_URL);
    }

    @Test
    void postSessionComputerDataWithNullSessionComputerDataThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.apiClient.postSessionComputerData(null));
    }

    @Test
    void postRunningDataWithNullRunningDataThrowsNPE() {
        assertThrows(NullPointerException.class, () -> this.apiClient.postRunningData(null, 1));
    }
}
