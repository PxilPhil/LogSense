import glob
import os
import queue
import pandas as pd
import causality
import manipulation
import anomaly
import warnings
import trend
from prediction import fit_linear_regression, predict_for_df
from data_analytics.helper import read_csv, calc_end_timestamp

warnings.filterwarnings("ignore")
first_ts = 0

prev_df = pd.DataFrame()  # previous dataframes of the last x minutes
current_df = pd.DataFrame()  # current dataframes of the last x minutes


def ingest_loop():
    csv_files = glob.glob(os.path.join("../data/processes", "*.csv"))

    for file in csv_files:
        new_df = pd.read_csv(file)
        ingest_process_data(new_df)


def ingest_process_data(new_df):
    # Idea behind the queue system is to concat a dataframe, keep 5 previous for analyzing things and 5 to be
    # analyzed (current) prev value is always needed when we are working with moving averages, otherwise not required
    global current_df
    global prev_df

    new_df = new_df.set_index('timestamp')
    current_df = pd.concat([current_df, new_df])

    if current_df.index.nunique() > 4 and prev_df.empty:  # don't do anything yet untiil we have saved previous values
        prev_df = current_df
        current_df = pd.DataFrame()
    elif current_df.index.nunique() > 4:  # only do something once we have both previous and current valuees
        timestamp_df = manipulation.group_by_timestamp(current_df)
        causality_list = causality.detect_relevancy(timestamp_df, current_df,
                                                    'residentSetSize')  # hardcoded to work for ram

        anomaly_map = dict()
        for application in causality_list:
            #  here concat prev and curr
            df = pd.concat([prev_df, current_df])
            selected_row = manipulation.select_rows_by_application(application, df)
            selected_row = manipulation.calculate_moving_avg(selected_row, 'residentSetSize')
            anomaly_list = anomaly.detect_anomalies(selected_row, 'residentSetSize')
            if len(anomaly_list) > 0:
                anomaly_map[application] = anomaly_list

        prev_df = current_df
        current_df = pd.DataFrame()
        return anomaly_map


def predict_resource_data():
    # read dataframe, remove nans, select only needed columns
    df = read_csv(os.path.join("../data/ressources", "*.csv"), True)
    df = df.dropna()
    df = df.filter(['timestamp', 'freeDiskSpace'])
    df = df.set_index('timestamp')
    print(df)

    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df)
    df = df.drop(columns=['freeDiskSpace'])  # don't need it anymore (except if we want to know accuracy)
    df = pd.concat([df, manipulation.create_df_between(timestamp, calc_end_timestamp(timestamp=timestamp, hours=60),
                                                       'T')])  # predict next hours in minute intervals
    df = predict_for_df(LR, df)
    print(df)
    return df


def fetch_application_data(name):  # supposed to analyze trends and everything in detail for one certain application
    df = read_csv(os.path.join("../data/processes", "*.csv"), False)
    df = manipulation.select_rows_by_application(name, df)
    print(df)
    # find trends
    df = manipulation.calculate_moving_avg(df, 'residentSetSize')
    trend_list = trend.detect_trends(df, 'MovingAvg')
    for entry in trend_list:
        print("trend prev_value:", entry.prev_value)
        print("trend curr_value:", entry.curr_value)
        print("trend change:", entry.change)
    # find anomalies
    anomaly_list = anomaly.detect_anomalies(df, 'residentSetSize')
    return anomaly_list


def fetch_process_trends():  # supposed get trends
    df = read_csv(os.path.join("../data/processes", "*.csv"), False)
    df = manipulation.group_by_timestamp(df)
    print(df)
    # find trends
    df = manipulation.calculate_moving_avg(df, 'residentSetSize')
    trend_list = trend.detect_trends(df, 'MovingAvg')
    return trend_list


if __name__ == "__main__":
    ingest_loop()
