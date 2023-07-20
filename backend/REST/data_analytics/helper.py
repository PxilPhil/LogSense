import glob
import pandas as pd

def read_csv(file):  # helper method for testing
    csv_files = glob.glob(file)

    df = pd.DataFrame()

    for file in csv_files:
        new_df = pd.read_csv(file)
        df = pd.concat([df, new_df])
    return df