import glob
import os
import pandas as pd
import warnings
from data_analytics import involvement, manipulation, anomaly, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from data_analytics.helper import read_csv, calc_end_timestamp

warnings.filterwarnings("ignore")
queue_df = pd.DataFrame()  # current data frame

def ingest_process_data(new_df):
    #TODO: We could already detect a lot of useful data on ingest, find out if we leave it at a hybrid approach or ingest
    global queue_df
    new_df = new_df.set_index('timestamp')
    anomaly_map = dict()
    print(queue_df)
    queue_df = pd.concat([queue_df, new_df])
    print(queue_df)
    pc_total_df = manipulation.group_by_timestamp(new_df)
    if queue_df.index.nunique() > 5:  # don't do anything yet until we have saved previous values
        relevant_list = involvement.detect_relevancy(pc_total_df, queue_df,
                                                     'residentSetSize')  # hardcoded to work for ram
        for application in relevant_list:
            selected_row = manipulation.select_rows_by_application(application, queue_df)
            selected_row = manipulation.calculate_moving_avg(selected_row, 'residentSetSize')
            anomaly_list = anomaly.detect_anomalies(selected_row, 'residentSetSize')
            if len(anomaly_list) > 0:
                anomaly_map[application] = anomaly_list
        queue_df = queue_df.drop(queue_df.index[1])
    return pc_total_df, anomaly_map


def predict_resource_data(df, days):
    # read dataframe, remove nans, select only needed columns
    df = queue_df  # TODO: Only temporary until database access works
    df = df.dropna()
    df = df.filter(['timestamp', 'freeDiskSpace'])
    df = df.set_index('timestamp')
    print(df)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df)
    df = manipulation.create_df_between(timestamp, calc_end_timestamp(timestamp=timestamp, days=days), 'D')
    df = predict_for_df(LR, df)
    print(df)
    return df


def fetch_application_data(df):  # supposed to analyze trends and everything in detail for one certain application
    df = queue_df  # TODO: Only temporary until database access works
    # find trends
    df = manipulation.calculate_moving_avg(df, 'residentSetSize')  #TODO: Get from database
    trend_list = trend.detect_trends(df, 'MovingAvg')
    # find anomalies
    anomaly_list = anomaly.detect_anomalies(df, 'residentSetSize')
    # get stats
    std = df['residentSetSize'].std()
    mean = df['residentSetSize'].mean()
    return df, anomaly_list, trend_list, std, mean


def fetch_pc_data(df, pc_total_df, column):  # fetch all application data in database for a certain time period
    df = queue_df  # TODO: Only temporary until database access works
    pc_total_df = manipulation.group_by_timestamp(df) #TODO: We can skip this if we get pc_total_data itself from database
    print(pc_total_df)
    # get influence percentage
    involvement_map = involvement.detect_involvement_percentual(df, pc_total_df, column)
    # find trends
    pc_total_df = manipulation.calculate_moving_avg(pc_total_df, column) #TODO: GET FROM DATABASE
    trend_list = trend.detect_trends(pc_total_df, 'MovingAvg')
    # get stats
    std = df[column].std()
    mean = df[column].mean()
    # get list of relevant data
    application_list = involvement.detect_relevancy(pc_total_df, df, column)
    # get allocation percentage
    df = df.set_index(['timestamp'])
    latest_row = df[df.index == df.index.max()]
    allocation_map = stats.calc_allocation(latest_row, column, application_list)
    # TODO: compare current value with last
    return pc_total_df, allocation_map, std, mean, trend_list, involvement_map
