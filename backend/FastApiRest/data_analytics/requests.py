import pandas as pd
import warnings
from data_analytics import involvement, manipulation, alerts, trend, stats
from data_analytics.prediction import fit_linear_regression, predict_for_df
from db_access.data import get_moving_avg_of_application
from db_access.pc import get_latest_moving_avg
from db_access.helper import get_pcid_by_stateid
from model.data import AllocationClass
from model.pc import ForecastData

warnings.filterwarnings("ignore")


def preprocess_pc_data(df, state_id):
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
    # check for custom alerts
    # TODO: Get custom alerts here or before
    custom_conditions = []  # list of conditions of a custom alerts
    alerts.check_custom_alerts(df, pc_total_df, custom_conditions)
    # find out if event has occured in pc_total_df
    pc_id = get_pcid_by_stateid(state_id)
    moving_avg_ram, moving_avg_cpu = get_latest_moving_avg(pc_id)
    if alerts.has_event_occurred(pc_total_df, moving_avg_ram, moving_avg_cpu):
        relevant_list = involvement.detect_relevancy(pc_total_df, df)
        for application in relevant_list:
            # TODO: We are working with percentual changes with moving averages, should we change that?
            selected_row = manipulation.select_rows_by_application(application, df)
            moving_avg_ram, moving_avg_cpu = get_moving_avg_of_application(pc_id, application)
            if moving_avg_ram > 0 and moving_avg_cpu > 0:
                alerts.detect_ram_event(selected_row, 'residentSetSize', moving_avg_ram, event_list,
                                        application)  # find ram events
                alerts.detect_cpu_event(selected_row, 'cpuUsage', moving_avg_cpu, event_list,
                                        application)  # find cpu events

    # if an event has been found, look through what application caused it
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
    event_list = alerts.detect_multiple_events(df, application_name)
    # get stats
    std_ram = df['ram'].std()
    mean_ram = df['ram'].mean()
    std_cpu = df['cpu'].std()
    mean_cpu = df['cpu'].mean()
    # find anomalies
    anomaly_list = alerts.detect_anomalies(df, 'cpu', 'ram')
    return df, event_list, anomaly_list, std_ram, std_cpu, mean_ram, mean_cpu


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
    std_ram = df['ram'].std()
    mean_ram = df['ram'].mean()
    std_cpu = df['cpu'].std()
    mean_cpu = df['cpu'].mean()
    # get allocation percentage for ram
    latest_total_value = pc_total_df.at[pc_total_df.index.max(), 'ram']
    allocation_map_ram = stats.calc_allocation(latest_total_value, 'ram', df)
    allocation_list_ram = [AllocationClass(name=key, allocation=value) for key, value in
                           allocation_map_ram.items()]  # convert map into list of our model object to send via json

    # get allocation percentage for cpu, no calculation needed
    allocation_list_cpu = []
    for index, row in df.iterrows():
        allocation_instance = AllocationClass(name=row['name'], allocation=row['cpu'])
        allocation_list_cpu.append(allocation_instance)

    anomaly_list = alerts.detect_anomalies(df, 'cpu', 'ram')
    return pc_total_df, anomaly_list, allocation_list_ram, allocation_list_cpu, std_ram, mean_ram, std_cpu, mean_cpu


def analyze_trends():
    """
    Analyzes application & pc trends, in order for that it groups data sets by date intervals
    :return:
    """
