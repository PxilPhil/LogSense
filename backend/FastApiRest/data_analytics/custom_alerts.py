from typing import List

from db_access.application import get_latest_application_data, get_application_between
from db_access.pc import select_recent_state, get_recent_pc_total_data, get_ram_time_series_between
from model.alerts import CustomAlert
from data_analytics.util import manipulation


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
                process_degree_trigger(condition, pc_id, df)
            elif condition.percentage_trigger_value:
                process_percentage_trigger(condition, df)
            elif condition.absolute_trigger_value:
                process_absolute_trigger(condition, pc_total_df, df)


def process_degree_trigger(condition, pc_id, df):
    if condition.start_date:
        # TODO: below this the df arent sorted by descending
        if condition.application:
            recent_app_df, recent_app_list = get_application_between(pc_id, condition.application, condition.start_date,
                                                                     df.index[-1])
            print(recent_app_df)
        else:
            recent_pc_df, recent_pc_list = get_ram_time_series_between(pc_id, condition.start_date,
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


def process_percentage_trigger(condition, df):
    if condition.application:
        application_df = manipulation.select_rows_by_application(condition.application, df)
        check_relative_condition(application_df, condition)
    else:
        check_relative_condition(df, condition)


def process_absolute_trigger(condition, pc_total_df, df):
    if condition.application:
        application_df = manipulation.select_rows_by_application(condition.application, df)
        check_absolute_condition(application_df, condition)
    else:
        check_absolute_condition(pc_total_df, condition)


def check_absolute_condition(df, condition):
    if df[condition.column].values[0] >= condition.absolute_trigger_value:
        return True
    return False


def check_relative_condition(df, condition):
    # TODO: Make this more universal for everything later on
    if str.lower(condition.column) == "ram":
        state_dict = select_recent_state()
        if df.iloc[0][condition.column] / state_dict[condition.column]:
            return True
        return False
    if str.lower(condition.column) == "cpu":
        if df[condition.column].values[0] >= condition.relative_trigger_value:
            return True
        return False
    print('not implemented yet')
    return False


def check_degree_condition(current_df, prev_df, condition):
    # Divide current column by last (oldest) row of the previous rows
    # delta_y_value = current_df.iloc[0][condition.column]-prev_df.iloc[-1][condition.column]
    delta_y_value = current_df.iloc[0][condition.column] - prev_df[prev_df.index.min()][condition.column]
    degree_value = delta_y_value / (len(prev_df) + len(current_df))
    if degree_value > condition.degree_trigger_value:
        return True
    return False
