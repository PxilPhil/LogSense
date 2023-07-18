import pandas as pd
import os
import glob
import manipulation

path = os.getcwd()
csv_files = glob.glob(os.path.join(path + "/data/processes", "*.csv"))

df = pd.DataFrame()

for file in csv_files:
    new_df = pd.read_csv(file)
    df = pd.concat([df, new_df])

manipulation.preprocess_data(df)
