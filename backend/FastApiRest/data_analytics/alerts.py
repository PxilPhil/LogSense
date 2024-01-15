from typing import List

from pandas import DataFrame

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
    alert_notifications = check_for_custom_alerts(user_id, pc_df, custom_alert_list, start, end)
    # check multiple complex, standard alerts

    return alert_notifications


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
        return df.query(f'{selected_column} / {state_dict[condition.column]} {condition.operator} {condition.percentage_trigger_value}')
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
