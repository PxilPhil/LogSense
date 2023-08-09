package org.example.converter;

import org.example.common.ListToStringConverter;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ListToStringSpacesConverterTest {
    private ListToStringConverter<Integer> listToStringConverter;

    @BeforeEach
    void setUp() {
        this.listToStringConverter = new ListToStringSpacesConverter();
    }

    @Test
    void convertCorrectly() {
        List<Integer> integerList = new ArrayList<>();
        integerList.add(3);
        integerList.add(18);
        integerList.add(7);
        integerList.add(412);

        String expectedResult = "3 18 7 412";
        String actualResult = this.listToStringConverter.convert(integerList);

        assertEquals(expectedResult, actualResult);
    }

    @Test
    void convertWithNullListReturnsNull() {
        String result = this.listToStringConverter.convert(null);

        assertNull(result);
    }

    @Test
    void convertWithEmptyListReturnsEmptyString() {
        String expectedResult = "";
        String actualResult = this.listToStringConverter.convert(new ArrayList<>());

        assertEquals(expectedResult, actualResult);
    }
}