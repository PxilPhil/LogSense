import numpy as np
import pandas as pd
import humanize
from _decimal import Decimal, ROUND_HALF_UP
from pandas import DataFrame

from data_analytics.util.change_anomaly_detection import detect_events
from model.data import StatisticData, Justification


def calc_allocation(latest_total_value, column, df):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    for index, row in df.iterrows():
        allocation_map[row['name']] = row[column] / latest_total_value
    return allocation_map


def calculate_trend_statistics(df: DataFrame, column: str, name: str) -> StatisticData:
    """
    Calculates statistics for the trend of a graph like:
    Median
    Average
    Standard Deviation
    Coefficient of Variation => Stability

    :return:
    """

    # calculate the stability of data
    std = df[column].std()
    mean = df[column].mean()
    cov = (std / mean) * 100  # stands for coefficient_of_variation

    # calculate changes that occurred from start to end
    recent_row = df.loc[df['measurement_time'].idxmax()]
    oldest_row = df.loc[df['measurement_time'].idxmin()]
    change = ((recent_row[column] - oldest_row[column]) / oldest_row[column]) * 100
    delta = recent_row[column] - oldest_row[column]

    stability = f"Stability: {determine_stability(cov)}\n"
    message = create_statistics_message(change, delta, name)

    if name.lower() == 'ram':
        average_gb = round(mean / (1024 ** 3), 2)
        current_gb = round(recent_row[column] / (1024 ** 3), 2)
    else: # in the case of cpu
        average_gb = round(mean, 2)*100
        current_gb = "{:.2f}".format(round(recent_row[column], 2) * 100)

    statistic_data = StatisticData(
        average=average_gb,
        current=current_gb,
        stability=stability,
        message=message
    )
    return statistic_data


def create_statistics_message(change, delta, name: str):
    delta_mb = convert_bytes_to_mb(delta)
    if abs(delta_mb) >= 1000:
        delta = convert_mb_to_gb(delta_mb)
        delta = Decimal(delta).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        delta = Decimal(delta_mb).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if name == 'ram':
        message = f"{name.upper()} Usage has changed by {round(change, 2)}% ({delta} GB) \n"
    else:
        message = f"{name.upper()} Usage has changed by {round(change, 2)}% ({delta} MB) \n"
    return message

def convert_mb_to_gb(size):
        return size / 1024
def convert_bytes_to_mb(size):
        return size / (1024 * 1024)  # convert bytes to mb

def append_statistics_message(message, event_amount, anomaly_amount, data_amount):
    message += f"{event_amount} Events detected \n {anomaly_amount} Anomalies detected \n"
    message += f"{data_amount} Datapoints fetched \n"
    return message


def determine_stability(cov):  # common rule of thumb is that cv < 15% is considered stable and < 30% medium
    if cov < 15:
        return 'High'
    elif cov < 30:
        return 'Medium'
    return 'Low'


def determine_event_ranges(df: DataFrame, anomalies_events: list[Justification], column: str):
    """
    This algorithm looks at the ranges between events & anomalies to determine anomalous data ranges (to be
    implemented) and provide statistics for them
    :return:
    """
    last_timestamp = None
    for anomaly_event in anomalies_events:
        if last_timestamp:
            selected_rows = df[
                (df['measurement_time'] >= last_timestamp) & (df['measurement_time'] <= anomaly_event.timestamp)]
            print(f"{last_timestamp}+{anomaly_event.timestamp}")
            if not selected_rows.empty:
                anomaly_event.statistics = calculate_trend_statistics(selected_rows, column, column)
        last_timestamp = anomaly_event.timestamp


def determine_linear_direction(df, column_name, tolerance):
    """
    Determines whether or not values are linearly rising or falling via linear regression and then checking the mean squared error
    :param df:
    :param column_name:
    :param tolerance:
    :return:
    """
    events = detect_events(df, column_name, 5)
    current_df = df.drop(
        index=df.index[df.index <= events[len(events) - 1]])  # only work with latest course (last change point)
    print('determine_linear_direction')
    print(current_df)

    # todo: change point detection algorithm always marks the last one as being an event which leads to probems
    if (len(current_df) > 0):
        column_values = current_df[column_name]

        if isinstance(column_values, pd.Series):
            column_values = column_values.values

        indices = np.arange(len(column_values))
        slope, intercept = np.polyfit(indices, column_values, 1)
        predicted_values = slope * indices + intercept
        mse = np.mean((column_values - predicted_values) ** 2)
        print(mse)
        print(tolerance)
        if mse < tolerance:
            if slope > 0:
                print('detected')
                return 1
            else:
                print('detected')
                return -1
    # only for testing
    """
    num_rows = 20
    start_value = 1000000
    increment = 250000

    linear_values = [start_value + i * increment for i in range(num_rows)]

    # Create a dataframe with the 'ram' column
    df = pd.DataFrame({column_name: linear_values})
    print(df)
    """
    return 0
