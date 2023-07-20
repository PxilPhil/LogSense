package org.example.converter;

import org.example.common.ListToStringConverter;

import java.util.List;
import java.util.stream.Collectors;

public class ListToStringSpacesConverter<T> implements ListToStringConverter<T> {
    @Override
    public String convert(List<T> list) {
        if (list != null) {
            return list.stream()
                    .map(n -> String.valueOf(n))
                    .collect(Collectors.joining(" "));
        }
        return null;
    }
}
