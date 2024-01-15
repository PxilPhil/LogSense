from typing import List

import pandas as pd
import warnings

from pandas import DataFrame

from data_analytics import manipulation, stats
from data_analytics.alerts import check_for_custom_alerts
from data_analytics.change_anomaly_detection import get_event_measurement_times, detect_events, detect_anomalies
from data_analytics.forecasting import fit_linear_regression, predict_for_df
from data_analytics.justification import justify_pc_data_points, justify_application_df
from data_analytics.stats import calculate_trend_statistics, create_statistics_message, append_statistics_message
from data_analytics.trend_analysis import determine_event_ranges
from db_access.pc import get_ram_time_series_limited
from model.alerts import CustomAlert, AlertNotification
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")


# todo: our current approach doing on request is pretty stupid, please change it

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


def forecast_disk_space(df, column, start, end, bucket_value):
    """
    Forecasts disk space allocation between a start and end date with a bucket_value.

    Args:
        prediction_df (DataFrame): The DataFrame containing free disk space values.
        column (str): The column in the DataFrame to be used for forecasting.
        start (str): The start date in the format 'YYYY-MM-DD HH:MM:SS'.
        end (str): The end date in the format 'YYYY-MM-DD HH:MM:SS'.
        bucket_value (str): The frequency for prediction (e.g., '1Min' for 1 minute, '5Min' for 5 minutes).

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """
    #todo: change point detection?

    # Convert start and end dates to datetime objects
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # Create a DataFrame with the specified frequency (bucket_value) between start and end dates
    date_range = pd.date_range(start=start_date, end=end_date, freq=bucket_value)
    prediction_df = pd.DataFrame({'datetime': date_range})
    prediction_df['measurement_time'] = prediction_df['datetime'].astype('int64') // 10 ** 6

    # Fit the linear regression model using the existing data
    LR = fit_linear_regression(df, column)

    # Predict values for the created DataFrame
    prediction_df = predict_for_df(LR, prediction_df, column)

    data_list = []
    for _, row in prediction_df.iterrows():
        data_list.append(ForecastData(**row.to_dict()))

    last_timestamp = None  # timestamp when free disk space reaches zero or below
    # Find out if and when Linear Regression is less than or equal to 0 (free disk space running out)
    no_disk_space_rows = prediction_df[prediction_df[column] <= 0]
    if not no_disk_space_rows.empty:
        last_timestamp = no_disk_space_rows['datetime'].iloc[0]

    return data_list, last_timestamp


