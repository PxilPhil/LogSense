import glob
import os
import pandas as pd
import warnings
from data_analytics import involvement, manipulation, anomaly, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from data_analytics.helper import read_csv, calc_end_timestamp
from db_access.data import get_moving_avg_of_total_ram

warnings.filterwarnings("ignore")
queue_df = pd.DataFrame()  # current data frame


def ingest_process_data(df):
    df = df.set_index('timestamp')
    anomaly_list = []
    pc_total_df = manipulation.group_by_timestamp(df)
    relevant_list = involvement.detect_relevancy(pc_total_df, df,
                                                 'residentSetSize')  # hardcoded to work for ram
    for application in relevant_list:
        selected_row = manipulation.select_rows_by_application(application, df)
        # TODO: Fetch from Database if last row was an anomaly
        moving_avg = get_moving_avg_of_total_ram(1, application)
        if moving_avg > 0:
            last_entry_was_anomaly = False
            anomaly.detect_anomaly(selected_row, 'residentSetSize', moving_avg, last_entry_was_anomaly, anomaly_list, application)
    return pc_total_df, anomaly_list


def predict_resource_data(df, days):  # predict disk space for the next x days
    # read dataframe, elect only needed columns
    df = df.filter(['measurement_time', 'free_disk_space'])
    df = df.set_index('measurement_time')
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df)
    df = manipulation.create_df_between(timestamp, calc_end_timestamp(timestamp=timestamp, days=days), 'D')
    df = predict_for_df(LR, df)
    return df


def fetch_application_data(df, application_name):  # supposed to analyze trends and everything in detail for one certain application
    # find trends
    df = manipulation.calculate_moving_avg(df, 'ram')
    trend_list = trend.detect_trends(df, 'MovingAvg')
    # find anomalies
    anomaly_list = anomaly.detect_anomalies(df, 'ram', application_name)
    # get stats
    std = df['ram'].std()
    mean = df['ram'].mean()
    return df, anomaly_list, trend_list, std, mean


def fetch_pc_data(df, pc_total_df, column):  # fetch all application data in database for a certain time period
    # find trends
    pc_total_df = manipulation.calculate_moving_avg(pc_total_df, column)  # TODO: GET FROM DATABASE
    trend_list = trend.detect_trends(pc_total_df, 'MovingAvg')
    # get stats
    std = pc_total_df[column].std()
    mean = pc_total_df[column].mean()
    # get allocation percentage
    latest_total_value = pc_total_df.at[pc_total_df.index.max(), column]
    allocation_map = stats.calc_allocation(latest_total_value, column, df)
    # TODO: compare current value with last
    return pc_total_df, allocation_map, std, mean, trend_list
