package org.example.converter;

import org.example.common.ListToStringConverter;
import org.example.monitor.Monitor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.stream.Collectors;

public class ListToStringSpacesConverter<T> implements ListToStringConverter<T> {
    private static final Logger LOGGER = LoggerFactory.getLogger(Monitor.class);

    @Override
    public String convert(List<T> list) {
        if (list != null) {
            return list.stream()
                    .map(n -> String.valueOf(n))
                    .collect(Collectors.joining(" "));
        } else {
            LOGGER.warn("Warning while converting a list to a string separated by spaces: the list is null. Therefore it can not be converted to a string.");
            return null;
        }
    }
}
