from pandas import DataFrame

from model.data import StatisticData


def calc_allocation(latest_total_value, column, df):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    for index, row in df.iterrows():
        allocation_map[row['name']] = row[column] / latest_total_value
    return allocation_map


def calculate_trend_statistics(df: DataFrame, column: str, name: str) -> StatisticData:
    """
    Calculates statistics for the trend of a graph like:
    Median
    Average
    Standard Deviation
    Coefficient of Variation => Stability

    :return:
    """

    # calculate the stability of data
    std = df[column].std()
    mean = df[column].mean()
    cov = (std / mean) * 100  # stands for coefficient_of_variation

    # calculate changes that occurred from start to end
    recent_row = df.loc[df['measurement_time'].idxmax()]
    oldest_row = df.loc[df['measurement_time'].idxmin()]
    change = ((recent_row[column] - oldest_row[column]) / oldest_row[column]) * 100
    delta = recent_row[column] - oldest_row[column]

    stability = f"Stability: {determine_stability(cov)}\n"
    message = create_statistics_message(change, delta, name)

    statistic_data = StatisticData(
        average=df[column].mean(),
        current=recent_row[column],
        stability=stability,
        message=message
    )
    return statistic_data


def create_statistics_message(change, delta, name: str):
    # this is a method to make a message displayed to the user when requesting statistical values
    message = f"{name} Usage has changed by {round(change, 2)} % ({round(delta, 2)})\n"
    return message

def append_statistics_message(message, event_amount, anomaly_amount, data_amount):
    message += f"{event_amount} Events detected \n {anomaly_amount} Anomalies detected \n"
    message += f"{data_amount} Datapoints fetched \n"
    return message

def determine_stability(cov):  # common rule of thumb is that cv < 15% is considered stable and < 30% medium
    if cov < 15:
        return 'High'
    elif cov < 30:
        return 'Medium'
    return 'Low'
