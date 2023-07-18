import pandas as pd

df = pd.DataFrame()  # initial dataframe


def preprocess_data(new_df):
    global df
    df = new_df
    return df.groupby(['timestamp']).sum(numeric_only=True).sort_values('timestamp', ascending=True)


def select_rows_by_application(selected_value):  # Method to select rows by value
    return df.loc[df.name == selected_value].groupby(['timestamp']).sum(numeric_only=True).sort_values(
        by=['timestamp'])


def calculate_moving_avg(rows, column):  # calculates moving avg for the column
    rows['MovingAvg'] = rows[column].rolling(
        window=5).mean()  # moving averages can be used to flatten
    return rows


def aggregate():
    return df.groupby("name").agg(list)
