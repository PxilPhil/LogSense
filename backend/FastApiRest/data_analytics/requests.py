import pandas as pd
import warnings
from data_analytics import involvement, manipulation, anomaly, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from db_access.data import get_moving_avg_of_application_ram
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")


def preprocess_pc_data(df):
    df = df.set_index('timestamp')
    anomaly_list = []
    pc_total_df = manipulation.group_by_timestamp(df)
    relevant_list = involvement.detect_relevancy(pc_total_df, df,
                                                 'residentSetSize')  # hardcoded to work for ram
    print(relevant_list)
    for application in relevant_list:
        selected_row = manipulation.select_rows_by_application(application, df)
        moving_avg = get_moving_avg_of_application_ram(1, application)
        if moving_avg > 0:
            last_entry_was_anomaly = False
            anomaly.detect_anomaly(selected_row, 'residentSetSize', moving_avg, last_entry_was_anomaly, anomaly_list,
                                   application)
    return pc_total_df, anomaly_list


def forecast_disk_space(df, days):  # predict disk space for the next x days
    # read dataframe, elect only needed columns
    df = df.filter(['measurement_time', 'free_disk_space'])
    df = df.set_index(pd.to_datetime(df['measurement_time']).astype('int64') // 10 ** 6)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df, 'free_disk_space')
    df = manipulation.create_df_between(timestamp, days, 'D')
    df = predict_for_df(LR, df)

    # convert timestamps to datetime
    df['datetime'] = pd.to_datetime(df.index, unit='ms')
    data_list = []
    for _, row in df.iterrows():
        data_list.append(ForecastData(**row.to_dict()))
    last_timestamp = None  # timestamp when free disk space reaches zero or below
    # find out if and when LinearRegression is less than 0 (free disk space running out)
    no_disk_space_rows = df[df['LinearRegression'] <= 0]
    if not no_disk_space_rows.empty:
        last_timestamp = no_disk_space_rows['datetime'].iloc[0]

    return data_list, last_timestamp


def analyze_application_data(df, application_name):  # supposed to analyze trends and everything in detail for one certain application
    # find anomalies
    anomaly_list = anomaly.detect_anomalies(df, 'ram', application_name)
    # get stats
    std = df['ram'].std()
    mean = df['ram'].mean()
    return df, anomaly_list, std, mean


def analyze_pc_data(df, pc_total_df, column):  # fetch all application data in database for a certain time period
    # get stats
    std = pc_total_df[column].std()
    mean = pc_total_df[column].mean()
    # get allocation percentage
    latest_total_value = pc_total_df.at[pc_total_df.index.max(), column]
    allocation_map = stats.calc_allocation(latest_total_value, column, df)
    allocation_list = [AllocationClass(name=key, allocation=value) for key, value in
                       allocation_map.items()]  # convert map into list of our model object to send via json
    # TODO: compare current value with last
    return pc_total_df, allocation_list, std, mean
