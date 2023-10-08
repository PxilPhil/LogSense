from datetime import datetime, timedelta

import numpy as np
import pandas
from pandas import DataFrame

from data_analytics.manipulation import get_justification_contained
from db_access.application import get_relevant_application_data, get_application_between
from db_access.pc import get_pc_data_at_measurement
from model.data import Justification, JustificationData

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

            justification = Justification(
                timestamp=point,
                till_timestamp=till_timestamp,
                pc_just_started=pc_just_started,
                total_delta_ram=None,
                total_delta_cpu=None,
                is_anomaly=should_tag_as_anomaly,
                justification_list=[]
            )
            calc_deltas(pc_total_df, justification, point)

            justify_data_point(justification, applications_dict, pc_just_started)
            justification_logs.append(justification)
    print(justification_logs)
    return justification_logs


def justify_data_point(lj: Justification, applications_dict, pc_just_started: bool):
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
    last_application_dict = None
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

                justification_data = JustificationData(
                    application=name,
                    timestamp=timestamp,
                    started=started,
                    stopped=stopped,
                    process_change=process_change,
                    delta_ram=delta_ram,
                    delta_cpu=delta_cpu,
                    warning=warning
                )

                lj.justification_list.append(justification_data)
        last_application_dict = application_dict


def justify_application_data_points(data_points: list, name: str, pc_id: int) -> list[
    Justification]:
    """
    Method to justify application data points without the application dataframe, mainly used for alerts
    :param df:
    :param data_points:
    :param name:
    :param prior_justifications:
    :param should_tag_as_anomaly:
    :return:
    """
    justifications: list[Justification] = []
    for point in data_points:
        start_point: datetime = point - timedelta(minutes=5)
        application_df, application_data_list = get_application_between(pc_id, name, start_point, point)
        # check application for justifications
        justification_list = check_application(application_df, name, point)
        justification = Justification(
            timestamp=point,
            till_timestamp=start_point,
            total_delta_ram=None,
            total_delta_cpu=None,
            pc_just_started=None,
            is_anomaly=False,
            justification_list=justification_list
        )

        calc_deltas(application_df, justification, point)
        justifications.append(justification)
    return justifications


def justify_application_df(df: DataFrame, data_points: list, name: str,
                           prior_justifications: list[Justification], should_tag_as_anomaly: bool) -> list[
    Justification]:
    # this method shares a lot of similarities with justify_data_point but it's meant only for one singular application
    justification_logs = []
    for point in data_points:

        time_window_start = df.loc[point, 'measurement_time'] - timedelta(minutes=5)
        time_window_end = df.loc[point, 'measurement_time']

        existing_justification = get_justification_contained(time_window_end, prior_justifications)
        if existing_justification:
            justification_logs.append(existing_justification)
        else:
            # select all rows in the specified time window
            time_window_rows = df[
                (df['measurement_time'] >= time_window_start) & (df['measurement_time'] <= time_window_end)]
            total_delta_ram = time_window_rows.iloc[-1]['ram'] - time_window_rows.iloc[0]['ram']
            total_delta_cpu = time_window_rows.iloc[-1]['cpu'] - time_window_rows.iloc[0]['cpu']

            # check application for justifications
            justification_list = check_application(time_window_rows, name, point)

            event_anomaly = Justification(
                timestamp=time_window_end,
                till_timestamp=time_window_start,
                total_delta_ram=total_delta_ram,
                total_delta_cpu=total_delta_cpu,
                pc_just_started=None,
                is_anomaly=should_tag_as_anomaly,
                justification_list=justification_list
            )
            justification_logs.append(event_anomaly)

    return justification_logs


def check_application(time_window_rows, name: str, timestamp: datetime) -> list[
    JustificationData]:  # checks application in order to get justfications
    # go through the specified time window
    justification_list = []

    last_row = None
    for index, row in time_window_rows.iterrows():
        if last_row is not None:
            warning = False
            started=False
            delta_ram = row['ram'] - last_row['ram']
            delta_cpu = row['cpu'] - last_row['cpu']
            process_change = row['process_count_difference']
            if (delta_ram > 0 > process_change and delta_cpu > 0) or (
                    delta_ram < 0 < process_change and delta_cpu < 0):
                warning = True

            time_difference = row['measurement_time'] - last_row['measurement_time']

            # application has just started if its the only entry or iif the difference to the last row is more than two minutes
            if (timestamp == index and len(time_window_rows)==1) or (time_difference>timedelta(minutes=2)):
                started=True
            justification_data = JustificationData(
                application=name,
                timestamp=row['measurement_time'],
                started=started,
                stopped=False,
                process_change=process_change,
                delta_ram=delta_ram,
                delta_cpu=delta_cpu,
                warning=warning
            )

            justification_list.append(justification_data)

        last_row = row
    return justification_list


def calc_deltas(df: DataFrame, justification: Justification, point: datetime):
    if df is not None:
        total_ram = df.loc[df['measurement_time'] == point, 'ram'].iloc[0]
        total_cpu = df.loc[df['measurement_time'] == point, 'cpu'].iloc[0]

        total_delta_ram = total_ram - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'ram'].iloc[0]
        total_delta_cpu = total_cpu - df.loc[df['measurement_time'] == df['measurement_time'].min(), 'cpu'].iloc[0]
        justification.total_delta_ram = np.int64(total_delta_ram).item()
        justification.total_delta_cpu = np.int64(total_delta_cpu).item()
