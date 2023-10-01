from typing import List

from db_access.application import get_latest_application_data, get_application_between
from db_access.pc import select_recent_state, get_recent_pc_total_data, get_total_pc_application_data_between
from model.data import EventData
from model.data import AnomalyData
from model.alerts import CustomAlerts, CustomAlert, CustomCondition
from scipy import stats
from data_analytics import manipulation

event_sensitivity_ram = 0.1
event_sensitivity_ram_occurrence = 0.05
event_sensitivity_cpu_occurrence = 0.05
event_sensitivity_cpu = 0.1

"""
This is deprecated code which was used for manual change (in our case event) detection
It worked by utilizing moving averages and dividing the current data point value with it. If the division was above a set threshold (like 10%) it was registered as an event
Replaced with a pelting algorithm from the ruptures library


Event Sensitivity for RAM is always the percentual value of the difference between the current value and the moving average of the last 5 rows
Event Sensitivity for CPU is always a percentual limiter, e.g. the pc cpu allocation has to rise by 10% to be registered as an event
"""

def has_event_occurred(df, moving_avg_ram, moving_avg_cpu):
    percentual_change = df['residentSetSize'].values[0] / moving_avg_ram
    if abs(percentual_change - 1) > event_sensitivity_ram_occurrence or (
            df['cpuUsage'].values[0] - moving_avg_cpu) > event_sensitivity_cpu_occurrence:
        return True
    return False


# TODO: Merge the event detection methods
def detect_ram_event(selected_row, column, moving_avg, event_list, application):
    percentual_change = selected_row[column].values[0] / moving_avg
    event_header = selected_row['processCountDifference'].values[0]
    if abs(percentual_change - 1) > event_sensitivity_ram:
        if (percentual_change > 1 and event_header > 0) or (percentual_change < 1 and event_header < 0):
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=1, change=percentual_change,
                                   application=application, column=column)
            event_list.append(event_data)
        else:
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=2, change=percentual_change,
                                   application=application, column=column)
            event_list.append(event_data)


def detect_cpu_event(selected_row, column, moving_avg, event_list, application):
    difference = selected_row[column].values[0] - moving_avg
    event_header = selected_row['processCountDifference'].values[0]
    if abs(difference) > event_sensitivity_cpu:
        if (difference > 0 and event_header > 0) or (difference < 0 and event_header < 0):
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=3, change=difference,
                                   application=application, column=column)
            event_list.append(event_data)
        else:
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=4, change=difference,
                                   application=application, column=column)
            event_list.append(event_data)


def detect_multiple_events(selected_row, application_name):
    event_list = []
    selected_row['percentage_change'] = selected_row['ram'] / selected_row['rolling_avg_ram'].shift()
    selected_row['cpu_difference'] = selected_row['cpu'] - selected_row['rolling_avg_cpu'].shift()
    selected_row = selected_row.dropna()
    previous_was_flagged = False
    for index, row in selected_row.iterrows():
        percentual_change = row['percentage_change']
        cpu_difference = row['cpu_difference']
        event_header = row['process_count_difference']
        # check for ram events
        if abs(percentual_change - 1) > event_sensitivity_ram:
            if (percentual_change > 1 and event_header > 0) or (percentual_change < 1 and event_header < 0):
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=1, change=percentual_change,
                                       application=application_name, column='ram')
                event_list.append(event_data)
            elif not previous_was_flagged:
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=2, change=percentual_change,
                                       application=application_name, column='ram')
                event_list.append(event_data)
            previous_was_flagged = True
        else:
            previous_was_flagged = False
        # check for cpu events
        if cpu_difference > event_sensitivity_cpu:
            if (cpu_difference > 0 and event_header > 0) or (cpu_difference < 0 and event_header < 0):
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=3, change=cpu_difference,
                                       application=application_name, column='cpu')
                event_list.append(event_data)
            elif not previous_was_flagged:
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=4, change=cpu_difference,
                                       application=application_name, column='cpu')
                event_list.append(event_data)
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return event_list
