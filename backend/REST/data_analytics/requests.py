import glob
import os

import pandas as pd
import manipulation
import causality
import anomaly
from data_analytics.helper import read_csv


def ingest_process_data():
    df = read_csv(os.path.join("../data/processes", "*.csv"))
    print(df)
    timestamp_df = manipulation.preprocess_data(df)
    agg_df = manipulation.aggregate(df)
    causality_list= causality.detect_causality(timestamp_df, agg_df, df, 'residentSetSize')  # hardcoded to work for ram

    # looks for anomalies for the process contained in the map
    # anomaly detection does not work yet

    anomaly_map = dict()
    for application in causality_list:
        print('loop')
        print(application)
        selected_row = manipulation.select_rows_by_application(application, df)
        selected_row = manipulation.calculate_moving_avg(selected_row, 'residentSetSize')
        anomaly_map[application] = anomaly.detect_anomalies(selected_row, 'residentSetSize')

    for key, obj_list in anomaly_map.items():
        print("Key:", key)
        for obj in obj_list:
            print("Object timestamp:", obj.timestamp)
            print("Object anomalyType:", obj.is_event)

    return df, timestamp_df


def fetch_process_data():  # supposed to analyze trends and everything in detail for one certain application
    return 0


if __name__ == "__main__":
    ingest_process_data()
