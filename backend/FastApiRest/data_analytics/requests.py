import glob
import os
import pandas as pd
import warnings
from data_analytics import involvement, manipulation, anomaly, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from data_analytics.helper import read_csv
from db_access.data import get_moving_avg_of_total_ram
import datetime
from model.data import AllocationClass
from model.pc import ForecastData

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
    df = df.set_index(pd.to_datetime(df['measurement_time']).astype('int64') // 10**6)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df, 'free_disk_space')
    df = manipulation.create_df_between(timestamp, days, 'D')
    df = predict_for_df(LR, df)

    # convert timestamps to datetime
    df['datetime'] = pd.to_datetime(df.index, unit='ms')
    data_list = []
    for _, row in df.iterrows():
        # Convert the 'measurement_time' from string to a datetime object
        data_list.append(ForecastData(**row.to_dict()))

    last_timestamp = None
    # find out if and when LinearRegression is less than 0 (free disk space running out)
    no_disk_space_rows = df[df['LinearRegression'] <= 0]
    if not no_disk_space_rows.empty:
        last_timestamp = no_disk_space_rows['datetime'].iloc[0]

    return data_list, last_timestamp


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
    allocation_list = [AllocationClass(name=key, allocation=value) for key, value in allocation_map.items()] # convert map into list of our model object to send via json

    print(allocation_list)
    # TODO: compare current value with last
    return pc_total_df, allocation_list, std, mean, trend_list
