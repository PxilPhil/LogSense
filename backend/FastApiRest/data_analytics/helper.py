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
