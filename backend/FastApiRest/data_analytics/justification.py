from datetime import datetime, timedelta

import pandas
from pandas import DataFrame

from data_analytics.manipulation import get_justification_contained
from db_access.application import get_relevant_application_data
from model.data import EventAnomalyJustifications, JustificationData

ram_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant
cpu_relevancy_threshold = 0.05  # percentual threshold applications should have to be considered relevant


class ApplicationStat:  # class to store application data
    def __init__(self, ram: int, cpu: int, process_change: int):
        self.ram = ram
        self.cpu = cpu
        self.process_change = process_change  # same as event_headers (processes in applications were closed or opened marked with -1, 0 or 1)


def justify_pc_data_points(pc_total_df, significant_data_points: list, prior_justifications: list[EventAnomalyJustifications], pc_id: int, should_tag_as_anomaly: bool) -> list[EventAnomalyJustifications]:
    """
    Function to loop through event list to call gather_event_logs()

    How event log detection works:
    On init, make a map of applications, if any applications are added/removed later it will be registered
    :return:
    """
    justification_logs = []
    for point in significant_data_points:
        print('data point')
        print(point)

        existing_justification = get_justification_contained(point, prior_justifications)
        if existing_justification:
            justification_logs.append(existing_justification)
        else:
            total_ram = pc_total_df.loc[pc_total_df['measurement_time'] == point, 'ram'].iloc[0]
            total_cpu = pc_total_df.loc[pc_total_df['measurement_time'] == point, 'cpu'].iloc[0]

            applications_df, application_data_list = get_relevant_application_data(pc_id, point,
                                                                                   total_ram * ram_relevancy_threshold,
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
            total_delta_ram = total_ram - pc_total_df.loc[pc_total_df['measurement_time'] == till_timestamp, 'ram']
            total_delta_cpu = total_cpu - pc_total_df.loc[pc_total_df['measurement_time'] == till_timestamp, 'cpu']

            lj = EventAnomalyJustifications(
                timestamp=point,
                till_timestamp=till_timestamp,
                total_delta_ram=total_delta_ram,
                total_delta_cpu=total_delta_cpu,
                pc_just_started=pc_just_started,
                is_anomaly=should_tag_as_anomaly,
                justification_list=[]
            )
            justify_data_point(lj, applications_dict, pc_just_started)
            justification_logs.append(lj)
    print(justification_logs)
    return justification_logs


def justify_data_point(lj: EventAnomalyJustifications, applications_dict, pc_just_started: bool):
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
    # TODO: If amount of distinct times only 1 then it initially started
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


def justify_application_data_points(df: DataFrame, data_points: list, name: str, prior_justifications: list[EventAnomalyJustifications], should_tag_as_anomaly: bool) -> list[EventAnomalyJustifications]:
    # this method shares a lot of similarities with justify_data_point but it's meant only for one singular application
    justification_logs = []
    for point in data_points:
        justification_list = []

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

            # go through the specified time window
            last_row = None
            for index, row in time_window_rows.iterrows():
                if last_row is not None:
                    delta_ram = row['ram'] - last_row['ram']
                    delta_cpu = row['cpu'] - last_row['cpu']
                    process_change = row['process_count_difference']
                    warning = False
                    if (delta_ram > 0 > process_change and delta_cpu > 0) or (
                            delta_ram < 0 < process_change and delta_cpu < 0):
                        warning = True
                    justification_data = JustificationData(
                        application=name,
                        timestamp=row['measurement_time'],
                        started=False,
                        stopped=False,
                        process_change=process_change,
                        delta_ram=delta_ram,
                        delta_cpu=delta_cpu,
                        warning=warning
                    )

                    justification_list.append(justification_data)

                last_row = row

            event_anomaly = EventAnomalyJustifications(
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
