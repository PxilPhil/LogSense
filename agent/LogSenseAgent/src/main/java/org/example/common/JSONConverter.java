package org.example.common;

import org.example.model.RunningData;
import org.example.model.SessionComputerData;

public interface JSONConverter {
    String convertSessionComputerDataToJson(SessionComputerData sessionComputerData);

    String convertRunningData(RunningData runningData);
}
