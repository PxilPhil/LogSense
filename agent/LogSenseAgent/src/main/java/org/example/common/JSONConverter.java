package org.example.common;

import org.example.model.SessionComputerData;
import org.example.model.RunningData;

public interface JSONConverter {
    String convertSessionComputerDataToJson(SessionComputerData sessionComputerData);

    String convertRunningData(RunningData runningData);
}