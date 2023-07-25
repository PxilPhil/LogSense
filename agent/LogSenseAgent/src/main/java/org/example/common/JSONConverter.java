package org.example.common;

import org.example.model.InitialData;
import org.example.model.RunningData;

public interface JSONConverter {
    String convertInitialDataToJson(InitialData initialData);

    String convertRunningData(RunningData runningData);
}
