import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta

def group_by_timestamp(df):
    return df.groupby('timestamp')[
        ['majorFaults', 'contextSwitches', 'threadCount', 'openFiles', 'residentSetSize', 'cpuUsage']].sum(
        numeric_only=True).sort_values('timestamp', ascending=True)


def select_rows_by_application(selected_value, df):  # Method to select rows by value
    return df.loc[df.name == selected_value].groupby(['timestamp']).sum(numeric_only=True).sort_values(
        by=['timestamp'])


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



def convert_to_data_frame(csv_string):
    csv_io = io.StringIO(csv_string)
    df = pd.read_csv(csv_io, sep="|")
    return df
