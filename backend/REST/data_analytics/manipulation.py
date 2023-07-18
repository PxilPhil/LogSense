import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import datetime
import time
import os
import glob
import statsmodels.api as sm

df = pd.DataFrame()  # initial dataframe
selected_row = pd.DataFrame()  # grouped dataframe for application by timestamp
timestamp_df = pd.DataFrame()  # grouped dataframe by timestamp by sum


def preprocess_data(new_df):
    global df
    global timestamp_df
    df = new_df
    timestamp_df = df.groupby(['timestamp']).sum(numeric_only=True).sort_values('timestamp', ascending=True)


def select_rows_by_application(selected_value):  # Method to select rows by value
    global selected_row
    selected_row = df.loc[df.name == selected_value].groupby(['timestamp']).sum(numeric_only=True).sort_values(
        by=['timestamp'])


def calculate_moving_avg(rows, column):  # calculates moving avg for the column
    rows['MovingAvg'] = rows[column].rolling(
        window=5).mean()  # moving averages can be used to flatten
    return rows
