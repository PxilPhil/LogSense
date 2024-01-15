import warnings

from pandas import DataFrame

from data_analytics.util import manipulation, stats
from data_analytics.util.change_anomaly_detection import get_event_measurement_times, detect_anomalies
from data_analytics.justification import justify_pc_data_points, justify_application_df
from data_analytics.util.stats import calculate_trend_statistics, append_statistics_message, determine_event_ranges
from db_access.pc import get_ram_time_series_limited
from model.data import AllocationClass

warnings.filterwarnings("ignore")


# todo: our current approach doing on request is pretty stupid, please change it

def preprocess_pc_data(df: DataFrame):
    """
    Preprocesses and groups data before inserting it into the database.

    Features:
        - Grouping the DataFrame by timestamp to create the total pc DataFrame.

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


def analyze_application_data(df, application_name):
    """
    Analyzes application data fetched by a client.

    Features:
        - Anomaly detection.
        - Change point detection
        - Simple statistical math (standard deviation, mean, median).
        - Calculate stability and trend statistics
        - Justifications for why changes or anomalies have occurred


    Args:
        df (DataFrame): The DataFrame containing application data.
        application_name (str): The name of the application.

    Returns:
        df: The DataFrame containing application data.
        ram_events_and_anomalies: The list of detected change points and anomalies for ram
        cpu_events_and_anomalies: The list of detected change points and anomalies for cpu
        statistic_data: Simple statistical data like mean, average, median, trend stats
    """
    # in order to prevent underfitting, we need to fetch more data if we have too little

    # detect changes or events
    ram_change_points = get_event_measurement_times(df, df,
                                                    'ram', 3)  # only do it for ram since it makes no sense to do it for cpu

    # find anomalies
    anomalies_ram = detect_anomalies(df, df, 'ram')
    anomalies_cpu = detect_anomalies(df, df, 'cpu')

    # get justifications for events and anomalies
    ram_anomaly_justifications = justify_application_df(df, anomalies_ram, application_name, None, True)
    ram_event_justifications = justify_application_df(df, ram_change_points, application_name, ram_anomaly_justifications,False)
    ram_events_and_anomalies = ram_anomaly_justifications + ram_event_justifications

    cpu_events_and_anomalies = justify_application_df(df, anomalies_cpu, application_name, None,
                                                      False)

    # get stats
    statistic_data_ram = calculate_trend_statistics(df, 'ram', 'RAM')
    statistic_data_ram.message = append_statistics_message(statistic_data_ram.message, len(ram_change_points), len(anomalies_ram), len(df))
    statistic_data_cpu = calculate_trend_statistics(df, 'cpu', 'CPU')
    statistic_data_cpu.message = append_statistics_message(statistic_data_cpu.message, len(anomalies_cpu), len(anomalies_cpu), len(df))

    # determine event anomaly ranges and save statistics of them in justifications
    determine_event_ranges(df, ram_events_and_anomalies, 'ram')
    determine_event_ranges(df, cpu_events_and_anomalies, 'cpu')

    return df, ram_events_and_anomalies, cpu_events_and_anomalies, statistic_data_ram, statistic_data_cpu


def analyze_pc_data(pc_id: int, df, pc_total_df, name: str):
    """
    Analyzes pc data, called by the client when fetching pc data of a certain category (like RAM).

    Features:
        - Anomaly detection.
        - Application allocation calculation
        - Change point detection
        - Simple statistical math (standard deviation, mean, median).
        - Calculate stability and trend statistics
        - Justifications for why changes or anomalies have occurred


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
        :param pc_id:

    """
    if name == 'ram':
        latest_total_ram = pc_total_df.at[pc_total_df.index.max(), 'value']
        allocation_map = stats.calc_allocation(latest_total_ram, name, df)
        allocation_list = [AllocationClass(name=key, allocation=value) for key, value in
                           allocation_map.items()]  # convert map into list of our model object to send via json
    elif name == 'cpu':  # get allocation percentage for cpu, no calculation needed
        allocation_list = []
        for index, row in df.iterrows():
            allocation_instance = AllocationClass(name=row['name'], allocation=row[name])
            allocation_list.append(allocation_instance)

    # sort allocations by impact
    allocation_list = sorted(allocation_list, key=lambda ram: ram.allocation, reverse=True)

    anomaly_measurements = []
    change_points = []
    training_df = pc_total_df  # dataframe used to train the models

    # fetch more data if needed to avoid underfittng
    if len(df.index) < 50:  # arbitrary value used
        training_df, extended_list = get_ram_time_series_limited(pc_id, 100)

    # detect anomalies
    anomaly_measurements = detect_anomalies(pc_total_df, training_df, 'value')

    # detect changes / events
    change_points = get_event_measurement_times(pc_total_df, training_df, 'value', 3)

    # justifies events and anomalies
    anomalies = justify_pc_data_points(pc_total_df, anomaly_measurements, None, 1, True)
    events = justify_pc_data_points(pc_total_df, change_points, anomalies, 1, False)
    events_and_anomalies = anomalies+events



    # get stats
    statistic_data = calculate_trend_statistics(pc_total_df, 'value', name)
    statistic_data.message = append_statistics_message(statistic_data.message, len(change_points), len(anomaly_measurements), len(pc_total_df))

    determine_event_ranges(pc_total_df, events_and_anomalies, 'value')

    return pc_total_df, allocation_list, events_and_anomalies, statistic_data

