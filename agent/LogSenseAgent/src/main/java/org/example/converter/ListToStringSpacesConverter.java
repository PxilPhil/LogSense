package org.example.converter;

import java.util.List;
import java.util.stream.Collectors;

import static java.util.Objects.requireNonNull;

public class ListToStringSpacesConverter<T> {
    public String convert(List<T> list) {
        requireNonNull(list);
        return list.stream()
                .map(String::valueOf)
                .collect(Collectors.joining(" "));
    }
}
