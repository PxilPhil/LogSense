from typing import List

from model.data import EventData, CustomCondition
from model.data import AnomalyData
from scipy import stats
from data_analytics import manipulation

z_limit = 2
event_sensitivity_ram = 0.1
event_sensitivity_ram_occurrence = 0.05
event_sensitivity_cpu_occurrence = 0.05
event_sensitivity_cpu = 0.1

"""
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
def detect_event(selected_row, column, moving_avg, event_list, application):
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
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=6, change=difference,
                                   application=application, column=column)
            event_list.append(event_data)
        else:
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=7, change=difference,
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
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=6, change=cpu_difference,
                                       application=application_name, column='cpu')
                event_list.append(event_data)
            elif not previous_was_flagged:
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=7, change=cpu_difference,
                                       application=application_name, column='cpu')
                event_list.append(event_data)
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return event_list


def detect_anomalies(df, first_column, second_column):
    anomaly_list = []
    # Calculate Z-Score for first column
    df['zscore'] = stats.zscore(df[first_column])
    anomaly_df = df.loc[stats.zscore(df[first_column]) > z_limit]

    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']),
                                   application=row['name'],
                                   column=first_column)
        anomaly_list.append(anomaly_data)

    # Calculate Z-Score for second column
    df['zscore'] = stats.zscore(df[second_column])
    anomaly_df = df.loc[stats.zscore(df[second_column]) > z_limit]

    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']),
                                   application=row['name'],
                                   column=second_column)
        anomaly_list.append(anomaly_data)
    return anomaly_list


def check_custom_alerts(df, pc_total_df, custom_conditions: List[
    CustomCondition]):  # checks current dataframe if custom alerts have occurred
    # TODO: get custom alerts from database for user
    # TODO: Keep track of non-consistent format
    # Lookback and StartDate are only allowed for degree
    # TODO: Should compared_df always be possible maximum values (like total amount of RAM available)?
    selected_column = ""  # selected column for the current condition (like RAM)
    for condition in custom_conditions:
        # Check if conditions apply for application
        if condition.application:
            application_df = manipulation.select_rows_by_application(condition.application, df)
            if not condition.degree_trigger_value:
                check_custom_conditions(application_df, pc_total_df, condition)
            past_application_df = check_past_entries(application_df, condition)
        else:
            if not condition.degree_trigger_value:
                check_past_entries(pc_total_df, condition)
            past_pc_df = check_past_entries(application_df, condition)
    return 0

def check_past_entries(df, condition: CustomCondition):
    # checks if and in what way previous entries should be fetched from database
    # TODO: We can remove this method if we get data from database beforehand
    if not condition.degree_trigger_value:
        check_custom_conditions
    elif condition.lookback_time:
        print('lookback')
    elif condition.start_date:
        print('go from start date')



def check_custom_conditions(df, compared_df, condition: CustomCondition):
    # Check if any conditions apply for a custom alert

    detected_rows = []
    # Case 1: df is current application and compared_df is previous values
    # Case 2: df is current pc dataframe and compared_df are previous pc dataframes

    # Return early if the condition object is empty
    if not any([condition.percentage_trigger_value, condition.absolute_trigger_value, condition.degree_trigger_value]):
        return detected_rows

    for index, (row, compared_row) in enumerate(zip(df.iterrows(), compared_df.iterrows())):
        _, row_data = row
        _, compared_row_data = compared_row

        if condition.percentage_trigger_value:
            if row_data[condition.column] / compared_row_data[condition.column] > condition.percentage_trigger_value:
                detected_rows.append(row_data)
        elif condition.absolute_trigger_value:
            if row_data[condition.column] > condition.absolute_trigger_value:
                detected_rows.append(row_data)
        elif condition.degree_trigger_value:
            # TODO: Implement degree
            pass
        else:
            raise ValueError("Invalid condition object")

    return detected_rows
