package org.example.api;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ApiClientTest {
    private ApiClient apiClient;

    @BeforeEach
    void setUp() {
        this.apiClient = new ApiClient();
    }

    @Test
    void postSessionComputerDataWithNullSessionComputerDataReturnsMinusOne() {
        int actualStateId = this.apiClient.postSessionComputerData(null);

        assertEquals(-1, actualStateId);
    }
}
