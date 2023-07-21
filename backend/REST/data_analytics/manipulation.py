import pandas as pd
import numpy as np


def group_by_timestamp(df):
    return df.groupby(['timestamp']).sum(numeric_only=True).sort_values('timestamp', ascending=True)


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


def create_df_between(start_timestamp, end_timestamp, frequency):
    start_datetime = pd.to_datetime(start_timestamp, unit='ms')
    end_datetime = pd.to_datetime(end_timestamp, unit='ms')

    timestamp_index = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency)
    timestamp_values = timestamp_index.astype(np.int64) // 10 ** 6

    new_df = pd.DataFrame(index=timestamp_values)

    return new_df

