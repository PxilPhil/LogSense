from typing import List

from pandas import DataFrame

from data_analytics.util.change_anomaly_detection import get_event_measurement_times, detect_anomalies
from data_analytics.util.stats import determine_linear_direction
from db_access.application import get_application_between

from db_access.pc import select_recent_state
from model.alerts import AlertNotification, CustomAlert


def check_for_alerts(user_id: int, custom_alert_list: List[CustomAlert], pc_df: DataFrame, start, end) -> List[
    AlertNotification]:
    """
    Checks for alerts that have appeared in a specified timeframe
    :return:
    """

    # first check for custom alerts
    alert_notifications: List[AlertNotification] = check_for_custom_alerts(user_id, pc_df, custom_alert_list, start,
                                                                           end)
    # check multiple complex, standard alerts
    check_for_anomalies_events(pc_df, alert_notifications)

    return alert_notifications


# todo: calculate variance/stability and display it as an alert, percentual appearences of anomalies and events, constantly rising linear data

def check_for_anomalies_events(pc_df, alert_notifications):
    ram_change_points = get_event_measurement_times(pc_df, pc_df,'ram', 3)  # only do it for ram since it makes no sense to do it for cpu
    anomalies_ram = detect_anomalies(pc_df, pc_df, 'ram')
    anomalies_cpu = detect_anomalies(pc_df, pc_df, 'cpu')

    alert_notifications.append(AlertNotification(
        type="RAM Events",
        message=f"Multiple RAM Events detected",
        severity_level=1,
        column="ram",
        application=None,
        detected_alert_list=ram_change_points
    ))

    alert_notifications.append(AlertNotification(
        type="CPU Anomalies",
        message=f"Multiple CPU Anomalies detected",
        severity_level=1,
        column="cpu",
        application=None,
        detected_alert_list=anomalies_cpu
    ))

    alert_notifications.append(AlertNotification(
        type="RAM Anomalies",
        message=f"Multiple RAM Anomalies detected",
        severity_level=1,
        column="ram",
        application=None,
        detected_alert_list=anomalies_ram
    ))

def check_for_linear_direction(df, alert_notifications, column_name):
    # check if there is a linear direction (values linearly falling or rising)

    linear_direction = determine_linear_direction(df, column_name, 0.05)
    if linear_direction > 0:
        alert_notifications.append(AlertNotification(
            type="Linear rising values",
            message="Linear rising values",
            severity_level=1,
            column=column_name,
            application=None,
            detected_alert_list=df['measurement_time'].iloc[-1]
        ))
    elif linear_direction < 0:
        alert_notifications.append(AlertNotification(
            type="Linear falling values",
            message="Linear falling values",
            severity_level=1,
            column=column_name,
            application = None,
            detected_alert_list=df['measurement_time'].iloc[-1]
        ))


def check_for_custom_alerts(pc_id, df, custom_alerts, start, end):
    alert_notifications = []

    for alert in custom_alerts:
        for condition in alert.conditions:
            selected_column = condition.column

            # check if it is an application
            if condition.application:
                df, application_data_list = get_application_between(pc_id, condition.application, start, end)

            # check if data frame is none (no data has been found)
            if df is not None:
                # check values should be detected with moving averages
                if condition.detect_via_moving_averages:
                    selected_column = 'moving_average_' + condition.column
                    df[selected_column] = df[condition.column].rolling(window=5).mean()
                    df[selected_column].fillna(df[condition.column], inplace=True)

                filtered_df = apply_condition(df, condition, selected_column)
                create_alert_notifications(filtered_df, alert_notifications, alert, condition)

    return alert_notifications


def apply_condition(df, condition, selected_column):
    if condition.column == "cpu":
        return df[df[selected_column] > condition.percentage_trigger_value]
    elif condition.percentage_trigger_value:
        state_dict = select_recent_state()
        return df.query(
            f'{selected_column} / {state_dict[condition.column]} {condition.operator} {condition.percentage_trigger_value}')
    elif condition.absolute_trigger_value:
        if condition.operator == '>':
            return df[df[selected_column] > condition.absolute_trigger_value]
        elif condition.operator == '<':
            return df[df[selected_column] < condition.absolute_trigger_value]
        elif condition.operator == '=':
            return df[df[selected_column] == condition.absolute_trigger_value]


def create_alert_notifications(filtered_df, alert_notifications, alert, condition):
    if not filtered_df.empty:
        timestamps = filtered_df['measurement_time'].tolist()
        alert_notification = AlertNotification(
            type=alert.type,
            message=alert.message,
            severity_level=alert.severity_level,
            column=condition.column,
            application=condition.application,
            detected_alert_list=timestamps
        )
        alert_notifications.append(alert_notification)
