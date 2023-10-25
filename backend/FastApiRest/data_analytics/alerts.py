from typing import List

import pandas as pd

from data_analytics.justification import justify_pc_data_points, justify_application_df
from db_access.application import get_latest_application_data, get_application_between

from db_access.pc import select_recent_state, get_recent_pc_total_data, get_ram_time_series
from model.data import EventData
from model.data import AnomalyData
from model.alerts import CustomAlerts, CustomAlert, CustomCondition, AlertNotification
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


def check_for_custom_alerts(pc_id, df, custom_alerts: List[CustomAlert], start, end) -> List[AlertNotification]:
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

    filtered_df = pd.DataFrame()  # data frame containing filtered values for the alerts
    alert_notifications: List[AlertNotification] = []
    for alert in custom_alerts:
        detected_alert_list = []
        for condition in alert.conditions: # TODO: Remove multiple conditions from alerts
            selected_column = condition.column
            # get application data frame if required
            if condition.application:
                df, application_data_list = get_application_between(pc_id, condition.application, start, end)
            # calculate moving averages if required
            if condition.detect_via_moving_averages:
                selected_column = 'moving_average_' + condition.column
                df[selected_column] = df[condition.column].rolling(window=5).mean()
                df[selected_column].fillna(df[condition.column], inplace=True)
            # check if any values of columns are needed to fetch

            # check conditions
            if condition.percentage_trigger_value and condition.column != "cpu":
                filtered_df = check_percentage_trigger(df, condition, selected_column)
            elif condition.column == "cpu":  # since cpu values could be seen as both percentage and absolute values
                condition.absolute_trigger_value = condition.percentage_trigger_value
                filtered_df = check_absolute_trigger(df, condition, selected_column)
            else:
                filtered_df = check_absolute_trigger(df, condition, selected_column)
            # create notification
            create_alert_notifications(df, filtered_df, alert_notifications, alert, condition, pc_id)
    return alert_notifications


def create_alert_notifications(df, filtered_df, alert_notifications, alert, condition, pc_id):
    if len(filtered_df) > 0:
        timestamps = filtered_df['measurement_time'].tolist()
        # create the alert notification object
        alert_notification = AlertNotification(
            type=alert.type,
            message=alert.message,
            severity_level=alert.severity_level,
            column=condition.column,
            application=condition.application,
            detected_alert_list=timestamps
        )
        alert_notifications.append(alert_notification)


def check_percentage_trigger(df, condition: CustomCondition, selected_column):
    state_dict = select_recent_state()
    if condition.operator == '>':
        return df[df[selected_column] / state_dict[
            condition.column] > condition.percentage_trigger_value]
    elif condition.operator == '<':
        return df[df[selected_column] / state_dict[
            condition.column] < condition.percentage_trigger_value]
    elif condition.operator == '=':
        return df[df[selected_column] / state_dict[
            condition.column] == condition.percentage_trigger_value]


def check_absolute_trigger(df, condition: CustomCondition, selected_column):
    if condition.operator == '>':
        return df[df[selected_column] > condition.absolute_trigger_value]
    elif condition.operator == '<':
        return df[df[selected_column] < condition.absolute_trigger_value]
    elif condition.operator == '=':
        return df[df[selected_column] == condition.absolute_trigger_value]
