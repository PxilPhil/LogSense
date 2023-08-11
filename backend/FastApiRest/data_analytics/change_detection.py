import numpy as np
import ruptures as rpt
from pandas import DataFrame

from db_access.application import get_application_data_before

penalty_value = 0.5  # value used for "penalizing" the pelting model for overfitting, decrease to detect more insignicant events and vice versa -> sensitivity in other words

"""
    Change detection works well for RAM but not for things like cpu
    -> penalty_value should be 0.5 to 1 depending on sensitivity
    -> indizes are subtracted by 1 because they appear to begin counting from 1, without it we get better results however?
    It highlights data points when large changes have occured (
    
    Solution for CPU:
    -> run pelting on it and sort out false positives
    -> use anomaly detection instead (current approach) and bucket if necessary
    
    Approach for finding meaningful events:
    Run pelting algorithm on the total pcdataframe to find change points
    Then fetch all available application data for the last few entries from change points to check if applications or processes were closed or opened
    Determine if a event is reasonable or not
    Keep in mind to check on time gaps as well
"""


class EventLog:  # class to store event log data
    def __init__(self, application, started, stopped, process_change, delta_ram, delta_cpu, warning):
        self.application = application
        self.started = started
        self.stopped = stopped
        self.process_change = process_change
        self.delta_ram = delta_ram
        self.delta_cpu = delta_cpu
        self.warning = warning


class EventLogs:
    def __init__(self, timestamp, event_log_list):
        self.timestamp = timestamp
        self.event_log_list = event_log_list


class ApplicationStat:  # class to store application data
    def __init__(self, ram: int, cpu: int, process_change: int):
        self.ram = ram
        self.cpu = cpu
        self.process_change = process_change  # same as event_headers (processes in applications were closed or opened marked with -1, 0 or 1)


def detect_change_events(df: DataFrame,
                         column: str):  # should not be used for data with very high variance like cpu usage
    df_values = df[column].values  # Access values
    detector = rpt.Pelt(model="rbf").fit(df_values.reshape(-1, 1))  # Reshape data
    change_points = detector.predict(pen=penalty_value)  # data points where significant change was detected
    change_points = np.array(change_points) - 1
    change_points_measurement_times = df['measurement_time'].iloc[change_points].tolist()
    print(change_points_measurement_times)
    return change_points_measurement_times


def check_on_events(change_points: list, pc_id: int):
    """
    Function to loop through event list to call gather_event_logs()

    How event log detection works:
    On init, make a map of applications, if any applications are added/removed later it will be registered
    :return:
    """
    event_logs = dict() # Map <timestamp, List<EventLogs>>
    for entry in change_points:
        applications_df, application_data_list = get_application_data_before(pc_id, entry, 10)
        # group by application data
        # TODO: only select relevant applications
        applications_dict = dict()
        print(applications_df)
        for index, row in applications_df.iterrows():
            application_stat = ApplicationStat(
                ram=row['ram'],
                cpu=row['cpu'],
                process_change=row['process_count_difference']
            )
            applications_dict[row['measurement_time']] = {row['name']: application_stat}

        gather_event_logs(event_logs, entry, applications_dict)
    return event_logs

def gather_event_logs(event_logs, entry, applications_dict):
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
    last_application_dict = None
    for timestamp, application_dict in applications_dict.items():  # looping through our Map<timestamp, Map<name, values>
        event_logs[timestamp] = []
        for name, data in application_dict.items():  # looping through our Map<name, values>
            if last_application_dict:
                started = False
                stopped = False
                process_change = 0
                delta_ram = 0
                delta_cpu = 0
                warning = False

                if name not in last_application_dict:  # application was started
                    started = True
                    delta_ram = data.ram
                    delta_cpu = data.cpu
                elif name in last_application_dict and name not in last_application_dict:  # application was stopped
                    stopped = True
                    delta_ram = data.ram
                    delta_cpu = data.cpu
                else:  # default case: nothing happened or only processes were stopped or started
                    warning = True
                    delta_ram = data.ram - last_application_dict[name].ram
                    delta_cpu = data.cpu - last_application_dict[name].cpu
                process_change = data.process_change

                event_log = EventLog(name, started, stopped, process_change, delta_ram, delta_cpu, warning)
                event_logs[timestamp].append(event_log)
        last_application_dict = application_dict