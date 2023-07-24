import glob
import pandas as pd
from datetime import datetime, timedelta


def read_csv(file, custom):  # helper method for testing
    csv_files = glob.glob(file)

    df = pd.DataFrame()

    if custom == True:
        for file in csv_files:
            new_df = pd.read_csv(file, sep='|', engine='python')
            df = pd.concat([df, new_df])
    else:
        for file in csv_files:
            new_df = pd.read_csv(file)
            df = pd.concat([df, new_df])
    return df


def calc_end_timestamp(timestamp,
                       hours):  # helper method to calculate the last timestamp going from a starting timestamp
    # and a time period
    time_delta = timedelta(hours=hours)
    end_date_time = datetime.fromtimestamp(timestamp / 1000) + time_delta
    end_timestamp = int(end_date_time.timestamp() * 1000)
    return end_timestamp
