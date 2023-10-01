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


def check_custom_alerts(pc_id, df, pc_total_df, custom_alerts: List[CustomAlert]):
    """
    Checks data that was requested if any custom alerts have occurred
    :param df:
    :param pc_total_df:
    :param custom_alerts:

    Documentation for Custom Alerts:
        - degree_trigger_value is used whenever a change should be a measured, when a condition uses it is also requires the property "lookback_time" on how many rows should be looked back upon or the property start_date from when data should be analyzed
        - percentage_trigger_value is used whenever a percentual trigger value should be set, in applications the formula is usage divided by maximum possible usage
        - absolute_trigger_value works with raw values like 5GB
    :return:
    """
    # TODO: If things doesnt work with iloc append with .values[0]
    for alert in custom_alerts:
        for condition in alert.conditions:
            if condition.degree_trigger_value:
                print('degree not implemented')
                # process_degree_trigger(condition, pc_id, df)
            elif condition.percentage_trigger_value:
                # finished
                process_percentage_trigger(condition, df)
            elif condition.absolute_trigger_value:
                # finished
                process_absolute_trigger(condition, pc_total_df, df)


def process_degree_trigger(condition, pc_id, df):
    if condition.start_date:
        # TODO: below this the df arent sorted by descending
        if condition.application:
            recent_app_df, recent_app_list = get_application_between(pc_id, condition.application, condition.start_date,
                                                                     df.index[-1])
            print(recent_app_df)
        else:
            recent_pc_df, recent_pc_list = get_total_pc_application_data_between(pc_id, condition.start_date,
                                                                                 df.index[-1])
            print(recent_pc_df)
    elif condition.lookback_time:
        # slope calculated via delta-y divided by delta-x
        # delta-y is calculated by last value divided by first value
        # delta-x is lookback_time
        if condition.application:
            recent_app_df, recent_app_list = get_latest_application_data(pc_id, condition.lookback_time,
                                                                         condition.application)
            print(recent_app_df)
        else:
            recent_pc_df, recent_pc_list = get_recent_pc_total_data(pc_id, condition.lookback_time)
            print(recent_pc_df)


def process_percentage_trigger(condition, df) -> bool:
    if condition.application:
        application_df = manipulation.select_rows_by_application(condition.application, df)
        return check_percentage_trigger(application_df, condition)
    else:
        return check_percentage_trigger(df, condition)


def process_absolute_trigger(condition, pc_total_df, df) -> bool:
    if condition.application:
        application_df = manipulation.select_rows_by_application(condition.application, df)
        return check_absolute_condition(application_df, condition)
    else:
        return check_absolute_condition(pc_total_df, condition)


def check_absolute_condition(df, condition) -> bool:
    if df[condition.column].values[0] >= condition.absolute_trigger_value:
        return True
    return False


def check_percentage_trigger(df, condition) -> bool:
    # TODO: Make this more universal for everything later on
    state_dict = select_recent_state()
    if df.iloc[0][condition.column] / state_dict[condition.column] > condition.percentage_trigger_value:
        return True
    return False


def check_degree_condition(current_df, prev_df, condition) -> bool:
    # Divide current column by last (oldest) row of the previous rows
    # delta_y_value = current_df.iloc[0][condition.column]-prev_df.iloc[-1][condition.column]
    delta_y_value = current_df.iloc[0][condition.column] - prev_df[prev_df.index.min()][condition.column]
    degree_value = delta_y_value / (len(prev_df) + len(current_df))
    if degree_value > condition.degree_trigger_value:
        return True
    return False
