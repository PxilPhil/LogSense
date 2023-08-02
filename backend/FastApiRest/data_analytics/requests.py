import pandas as pd
import warnings
from data_analytics import involvement, manipulation, anomaly, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from db_access.data import get_moving_avg_of_application_ram
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")

"""
Some more ideas:

Threshold Analysis:
Check if applications or pcs are at a certain threshold for some time (like always using a large amount of RAM and CPU)

Anomaly Detection:
Z-Scale test for certain timeframe
Moving Avg of a larger window size (timeframe)

CPU Analysis:
Like for RAM

Application Performance Trends: -> doing this rn
You can analyze the performance trends of applications over time. For example, you can calculate the average RAM or CPU usage of each application per day/week/month and plot it to observe any trends or patterns.

Comparing Applications:
You can compare the performance of different applications based on their RAM or CPU usage. Calculate statistics like mean and standard deviation for each application and compare them to identify which applications are more resource-intensive.
Resource Usage Over Time:

Explore the correlation between RAM and CPU usage. You can calculate the correlation coefficient between these two metrics to see if there's any relationship between them.
Outlier Detection:

Data Aggregation and Filtering: -> Done
Implement functions to aggregate data at different time intervals (e.g., hourly, daily) or filter data based on certain criteria (e.g., applications with high resource usage).

Resource Allocation Optimization:
You can use optimization techniques to recommend an optimal allocation of resources to different applications based on their historical usage patterns.

Version Comparision for Devs for example
"""


def preprocess_pc_data(df):
    """
    Preprocesses data before inserting it into the database.

    Features:
        - Grouping the DataFrame by timestamp to create the total pc DataFrame.
        - Detecting the relevancy of applications to analyze only those with great influence.
        - Detecting events of relevant applications.

    Args:
        df (DataFrame): The DataFrame containing pc data to be inserted.

    Returns:
        pc_total_df: The total pc DataFrame grouped by timestamp.
        anomaly_list: A list of detected anomalies.
    """
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


def forecast_disk_space(df, days):
    """
    Forecasts disk space allocation for a certain number of days.

    Features:
    - Training a linear regression model by existing disk space data.
    - Building a new DataFrame to be filled with data by the linear regression model later on.
    - Filling the DataFrame with prediction values.
    - Finding out when free disk space will run out and save the timestamp into "last_timestamp".

    Args:
        df (DataFrame): The DataFrame containing free disk space values.
        days (int): The number of days data should be forecasted for.

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """
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


def analyze_application_data(df, application_name):
    """
    Analyzes application data fetched by a client.

    Features:
        - Anomaly detection.
        - Simple statistical math (standard deviation, mean).

    Args:
        df (DataFrame): The DataFrame containing application data.
        application_name (str): The name of the application.

    Returns:
        df: The DataFrame containing application data.
        anomaly_list: The list of detected anomalies.
        std: Standard deviation from mean, used for calculating "Stability".
        mean: Average of the values.
    """
    # find anomalies
    anomaly_list = anomaly.detect_anomalies(df, 'ram', application_name)
    # get stats
    std = df['ram'].std()
    mean = df['ram'].mean()
    return df, anomaly_list, std, mean


def analyze_pc_data(df, pc_total_df, column):
    """
    Analyzes pc data, called by the client when fetching pc data of a certain category (like RAM).

    Features:
        - Calculating allocation of applications.
        - Simple statistical math (standard deviation, mean).

    Args:
        df (DataFrame): The DataFrame containing application data.
        pc_total_df (DataFrame): The DataFrame containing total pc data.
        column (str): Column which should be analyzed like RAM (deprecated).

    Returns:
        pc_total_df: The DataFrame containing total pc data.
        allocation_list: The list of allocations (which application makes up how much percent of RAM/CPU usage).
        std: Standard deviation from mean, used for calculating "Stability".
        mean: Average of the values.
    """
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

def analyze_trends():
    """
    Analyzes application & pc trends, in order for that it groups data sets by date intervals
    :return:
    """



