package org.example.converter;

import java.util.ArrayList;
import java.util.List;

public class ObjectListConverter<T> {
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
        }
        return null;
    }
}
