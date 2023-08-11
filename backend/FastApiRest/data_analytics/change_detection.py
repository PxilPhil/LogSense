from datetime import timedelta

from pandas import DataFrame
import ruptures as rpt
import numpy as np
from data_analytics import manipulation

from db_access.application import get_latest_application_data, get_application_data_before

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
    def __init__(self, application, interruption, process_change, delta_ram, delta_cpu, warning):
        self.application = application
        self.interruption = interruption
        self.process_change = process_change
        self.delta_ram = delta_ram
        self.delta_cpu = delta_cpu
        self.warning = warning


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
    event_logs = dict()  # a dictionary containing our detected event logs
    for entry in change_points:
        applications_df, application_data_list = get_application_data_before(pc_id, entry, 10)
        # group by application data
        # TODO: replace with pandas function
        # TODO: only select relevant applications
        applications_dict = dict()
        for index, row in applications_df.iterrows():
            application_stat = ApplicationStat(
                ram=row['ram'],
                cpu=row['cpu'],
                process_change=row['process_count_difference']
            )
            applications_dict[row['measurement_time']] = {row['name']: application_stat}

        last_application_data = None
        for timestamp, application_data in applications_dict.items():
            for name, data in application_data.items():
                if last_application_data:
                    # Check if the name is in the current application_data
                    if name not in application_data:
                        print(f"{name} exists in the current application_data.")

                    # Check if the name is in the previous application_data but not in the current one
                    if name in last_application_data and name not in application_data:
                        print(f"{name} was in the last application_data but not in the current one.")
            last_application_data = application_data
def gather_event_logs():
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """
