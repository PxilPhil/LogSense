from typing import List

import pandas as pd
import warnings

from pandas import DataFrame

from data_analytics import manipulation, stats
from data_analytics.alerts import check_for_custom_alerts
from data_analytics.change_anomaly_detection import get_event_measurement_times, detect_events, detect_anomalies
from data_analytics.forecasting import fit_linear_regression, predict_for_df
from data_analytics.justification import justify_pc_data_points, justify_application_df
from data_analytics.manipulation import determine_stability
from data_analytics.stats import calculate_trend_statistics
from data_analytics.trend_analysis import determine_event_ranges
from model.alerts import CustomAlert, AlertNotification
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")

def preprocess_pc_data(df: DataFrame):
    """
    Preprocesses and groups data before inserting it into the database.

    Features:
        - Grouping the DataFrame by timestamp to create the total pc DataFrame.

    Args:
        df (DataFrame): The DataFrame containing pc data to be inserted.

    Returns:
        pc_total_df: The total pc DataFrame grouped by timestamp.
        event_list: A list of detected events.
    """
    df = df.set_index('timestamp')
    event_list = []
    pc_total_df = manipulation.group_by_timestamp(df)
    return pc_total_df, event_list


def forecast_disk_space(df: DataFrame, column: str, days):
    """
    Forecasts disk space allocation for a certain number of days.

    Features:
    - Training a linear regression model by existing disk space data.
    - Building a new DataFrame to be filled with data by the linear regression model later on.
    - Filling the DataFrame with prediction values.
    - Finding out when free disk space will run out and save the timestamp into "last_timestamp".

    Args:
        df (DataFrame): The DataFrame containing free disk space values.
        days (int): The number of days data should be forecasted for.

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """
    # read dataframe, elect only needed columns
    df = df.filter(['measurement_time', column])
    df = df.set_index(pd.to_datetime(df['measurement_time']).astype('int64') // 10 ** 6)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df, column)
    df = manipulation.create_df_between(timestamp, days, 'D')
    df = predict_for_df(LR, df)

    # convert timestamps to datetime
    df['datetime'] = pd.to_datetime(df.index, unit='ms')
    data_list = []
    for _, row in df.iterrows():
        data_list.append(ForecastData(**row.to_dict()))
    last_timestamp = None  # timestamp when free disk space reaches zero or below
    # find out if and when LinearRegression is less than 0 (free disk space running out)
    no_disk_space_rows = df[df['LinearRegression'] <= 0]
    if not no_disk_space_rows.empty:
        last_timestamp = no_disk_space_rows['datetime'].iloc[0]

    return data_list, last_timestamp


def analyze_application_data(df, application_name):
    """
    Analyzes application data fetched by a client.

    Features:
        - Anomaly detection.
        - Change point detection
        - Simple statistical math (standard deviation, mean, median).
        - Calculate stability and trend statistics
        - Justifications for why changes or anomalies have occurred


    Args:
        df (DataFrame): The DataFrame containing application data.
        application_name (str): The name of the application.

    Returns:
        df: The DataFrame containing application data.
        ram_events_and_anomalies: The list of detected change points and anomalies for ram
        cpu_events_and_anomalies: The list of detected change points and anomalies for cpu
        statistic_data: Simple statistical data like mean, average, median, trend stats
    """
    # detect changes or events
    ram_change_points = get_event_measurement_times(df, 'ram')

    # find anomalies
    anomalies_ram = detect_anomalies(df, 'ram')
    anomalies_cpu = detect_anomalies(df, 'cpu')

    # get justifications for events and anomalies
    ram_anomaly_justifications = justify_application_df(df, anomalies_ram, application_name, None, True)
    ram_events_and_anomalies = justify_application_df(df, ram_change_points, application_name,
                                                      ram_anomaly_justifications,
                                                      False)
    cpu_events_and_anomalies = justify_application_df(df, anomalies_cpu, application_name, None,
                                                      False)

    # get stats
    statistic_data = calculate_trend_statistics(df)

    # look at data ranges
    determine_event_ranges(df, ram_change_points)

    return df, ram_events_and_anomalies, cpu_events_and_anomalies, statistic_data


def analyze_pc_data(df, pc_total_df):
    """
    Analyzes pc data, called by the client when fetching pc data of a certain category (like RAM).

    Features:
        - Anomaly detection.
        - Application allocation calculation
        - Change point detection
        - Simple statistical math (standard deviation, mean, median).
        - Calculate stability and trend statistics
        - Justifications for why changes or anomalies have occurred


    Args:
        df (DataFrame): The DataFrame containing application data.
        pc_total_df (DataFrame): The DataFrame containing total pc data.
        column (str): Column which should be analyzed like RAM (deprecated).

    Returns:
        pc_total_df: The DataFrame containing total pc data.
        anomaly_list: The list of detected anomalies
        allocation_list: The list of allocations (which application makes up how much percent of RAM/CPU usage).
        std: Standard deviation from mean, used for calculating "Stability".
        mean: Average of the values.
    """
    # get allocation percentage for ram
    latest_total_ram = pc_total_df.at[pc_total_df.index.max(), 'ram']
    allocation_map_ram = stats.calc_allocation(latest_total_ram, 'ram', df)
    allocation_list_ram = [AllocationClass(name=key, allocation=value) for key, value in
                           allocation_map_ram.items()]  # convert map into list of our model object to send via json

    # get allocation percentage for cpu, no calculation needed
    allocation_list_cpu = []
    for index, row in df.iterrows():
        allocation_instance = AllocationClass(name=row['name'], allocation=row['cpu'])
        allocation_list_cpu.append(allocation_instance)

    # sort allocations by impact
    allocation_list_cpu = sorted(allocation_list_cpu, key=lambda cpu: cpu.allocation, reverse=True)
    allocation_list_ram = sorted(allocation_list_ram, key=lambda ram: ram.allocation, reverse=True)

    # detect anomalies
    anomaly_measurements_ram = detect_anomalies(pc_total_df, 'ram')
    anomaly_measurements_cpu = detect_anomalies(pc_total_df, 'cpu')

    # detect changes / events
    ram_change_points = get_event_measurement_times(pc_total_df, 'ram')
    cpu_change_points = get_event_measurement_times(df, 'cpu')

    # justifies events and anomalies
    ram_anomalies = justify_pc_data_points(pc_total_df, anomaly_measurements_ram, None, 1, True)
    ram_anomaly_events = justify_pc_data_points(pc_total_df, ram_change_points, ram_anomalies, 1, False)

    cpu_anomalies = justify_pc_data_points(pc_total_df, anomaly_measurements_cpu,
                                           ram_anomaly_events, 1, True)
    cpu_anomaly_events = justify_pc_data_points(pc_total_df, cpu_change_points,
                                                ram_anomaly_events + cpu_anomalies, 1, False)

    # get stats
    statistic_data = calculate_trend_statistics(pc_total_df)

    return pc_total_df, allocation_list_ram, allocation_list_cpu, ram_anomaly_events, cpu_anomaly_events, statistic_data


def analyze_trends():
    """
    Analyzes application & pc trends, in order for that it groups data sets by date intervals
    :return:
    """


def check_for_alerts(user_id: int, custom_alert_list: List[CustomAlert], pc_df: DataFrame, start, end) -> List[
    AlertNotification]:
    """
    Checks for alerts that have appeared in a specified timeframe
    :return:
    """

    # first check for custom alerts
    alert_notifications = check_for_custom_alerts(user_id, pc_df, custom_alert_list, start, end)
    # check multiple complex, standard alerts

    return alert_notifications
