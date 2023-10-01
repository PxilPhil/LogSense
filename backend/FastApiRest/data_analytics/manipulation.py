from typing import List

import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta

from model.alerts import CustomAlert
from model.data import EventAnomalyJustifications

"""
    This module contains a lot of helper methods for specific cases in our application
"""


def group_by_timestamp(df):
    return df.groupby('timestamp')[
        ['majorFaults', 'contextSwitches', 'threadCount', 'openFiles', 'residentSetSize', 'cpuUsage',
         'processCountDifference']].sum(
        numeric_only=True).sort_values('timestamp', ascending=True)


def select_rows_by_application(selected_value, df):  # Method to select rows by value
    return df.loc[df.name == selected_value].groupby(['timestamp']).sum(numeric_only=True).sort_values(
        by=['timestamp'])


def group_by_name(df):
    return df.groupby(['name']).sum(numeric_only=True)


def calculate_moving_avg(df, column):  # calculates moving avg for the column
    df['MovingAvg'] = df[column].rolling(
        window=5).mean()  # moving averages can be used to flatten
    df = df.dropna()
    return df


def aggregate(df):
    return df.groupby("name").agg(list)


def create_df_between(start_timestamp, days, frequency):
    start_datetime = pd.to_datetime(start_timestamp, unit='ms')
    end_datetime = pd.to_datetime(calc_end_timestamp(start_timestamp, days), unit='ms')

    timestamp_index = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency)
    timestamp_values = timestamp_index.astype(np.int64) // 10 ** 6

    new_df = pd.DataFrame(index=timestamp_values)

    return new_df


def calc_end_timestamp(timestamp,
                       days):  # helper method to calculate the last timestamp going from a starting timestamp
    # and a time period
    time_delta = timedelta(days=days)
    end_date_time = datetime.fromtimestamp(timestamp / 1000) + time_delta
    end_timestamp = int(end_date_time.timestamp() * 1000)
    return end_timestamp

def determine_stability(cov): # maybe put this into a own module later on, used to convert COV to be easily readable by a user
    # TODO: keep in mind these are really abstract placeholder values
    if cov<5:
        return 'High Stability'
    elif cov<10:
        return 'Medium Stability'
    elif cov<20:
        return 'Low Stability'
    return 'Extremely Low Stability'

def convert_to_data_frame(csv_string):
    csv_io = io.StringIO(csv_string)
    df = pd.read_csv(csv_io, sep="|")
    return df


def convert_column_to_list(df, column):
    return df[column].tolist()


def add_justification_to_anomaly(anomaly_list: list, justification: EventAnomalyJustifications):
    for anomaly in anomaly_list:
        if anomaly.timestamp == justification.timestamp:
            anomaly.justification = justification


def get_justification_contained(timestamp: datetime, justification_list: list[EventAnomalyJustifications]):
    if justification_list is not None:
        for justification in justification_list:
            if timestamp == justification.timestamp:
                return justification
    return None