def determine_full_disk_space(df: DataFrame, column: str, max_days):
    """
    Forecasts disk space allocation for a certain number of days.

    Features:
    - Training a linear regression model by existing disk space data.
    - Building a new DataFrame to be filled with data by the linear regression model later on.
    - Filling the DataFrame with prediction values.
    - Finding out when free disk space will run out and save the timestamp into "last_timestamp".

    Args:
        df (DataFrame): The DataFrame containing free disk space values.
        max_days (int): The number of days data should be forecasted for.

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """

    last_timestamp = None  # timestamp when free disk space reaches zero or below
    total_days = 0
    current_days = 10
    data_list = []

    # read dataframe, elect only needed columns
    events = detect_events(df, column, 10)

    df = df.drop(index=df.index[df.index >= events[len(events)-1]])
    df = df.filter(['measurement_time', column])
    df = df.set_index(pd.to_datetime(df['measurement_time']).astype('int64') // 10 ** 6)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df, column)

    while last_timestamp is None and total_days < max_days:
        prediction_df = manipulation.create_df_between(timestamp, current_days, 'D')
        prediction_df = predict_for_df(LR, prediction_df)

        # convert timestamps to datetime
        prediction_df['datetime'] = pd.to_datetime(prediction_df.index, unit='ms')
        # find out if and when LinearRegression is less than 0 (free disk space running out)
        no_disk_space_rows = prediction_df[prediction_df['LinearRegression'] <= 0]
        total_days = total_days + current_days

        for _, row in prediction_df.iterrows():
            data_list.append(ForecastData(**row.to_dict()))

        if not no_disk_space_rows.empty:
            last_timestamp = no_disk_space_rows['datetime'].iloc[0]
        else:
            timestamp = int((pd.Timestamp(prediction_df['datetime'].iloc[-1]) + pd.DateOffset(days=1)).timestamp() * 1000)

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
    # in order to prevent underfitting, we need to fetch more data if we have too little

    # detect changes or events
    ram_change_points = get_event_measurement_times(df, df,
                                                    'ram', 3)  # only do it for ram since it makes no sense to do it for cpu

    # find anomalies
    anomalies_ram = detect_anomalies(df, df, 'ram')
    anomalies_cpu = detect_anomalies(df, df, 'cpu')

    # get justifications for events and anomalies
    ram_anomaly_justifications = justify_application_df(df, anomalies_ram, application_name, None, True)
    ram_event_justifications = justify_application_df(df, ram_change_points, application_name, ram_anomaly_justifications,False)
    ram_events_and_anomalies = ram_anomaly_justifications + ram_event_justifications

    cpu_events_and_anomalies = justify_application_df(df, anomalies_cpu, application_name, None,
                                                      False)

    # get stats
    statistic_data_ram = calculate_trend_statistics(df, 'ram', 'RAM')
    statistic_data_ram.message = append_statistics_message(statistic_data_ram.message, len(ram_change_points), len(anomalies_ram), len(df))
    statistic_data_cpu = calculate_trend_statistics(df, 'cpu', 'CPU')
    statistic_data_cpu.message = append_statistics_message(statistic_data_cpu.message, len(anomalies_cpu), len(anomalies_cpu), len(df))

    # determine event anomaly ranges and save statistics of them in justifications
    determine_event_ranges(df, ram_events_and_anomalies, 'ram')
    determine_event_ranges(df, cpu_events_and_anomalies, 'cpu')

    return df, ram_events_and_anomalies, cpu_events_and_anomalies, statistic_data_ram, statistic_data_cpu


def analyze_pc_data(pc_id: int, df, pc_total_df, name: str):
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
        :param pc_id:

    """
    if name == 'ram':
        latest_total_ram = pc_total_df.at[pc_total_df.index.max(), 'value']
        allocation_map = stats.calc_allocation(latest_total_ram, name, df)
        allocation_list = [AllocationClass(name=key, allocation=value) for key, value in
                           allocation_map.items()]  # convert map into list of our model object to send via json
    elif name == 'cpu':  # get allocation percentage for cpu, no calculation needed
        allocation_list = []
        for index, row in df.iterrows():
            allocation_instance = AllocationClass(name=row['name'], allocation=row[name])
            allocation_list.append(allocation_instance)

    # sort allocations by impact
    allocation_list = sorted(allocation_list, key=lambda ram: ram.allocation, reverse=True)

    anomaly_measurements = []
    change_points = []
    training_df = pc_total_df  # dataframe used to train the models

    # fetch more data if needed to avoid underfittng
    if len(df.index) < 50:  # arbitrary value used
        training_df, extended_list = get_ram_time_series_limited(pc_id, 100)

    # detect anomalies
    anomaly_measurements = detect_anomalies(pc_total_df, training_df, 'value')

    # detect changes / events
    change_points = get_event_measurement_times(pc_total_df, training_df, 'value', 3)

    print('----------------------------------------')
    print(anomaly_measurements)
    print(change_points)


    # justifies events and anomalies
    anomalies = justify_pc_data_points(pc_total_df, anomaly_measurements, None, 1, True)
    events = justify_pc_data_points(pc_total_df, change_points, anomalies, 1, False)
    events_and_anomalies = anomalies+events



    # get stats
    statistic_data = calculate_trend_statistics(pc_total_df, 'value', name)
    statistic_data.message = append_statistics_message(statistic_data.message, len(change_points), len(anomaly_measurements), len(pc_total_df))

    determine_event_ranges(pc_total_df, events_and_anomalies, 'value')

    return pc_total_df, allocation_list, events_and_anomalies, statistic_data


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
