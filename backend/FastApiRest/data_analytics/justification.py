from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pandas import DataFrame

from data_analytics.manipulation import get_justification_contained
from db_access.application import get_relevant_application_data, get_application_between
from db_access.pc import get_pc_data_at_measurement
from model.data import Justification

ram_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant
cpu_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant


class ApplicationStat:  # class to store application data
    def __init__(self, ram: int, cpu: int, process_change: int):
        self.ram = ram
        self.cpu = cpu
        self.process_change = process_change  # same as event_headers (processes in applications were closed or opened marked with -1, 0 or 1)


def perform_justification_processing(df: DataFrame):
    """
    Function to perform data manipulation and processing required for making justifications
    :return:
    """
    # get the most important applications
    important_applications = df.loc[df.groupby('name')['measurement_time'].idxmax()]

    # find out process changes in applications
    summary_df = df.groupby('name')['process_count_difference'].sum().reset_index()

    # find out which applications were started or stopped
    grouped = df.groupby('measurement_time')['name'].unique().reset_index()
    grouped = grouped.sort_values(by='measurement_time')
    first_names = set(grouped['name'].iloc[0])
    grouped['added'] = grouped['name'].apply(lambda x: list(set(x) - first_names))
    grouped['removed'] = grouped['name'].apply(lambda x: list(first_names - set(x)))

    # put the data into array of string to make working with them easier
    started = [name for name in np.concatenate(grouped['added']) if not pd.isna(name)]
    stopped = [name for name in np.concatenate(grouped['removed']) if not pd.isna(name)]

    return important_applications, summary_df, started, stopped


def justify_pc_data_points(pc_total_df, significant_data_points: list, prior_justifications: list[Justification],
                           pc_id: int, should_tag_as_anomaly: bool) -> list[Justification]:
    """
    Function to loop through event list to call gather_event_logs()

    How event log detection works:
    On init, make a map of applications, if any applications are added/removed later it will be registered
    :return:
    """
    justification_logs = []

    for point in significant_data_points:
        existing_justification = get_justification_contained(point, prior_justifications)
        if existing_justification:
            justification_logs.append(existing_justification)
        else:
            ram_relevancy = get_pc_data_at_measurement(ram_relevancy_threshold, point, pc_id)
            applications_df, application_data_list = get_relevant_application_data(pc_id, point, ram_relevancy,
                                                                                   cpu_relevancy_threshold)
            pc_just_started = False

            if applications_df['measurement_time'].nunique() <= 1:
                pc_just_started = True

            till_timestamp = applications_df['measurement_time'].min()

            important_applications, summary_df, started, stopped = perform_justification_processing(applications_df)
            message = create_justification_message(pc_just_started, None, None, important_applications, summary_df,
                                                   started, stopped)

            justification = Justification(
                timestamp=point,
                till_timestamp=till_timestamp,
                is_anomaly=should_tag_as_anomaly,
                justification_message=message,
                statistics=None
            )

            justification_logs.append(justification)
    return justification_logs


def justify_application_data_points(data_points: list, name: str, pc_id: int) -> list[
    Justification]:
    """
    Method to justify application data points without the application dataframe, mainly used for alerts
    :param data_points:
    :param name:
    :return:
    """
    justifications: list[Justification] = []
    for point in data_points:
        start_point: datetime = point - timedelta(minutes=5)
        application_df, application_data_list = get_application_between(pc_id, name, start_point, point)
        # check application for justifications
        total_delta_ram, total_delta_cpu = calc_deltas(application_df, point)

        important_applications, summary_df, started, stopped = perform_justification_processing(application_df)

        justification_message = create_justification_message(False, total_delta_ram, total_delta_cpu,
                                                             important_applications, summary_df, started, stopped)
        justification = Justification(
            timestamp=point,
            till_timestamp=start_point,
            is_anomaly=False,
            justification_message=justification_message,
            statistics=None
        )

        justifications.append(justification)
    return justifications


def justify_application_df(df: DataFrame, data_points: list, name: str,
                           prior_justifications: list[Justification], should_tag_as_anomaly: bool) -> list[
    Justification]:
    # this method shares a lot of similarities with justify_data_point but it's meant only for one singular application
    justification_logs = []
    for point in data_points:
        till_timestamp_point = point - timedelta(minutes=5)

        existing_justification = get_justification_contained(point, prior_justifications)
        if existing_justification:
            justification_logs.append(existing_justification)
        else:
            # select all rows in the specified time window
            time_window_rows = df[
                (df['measurement_time'] >= till_timestamp_point) & (df['measurement_time'] <= point)]
            total_delta_ram = time_window_rows.iloc[-1]['ram'] - time_window_rows.iloc[0]['ram']
            total_delta_cpu = time_window_rows.iloc[-1]['cpu'] - time_window_rows.iloc[0]['cpu']

            # check application for justifications
            important_applications, summary_df, started, stopped = perform_justification_processing(time_window_rows)

            justification_message = create_justification_message(False, total_delta_ram, total_delta_cpu,
                                                                 important_applications, summary_df, started, stopped)

            event_anomaly = Justification(
                timestamp=point,
                till_timestamp=till_timestamp_point,
                is_anomaly=should_tag_as_anomaly,
                justification_message=justification_message,
                statistics=None
            )
            justification_logs.append(event_anomaly)

    return justification_logs


def calc_deltas(df: DataFrame, point: datetime):
    if df is not None:
        total_ram = df.loc[df['measurement_time'] == point, 'ram'].iloc[0]
        total_cpu = df.loc[df['measurement_time'] == point, 'cpu'].iloc[0]

        total_delta_ram = total_ram - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'ram'].iloc[0]
        total_delta_cpu = total_cpu - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'cpu'].iloc[0]
        return np.int64(total_delta_ram).item(), np.int64(total_delta_cpu).item()


def format_application_info(row):
    return f"Name: {row['name']}, RAM: {row['ram']}, CPU: {row['cpu']}\n"


def create_justification_message(pc_just_started: bool, total_delta_ram, total_delta_cpu, important_applications,
                                 summary_df, started, stopped) -> str:
    message = "-General Information-\n"

    # build initial part
    if pc_just_started:
        message = "PC just started\n"
    if total_delta_ram:
        message += f"Total Delta of RAM is {total_delta_ram}\n"
    if total_delta_cpu:
        message += f"Total Delta of CPU is {total_delta_cpu}\n"

    # build application part
    message = "Application with high impact:\n"
    app_info = important_applications.apply(format_application_info, axis=1)
    message += app_info.str.cat(sep="")

    for name in started:
        message += name + ' was started\n'

    for name in stopped:
        message += name + ' was stopped\n'

    for index, row in summary_df.iterrows():
        if row['process_count_difference'] > 0:
            message += f"{row['name']} opened {row['process_count_difference']} processes\n"
        elif row['process_count_difference'] < 0:
            message += f"{row['name']} closed {row['process_count_difference']} processes\n"

    return message
