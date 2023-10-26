"""
This module is supposed to perform trend analysis operations
Features:
Calculating rise/fall of cpu & ram usage for a timeframe
Looking at the data between events to create anomaly ranges
"""
from pandas import DataFrame

from data_analytics.stats import calculate_trend_statistics
from model.data import StatisticData, Justification


def determine_event_ranges(df: DataFrame, anomalies_events: list[Justification], column: str):
    """
    This algorithm looks at the ranges between events & anomalies to determine anomalous data ranges (to be
    implemented) and provide statistics for them
    :return:
    """
    last_timestamp = None
    for anomaly_event in anomalies_events:
        if last_timestamp:
            selected_rows = df[(df['measurement_time'] >= last_timestamp) & (df['measurement_time'] <= anomaly_event.timestamp)]
            print(f"{last_timestamp}+{anomaly_event.timestamp}")
            if not selected_rows.empty:
                anomaly_event.statistics = calculate_trend_statistics(selected_rows, column)
        last_timestamp = anomaly_event.timestamp

def application_change_detection():
    """
    This algorithm looks at changes & differences between applications
    :return:
    """
