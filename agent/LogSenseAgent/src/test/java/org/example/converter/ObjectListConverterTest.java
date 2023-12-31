package org.example.converter;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class ObjectListConverterTest {
    private ObjectListConverter<Integer> objectListConverter;

    @BeforeEach
    void setUp() {
        this.objectListConverter = new ObjectListConverter();
    }

    @Test
    void convertObjectListCorrectly() {
        List<Object> objectList = new ArrayList<>();
        objectList.add(15);
        objectList.add(2);
        objectList.add(129);

        List<Integer> expectedIntegerList = new ArrayList<>();
        expectedIntegerList.add(15);
        expectedIntegerList.add(2);
        expectedIntegerList.add(129);

        List<Integer> actualIntegerList = this.objectListConverter.convertObjectList(objectList, Integer.class);

        assertEquals(expectedIntegerList, actualIntegerList);
    }

    @Test
    void convertObjectListWithNullObjectListReturnsNull() {
        List<Integer> integerList = this.objectListConverter.convertObjectList(null, Integer.class);

        assertNull(integerList);
    }

    @Test
    void convertObjectListWithNullTargetTypeReturnsNull() {
        List<Object> objectList = new ArrayList<>();
        objectList.add(15);
        objectList.add(2);
        objectList.add(129);

        List<Integer> integerList = this.objectListConverter.convertObjectList(objectList, null);

        assertNull(integerList);
    }

    @Test
    void convertObjectListWithDifferentDataTypesInListReturnsListWithNullValues() {
        List<Object> objectList = new ArrayList<>();
        objectList.add(12);
        objectList.add("Test");
        objectList.add(2419);
        objectList.add(true);

        List<Integer> expectedIntegerList = new ArrayList<>();
        expectedIntegerList.add(12);
        expectedIntegerList.add(null);
        expectedIntegerList.add(2419);
        expectedIntegerList.add(null);

        List<Integer> actualIntegerList = this.objectListConverter.convertObjectList(objectList, Integer.class);

        assertEquals(expectedIntegerList, actualIntegerList);
    }

    @Test
    void convertObjectListWithEmptyObjectListReturnsEmptyList() {
        List<Integer> expectedIntegerList = new ArrayList<>();
        List<Integer> actualIntegerList = this.objectListConverter.convertObjectList(new ArrayList<>(), Integer.class);

        assertEquals(expectedIntegerList, actualIntegerList);
    }
}