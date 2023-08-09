package org.example.common;

import java.util.List;

// JR: interface useful? / could it be made more generic?
public interface ListToStringConverter<T> {
    String convert(List<T> list);
}
