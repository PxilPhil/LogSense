import glob
import os
import queue
import pandas as pd
import manipulation
import causality
import anomaly
import warnings
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
    # Idea behind the queue system is to concat a dataframe, keep 5 previous for analyzing things and 5 to be analyzed (current)
    # prev value is always needed when we are working with moving averages, otherwise they are not required

    # TODO: Nan Values still persists in some cases
    global current_df
    global prev_df

    new_df = new_df.set_index('timestamp')
    current_df = pd.concat([current_df, new_df])

    if current_df.index.nunique() > 4 and prev_df.empty:  # don't do anything yet untiil we have saved previous values
        print('waiting')
        prev_df = current_df
        current_df = pd.DataFrame()
    elif current_df.index.nunique() > 4:  # only do something once we have both previous and current valuees
        print('loop')
        timestamp_df = manipulation.preprocess_data(current_df)
        agg_df = manipulation.aggregate(current_df)
        causality_list = causality.detect_causality(timestamp_df, agg_df, current_df,
                                                    'residentSetSize')  # hardcoded to work for ram

        # causalitiy is never detected
        print('loop 2')
        anomaly_map = dict()
        for application in causality_list:
            print('application')
            print(application)
            #  here concat prev and curr
            df = pd.concat([prev_df, current_df])
            selected_row = manipulation.select_rows_by_application(application, df)
            selected_row = manipulation.calculate_moving_avg(selected_row, 'residentSetSize')
            anomaly_map[application] = anomaly.detect_anomalies(selected_row, 'residentSetSize')

        # TODO: remove later since it is only for output
        for key, obj_list in anomaly_map.items():
            print("Key:", key)
            for obj in obj_list:
                print("Object timestamp:", obj.timestamp)
                print("Object anomalyType:", obj.is_event)
        prev_df = current_df
        current_df = pd.DataFrame()


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


def fetch_process_data(name):  # supposed to analyze trends and everything in detail for one certain application
    # TODO: fetch data from database
    # TODO: run algorithms on it
    return 0


if __name__ == "__main__":
    ingest_loop()
