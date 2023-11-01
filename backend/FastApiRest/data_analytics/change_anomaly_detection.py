import numpy as np
import ruptures as rpt
from pandas import DataFrame
from sklearn.ensemble import IsolationForest

from model.data import Justification

penalty_value = 0.5  # value used for "penalizing" the pelting model for overfitting, decrease to detect more insignicant events and vice versa -> sensitivity in other words

"""
    Change point detection done via pelting algorithm with a penalty value between 0.5 and 1
    Anomaly detection done via Isolation Forest with a contamination of 0.1 (atleast for appliications)
"""


def get_event_measurement_times(predicted_df: DataFrame, training_df: DataFrame,
                                column: str) -> list:
    change_points = detect_events(training_df, column)

    change_points = training_df['measurement_time'].iloc[change_points].tolist()

    change_points_measurement_times = [change_point for change_point in change_points if
                                       change_point in predicted_df['measurement_time'].values]
    return change_points_measurement_times


def detect_events(df: DataFrame, column: str) -> list:  # should not be used for data with very high variance like cpu usage
    df_values = df[column].values.reshape(-1, 1)
    detector = rpt.Pelt(model="rbf").fit(df_values)
    change_points = detector.predict(pen=penalty_value)  # data points where significant change was detected
    change_points = np.array(change_points) - 1

    return change_points


def detect_anomalies(predicted_df: DataFrame, training_df: DataFrame, column: str):
    # unsure if we really need to split in training and prediction data
    df_training_values = training_df[column].values.reshape(-1, 1)
    df_prediction_values = predicted_df[column].values.reshape(-1, 1)
    clf = IsolationForest(contamination=0.1, random_state=None)
    clf.fit(df_training_values)
    predicted_labels = clf.predict(df_prediction_values)
    anomaly_indices = np.where(predicted_labels == -1)[0]
    anomaly_measurement_times = predicted_df['measurement_time'].iloc[anomaly_indices].tolist()
    return anomaly_measurement_times
