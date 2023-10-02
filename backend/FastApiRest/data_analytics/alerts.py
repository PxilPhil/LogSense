from typing import List

from db_access.application import get_latest_application_data, get_application_between
from db_access.pc import select_recent_state, get_recent_pc_total_data, get_total_pc_application_data_between
from model.data import EventData
from model.data import AnomalyData
from model.alerts import CustomAlerts, CustomAlert, CustomCondition
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


def detect_anomalies(df, first_column, second_column):
    anomaly_list = []
    # Calculate Z-Score for first column
    df['zscore'] = stats.zscore(df[first_column])
    anomaly_df = df.loc[stats.zscore(df[first_column]) > z_limit]
    detect_anomalies_via_score(anomaly_list, anomaly_df, first_column)

    # Calculate Z-Score for second column
    df['zscore'] = stats.zscore(df[second_column])
    anomaly_df = df.loc[stats.zscore(df[second_column]) > z_limit]
    detect_anomalies_via_score(anomaly_list, anomaly_df, second_column)

    return anomaly_list


def detect_anomalies_via_score(anomaly_list, anomaly_df, column):
    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']),
                                   application=row['name'],
                                   column=column)
        anomaly_list.append(anomaly_data)


def check_for_custom_alerts(pc_id, df, custom_alerts: List[CustomAlert], start, end):
    """
    Checks data that was requested if any custom alerts have occurred
    :param end:
    :param start:
    :param df:
    :param pc_total_df:
    :param custom_alerts:

    Documentation for Custom Alerts:
        - percentage_trigger_value is used whenever a percentual trigger value should be set, in applications the formula is usage divided by maximum possible usage
        - absolute_trigger_value works with raw values like 5GB
    :return:
    """
    # TODO: If things doesnt work with iloc append with .values[0]
    # TODO: This is just a example implemeentation, change it lateer on
    # if absolute_trigger_value or relative_trigger_value with cpu=> we dont need anything more
    # if relative_trigger_value and NOT CPU =>
    for alert in custom_alerts:
        print(alert.message)
        for condition in alert.conditions:
            if condition.application:
                df, application_data_list = get_application_between(pc_id, condition.application, start, end)
            if condition.percentage_trigger_value and condition.column != "cpu":
                print(check_percentage_trigger(df, condition))
            elif condition.column == "cpu":
                condition.absolute_trigger_value = condition.percentage_trigger_value
                print(check_absolute_trigger(df, condition))
            else:
                print(check_absolute_trigger(df, condition))

def check_percentage_trigger(df, condition: CustomCondition) -> bool:
    # TODO: Make this more universal for everything later on
    print(df)
    state_dict = select_recent_state()
    filtered_df = df[df['moving_average_'+condition.column] / state_dict[condition.column] > condition.percentage_trigger_value]
    if not filtered_df.empty:
        return True
    return False


def check_absolute_trigger(df, condition: CustomCondition) -> bool:
    print(df)
    filtered_df = df[df['moving_average_'+condition.column] > condition.absolute_trigger_value]
    if not filtered_df.empty:
        return True
    return False

