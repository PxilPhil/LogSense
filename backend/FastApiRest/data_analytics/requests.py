import pandas as pd
import warnings

from pandas import DataFrame

from data_analytics import involvement, manipulation, custom_alerts, stats
from data_analytics.anomaly_detection import detect_anomalies
from data_analytics.change_detection import get_event_measurement_times, detect_events
from data_analytics.forecasting import fit_linear_regression, predict_for_df
from data_analytics.justification import justify_pc_data_points, justify_application_data_points
from db_access.data import get_moving_avg_of_application
from db_access.pc import get_latest_moving_avg
from db_access.helper import get_pcid_by_stateid
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")

"""
    Documentation Comments:
    Events:
    Rework event detection to make threshold dependent on things like variance
    Formula for threshold: mean + (multiplier * std_dev)
    Alternatives to percentual detection include online/offline change point detection algorithms (ChangeFinder/Ruptures)
    
    Predictions:
    If possible save a trained model
    Use exponential smoothing( Holt-Winters?), might be possible to use more powerful models than linear regression
    -> Random Forest, Keep linear regression with Piecewise Linear Regression or time bucketing
    
    Anomalies:
    We just assume a normal distribution of data
    
    Any other things we could implement?
"""


def preprocess_pc_data(df: DataFrame, state_id: int):
    """
    Preprocesses and analyzes data before inserting it into the database.

    Features:
        - Grouping the DataFrame by timestamp to create the total pc DataFrame.
        - Detecting if an event has occured or not
        - Find relevant applications to find out if events have occured in them
        - Detecting events of relevant applications.

    Args:
        df (DataFrame): The DataFrame containing pc data to be inserted.

    Returns:
        pc_total_df: The total pc DataFrame grouped by timestamp.
        event_list: A list of detected events.
    """
    df = df.set_index('timestamp')
    event_list = []
    pc_total_df = manipulation.group_by_timestamp(df)
    return pc_total_df, event_list


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
        event_list: The list of detected events
        anomaly_list: The list of detected anomalies.
        std: Standard deviation from mean, used for calculating "Stability".
        mean: Average of the values.
    """
    # find events
    ram_event_points = detect_events(df, 'ram')
    # get stats
    std_ram = df['ram'].std()
    mean_ram = df['ram'].mean()
    std_cpu = df['cpu'].std()
    mean_cpu = df['cpu'].mean()
    # find anomalies
    #TODO: Implement new anomaly and event justification like for pc data
    #TODO: On Insert we get duplicate data (why????)
    anomaly_measurements_ram = detect_anomalies(df, 'ram')
    anomaly_measurements_cpu = detect_anomalies(df, 'cpu')

    ram_events = justify_application_data_points(df, ram_event_points, application_name)
    cpu_events = []
    print(ram_events)

    return df, ram_events, cpu_events, anomaly_measurements_ram, anomaly_measurements_cpu, std_ram, std_cpu, mean_ram, mean_cpu



def analyze_pc_data(df, pc_total_df):
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
        anomaly_list: The list of detected anomalies
        allocation_list: The list of allocations (which application makes up how much percent of RAM/CPU usage).
        std: Standard deviation from mean, used for calculating "Stability".
        mean: Average of the values.
    """
    # get stats
    std_ram = pc_total_df['ram'].std()
    mean_ram = pc_total_df['ram'].mean()
    std_cpu = pc_total_df['cpu'].std()
    mean_cpu = pc_total_df['cpu'].mean()
    # get allocation percentage for ram
    latest_total_ram = pc_total_df.at[pc_total_df.index.max(), 'ram']
    allocation_map_ram = stats.calc_allocation(latest_total_ram, 'ram', df)
    allocation_list_ram = [AllocationClass(name=key, allocation=value) for key, value in
                           allocation_map_ram.items()]  # convert map into list of our model object to send via json

    # get allocation percentage for cpu, no calculation needed
    allocation_list_cpu = []
    for index, row in df.iterrows():
        allocation_instance = AllocationClass(name=row['name'], allocation=row['cpu'])
        allocation_list_cpu.append(allocation_instance)

    # detect anomalies
    anomaly_measurements_ram = detect_anomalies(pc_total_df, 'ram')
    anomaly_measurements_cpu = detect_anomalies(pc_total_df, 'cpu')

    # detect changes / events
    ram_change_points = get_event_measurement_times(pc_total_df, 'ram')

    # explain changes (events) and anomalies with EventLogs
    ram_events = justify_pc_data_points(pc_total_df, ram_change_points, 1)  # TODO: change pc_id
    cpu_events = justify_pc_data_points(pc_total_df, anomaly_measurements_cpu, 1)  # TODO: change pc_id
    ram_anomalies = justify_pc_data_points(pc_total_df, anomaly_measurements_ram, 1)  # TODO: change pc_id
    cpu_anomalies = cpu_events  # cpu events are the same as cpu anomalies

    return pc_total_df, allocation_list_ram, allocation_list_cpu, std_ram, mean_ram, std_cpu, mean_cpu, ram_events, cpu_events, ram_anomalies, cpu_anomalies


def analyze_trends():
    """
    Analyzes application & pc trends, in order for that it groups data sets by date intervals
    :return:
    """
