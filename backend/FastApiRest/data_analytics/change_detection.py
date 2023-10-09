import numpy as np
import ruptures as rpt
from pandas import DataFrame

from model.data import Justification, JustificationData

penalty_value = 0.5  # value used for "penalizing" the pelting model for overfitting, decrease to detect more insignicant events and vice versa -> sensitivity in other words

"""
    Change detection works well for RAM but not for things like cpu
    -> penalty_value should be 0.5 to 1 depending on sensitivity
    -> indizes are subtracted by 1 because they appear to begin counting from 1, without it we get better results however?
    It highlights data points when large changes have occured (
    
    Solution for CPU:
    -> run pelting on it and sort out false positives
    -> use anomaly detection instead (current approach) and bucket if necessary
    
    Approach for finding meaningful events:
    Run pelting algorithm on the total pcdataframe to find change points
    Then fetch all available application data for the last few entries from change points to check if applications or processes were closed or opened
    Determine if a event is reasonable or not
    Keep in mind to check on time gaps as well
"""


def get_event_measurement_times(df: DataFrame,
                                column: str) -> list:
    # TODO: Perhaps move into manipulation?
    change_points = detect_events(df, column)
    change_points_measurement_times = df['measurement_time'].iloc[change_points].tolist()
    print(change_points_measurement_times)
    return change_points_measurement_times


def detect_events(df: DataFrame, column: str) -> list:  # should not be used for data with very high variance like cpu usage
    df_values = df[column].values  # Access values
    detector = rpt.Pelt(model="rbf").fit(df_values.reshape(-1, 1))  # Reshape data
    change_points = detector.predict(pen=penalty_value)  # data points where significant change was detected
    change_points = np.array(change_points) - 1
    return change_points
