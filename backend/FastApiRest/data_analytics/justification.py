from datetime import datetime, timedelta

import numpy as np
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

            applications_dict = dict()
            for index, row in applications_df.iterrows():
                application_stat = ApplicationStat(
                    ram=row['ram'],
                    cpu=row['cpu'],
                    process_change=row['process_count_difference']
                )
                applications_dict[row['measurement_time']] = {row['name']: application_stat}

            till_timestamp = applications_df['measurement_time'].min()

            message = create_justification_message(pc_just_started, None, None)
            message += justify_data_point(applications_dict, pc_just_started)

            justification = Justification(
                timestamp=point,
                till_timestamp=till_timestamp,
                is_anomaly=should_tag_as_anomaly,
                justification_message=message
            )

            justification_logs.append(justification)
    print(justification_logs)
    return justification_logs


def justify_data_point(applications_dict, pc_just_started: bool) -> str:
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
    last_application_dict = None
    message = ""

    for timestamp, application_dict in applications_dict.items():  # looping through our Map<timestamp, Map<name, values>
        for name, data in application_dict.items():  # looping through our Map<name, values>
            if last_application_dict or pc_just_started:
                started = False
                stopped = False
                process_change = 0
                delta_ram = 0
                delta_cpu = 0
                warning = False
                if (delta_ram > 0 > process_change and delta_cpu > 0) or (
                        delta_ram < 0 < process_change and delta_cpu < 0):
                    warning = True

                if pc_just_started or name not in last_application_dict:  # application was started
                    started = True
                    delta_ram = data.ram
                    delta_cpu = data.cpu
                    process_change = data.process_change
                elif name in last_application_dict and name not in last_application_dict:  # application was stopped
                    stopped = True
                    delta_ram = last_application_dict[name].ram
                    delta_cpu = last_application_dict[name].cpu
                    process_change = last_application_dict[name].process_change
                else:  # default case: nothing happened or only processes were stopped or started
                    delta_ram = data.ram - last_application_dict[name].ram
                    delta_cpu = data.cpu - last_application_dict[name].cpu
                    print(delta_cpu)
                    process_change = data.process_change
                    if not ((delta_ram < 0 < process_change and delta_cpu < 0) or (
                            delta_ram > 0 > process_change and delta_cpu > 0)):
                        warning = True

                message = append_justification_message(message, name, timestamp, started, stopped, process_change,
                                                       delta_ram, delta_cpu, warning)

        last_application_dict = application_dict
    return message


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

        justification_message = create_justification_message(False, total_delta_ram, total_delta_cpu)
        justification_message += check_application(application_df, name, point)
        justification = Justification(
            timestamp=point,
            till_timestamp=start_point,
            is_anomaly=False,
            justification_message=justification_message
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
            justification_message = create_justification_message(False, total_delta_ram, total_delta_cpu)
            justification_message += check_application(time_window_rows, name, point)

            event_anomaly = Justification(
                timestamp=point,
                till_timestamp=till_timestamp_point,
                is_anomaly=should_tag_as_anomaly,
                justification_message=justification_message
            )
            justification_logs.append(event_anomaly)

    return justification_logs


def check_application(time_window_rows, name: str,
                      timestamp: datetime) -> str:  # checks application in order to get justifications
    # go through the specified time window

    message = ""
    last_row = None
    for index, row in time_window_rows.iterrows():
        if last_row is not None:
            warning = False
            started = False
            delta_ram = row['ram'] - last_row['ram']
            delta_cpu = row['cpu'] - last_row['cpu']
            process_change = row['process_count_difference']
            if (delta_ram > 0 > process_change and delta_cpu > 0) or (
                    delta_ram < 0 < process_change and delta_cpu < 0):
                warning = True

            time_difference = row['measurement_time'] - last_row['measurement_time']

            # application has just started if its the only entry or iif the difference to the last row is more than
            # two minutes
            if (timestamp == index and len(time_window_rows) == 1) or (time_difference > timedelta(minutes=2)):
                started = True
            message = append_justification_message(message, name, timestamp, started, False, process_change,
                                                   delta_ram, delta_cpu, warning)

        last_row = row
    return message


def calc_deltas(df: DataFrame, point: datetime):
    if df is not None:
        total_ram = df.loc[df['measurement_time'] == point, 'ram'].iloc[0]
        total_cpu = df.loc[df['measurement_time'] == point, 'cpu'].iloc[0]

        total_delta_ram = total_ram - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'ram'].iloc[0]
        total_delta_cpu = total_cpu - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'cpu'].iloc[0]
        return np.int64(total_delta_ram).item(), np.int64(total_delta_cpu).item()

def create_justification_message(pc_just_started: bool, total_delta_ram, total_delta_cpu) -> str:
    message = ""
    if pc_just_started:
        message = "PC just started\n"
    if total_delta_ram:
        message += f"Total Delta of RAM is {total_delta_ram}\n"
    if total_delta_cpu:
        message += f"Total Delta of CPU is {total_delta_cpu}\n"
    return message

def append_justification_message(existing_message: str, application, timestamp, started, stopped, process_change,
                                 delta_ram, delta_cpu,
                                 warning) -> str:
    message = f"Regarding {application} at {timestamp}:\n"

    if started:
        message += f"{application} has been started.\n"

    if stopped:
        message += f"{application} has been stopped.\n"

    if process_change > 0 or process_change < 0:
        message += f"Number of processes has changed by {process_change}.\n"

    if delta_ram:
        message += f"RAM usage has changed by {delta_ram}.\n"

    if delta_cpu:
        message += f"CPU usage has changed by {delta_cpu}.\n"

    if warning:
        message += "Please be aware that this might require your attention.\n"
    existing_message += "\n" + message
    return existing_message
