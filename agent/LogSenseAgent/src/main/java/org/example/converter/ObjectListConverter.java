package org.example.converter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class ObjectListConverter<T> {
    private static final Logger LOGGER = LoggerFactory.getLogger(ObjectListConverter.class);

    public List<T> convertObjectList(List<Object> objectList, Class<T> targetType) {
        if (objectList != null && targetType != null) {
            List<T> list = new ArrayList<>();
            for (Object object : objectList) {
                if (targetType.isInstance(object)) {
                    list.add(targetType.cast(object));
                } else {
                    list.add(null);
                }
            }
            return list;
        } else {
            LOGGER.warn("Warning while converting a list of objects to a list of another type: either the list of objects or the target type is null. Therefore the list of objects can not be converted to a list of another type.");
            return null;
        }
    }
}
