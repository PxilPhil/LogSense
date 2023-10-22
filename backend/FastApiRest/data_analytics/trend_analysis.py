"""
This module is supposed to perform trend analysis operations
Features:
Calculating rise/fall of cpu & ram usage for a timeframe
Looking at the data between events to create anomaly ranges
"""
from pandas import DataFrame

from data_analytics.stats import calculate_trend_statistics
from model.data import StatisticData


def determine_event_ranges(df: DataFrame, timestamps: list):
    """
    This algorithm looks at the ranges between events & anomalies to determine anomalous data ranges (to be implemented)
    :return:
    """
    last_timestamp = None
    range_stats: list[StatisticData] = []
    for timestamp in timestamps:
        if last_timestamp:
            selected_rows = df[(df['measurement_time'] >= last_timestamp) & (df['measurement_time'] <= timestamp)]
            print(f"{last_timestamp}+{timestamp}")
            range_stats.append(calculate_trend_statistics(selected_rows))
        last_timestamp = timestamp
    print(range_stats)
    return range_stats


def application_change_detection():
    """
    This algorithm looks at changes & differences between applications
    :return:
    """
