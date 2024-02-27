import numpy as np
import ruptures as rpt
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

from model.data import Justification

"""
    Change point detection done via pelting algorithm with a penalty value between 0.5 and 1
    Anomaly detection done via Isolation Forest with a contamination of 0.1 (atleast for appliications)
    
    Documentation for cpu overall worked best: penalty of 3 contamination of 0.03
    Documentation for rest overall worked best: penalty of 2? contamination of 0.03

"""


def get_event_measurement_times(predicted_df: DataFrame, training_df: DataFrame,
                                column: str, penalty: int) -> list:
    if not training_df.empty and len(training_df) >= 50:
        change_points = detect_events(training_df, column, penalty)
        if not change_points:
            return []

        change_points = training_df['measurement_time'].iloc[change_points].tolist()

        change_points_measurement_times = [change_point for change_point in change_points if
                                           change_point in predicted_df['measurement_time'].values]
        return change_points_measurement_times
    return []

def detect_events(df: DataFrame, column: str, penalty: int) -> list:
    # Penalty value used for "penalizing" the pelt model for overfitting.

    df_values = df[column].values.reshape(-1, 1)
    detector = rpt.Pelt(model="rbf").fit(df_values)
    change_points = detector.predict(pen=penalty)  # Data points where significant change was detected

    change_points = [cp - 1 for cp in change_points if
                     cp > 0]  # move position by one because the algorithm moves them back by one index

    if len(change_points) > 0 and change_points[-1] == len(
            df_values) - 1:  # algorithm always detects last point as change point, remove because of that
        change_points = change_points[:-1]

    # Event set to first index if none contained
    if not change_points:
        return [0]

    return change_points


def detect_anomalies(predicted_df: DataFrame, training_df: DataFrame, column: str, contamination_rate: float = 0.03):
    # Extract values from the data
    df_training_values = training_df[column].values.reshape(-1, 1)
    df_prediction_values = predicted_df[column].values.reshape(-1, 1)

    # Model training and prediction
    clf = IsolationForest(contamination=contamination_rate, random_state=42)
    clf.fit(df_training_values)
    predicted_labels = clf.predict(df_prediction_values)

    # Extract measurement times when anomalies occur
    anomaly_indices = np.where(predicted_labels == -1)[0]
    anomaly_measurement_times = predicted_df['measurement_time'].iloc[anomaly_indices].tolist()

    return anomaly_measurement_times
