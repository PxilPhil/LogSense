import glob
import os

import pandas as pd
import manipulation
import causality
import anomaly


def read_csv():  # helper method for testing
    csv_files = glob.glob(os.path.join("../data/processes", "*.csv"))

    df = pd.DataFrame()

    for file in csv_files:
        new_df = pd.read_csv(file)
        df = pd.concat([df, new_df])
    return df


def ingest_process_data():
    # do drop na for safety reasons and exception handling
    df = read_csv()
    df = df.dropna()
    print(df)

    timestamp_df = manipulation.preprocess_data(df)
    agg_df = manipulation.aggregate(df)
    causality_list = causality.detect_causality(timestamp_df, agg_df, df,
                                                'residentSetSize')  # hardcoded to work for ram

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


def fetch_process_data():  # supposed to analyze trends and everything in detail for one certain application
    return 0


if __name__ == "__main__":
    ingest_process_data()
