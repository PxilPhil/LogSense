from pandas import DataFrame

from data_analytics.manipulation import determine_stability
from model.data import StatisticData


def calc_allocation(latest_total_value, column, df):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    for index, row in df.iterrows():
        allocation_map[row['name']] = row[column] / latest_total_value
    return allocation_map


def calculate_trend_statistics(df: DataFrame) -> StatisticData:
    """
    Calculates statistics for the trend of a graph like:
    Median
    Average
    Standard Deviation
    Coefficient of Variation => Stability

    :return:
    """

    # calculate the stability of data
    std_ram = df['ram'].std()
    mean_ram = df['ram'].mean()
    std_cpu = df['cpu'].std()
    mean_cpu = df['cpu'].mean()
    cov_ram = (std_ram / mean_ram) * 100  # stands for coefficient_of_variation
    cov_cpu = (std_cpu / mean_cpu) * 100  # stands for coefficient_of_variation

    # calculate changes that occurred for ram and cpu data from the start to end
    max_time_row = df[df['measurement_time'] == df['measurement_time'].max()]
    min_time_row = df[df['measurement_time'] == df['measurement_time'].min()]
    ram_ratio = max_time_row['ram'].values[0] / min_time_row['ram'].values[0]
    cpu_ratio = max_time_row['cpu'].values[0] / min_time_row['cpu'].values[0]
    ram_delta = max_time_row['ram'].values[0] - min_time_row['ram'].values[0]
    cpu_delta = max_time_row['cpu'].values[0] - min_time_row['cpu'].values[0]

    stability = f"RAM Stability: {determine_stability(cov_ram)}\n CPU Stability: {determine_stability(cov_ram)}\n"
    message = create_statistics_message(ram_ratio, ram_delta, cpu_ratio, cpu_delta)

    statistic_data = StatisticData(
        average_ram = df['ram'].mean(),
        median_ram = df['ram'].median(),
        average_cpu = df['cpu'].mean(),
        median_cpu = df['cpu'].median(),
        stability=stability,
        message=message

    )
    return statistic_data


def create_statistics_message(ram_ratio, ram_delta, cpu_ratio, cpu_delta):
    # this is a method to make a message displayed to the user when requesting statistical values
    message = ""
    if ram_ratio and ram_delta:
        message += f"RAM has changed by {ram_ratio} ({ram_delta})"
    if cpu_ratio and cpu_delta:
        message += f"CPU has changed by {cpu_ratio} ({cpu_delta})"
    return message