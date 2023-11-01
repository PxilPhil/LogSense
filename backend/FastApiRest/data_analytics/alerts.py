from db_access.application import get_application_between

from db_access.pc import select_recent_state, get_recent_pc_total_data, get_ram_time_series_between
from model.data import AnomalyData
from model.alerts import AlertNotification

z_limit = 2
event_sensitivity_ram = 0.1
event_sensitivity_ram_occurrence = 0.05
event_sensitivity_cpu_occurrence = 0.05
event_sensitivity_cpu = 0.1

"""
Event Sensitivity for RAM is always the percentual value of the difference between the current value and the moving average of the last 5 rows
Event Sensitivity for CPU is always a percentual limiter, e.g. the pc cpu allocation has to rise by 10% to be registered as an event
"""


def detect_anomalies_via_score(anomaly_list, anomaly_df, column):
    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']),
                                   application=row['name'],
                                   column=column)
        anomaly_list.append(anomaly_data)


def check_for_custom_alerts(pc_id, df, custom_alerts, start, end):
    alert_notifications = []

    for alert in custom_alerts:
        for condition in alert.conditions:
            selected_column = condition.column

            # check if it is an application
            if condition.application:
                df, application_data_list = get_application_between(pc_id, condition.application, start, end)

            # check values should be detected with moving averages
            if condition.detect_via_moving_averages:
                selected_column = 'moving_average_' + condition.column
                print(condition.column)
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
