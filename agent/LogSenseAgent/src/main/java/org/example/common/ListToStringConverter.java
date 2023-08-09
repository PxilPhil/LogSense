package org.example.common;

import java.util.List;

public interface ListToStringConverter<T> {
    String convert(List<T> list);
}
