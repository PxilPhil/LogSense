import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression

from data_analytics.util import manipulation
from data_analytics.util.change_anomaly_detection import detect_events
from model.pc import ForecastData

def forecast_disk_space(df, column, start, end, bucket_value):
    """
    Forecasts disk space allocation between a start and end date with a bucket_value.

    Args:
        prediction_df (DataFrame): The DataFrame containing free disk space values.
        column (str): The column in the DataFrame to be used for forecasting.
        start (str): The start date in the format 'YYYY-MM-DD HH:MM:SS'.
        end (str): The end date in the format 'YYYY-MM-DD HH:MM:SS'.
        bucket_value (str): The frequency for prediction (e.g., '1Min' for 1 minute, '5Min' for 5 minutes).

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """

    # Convert start and end dates to datetime objects
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # Create a DataFrame with the specified frequency (bucket_value) between start and end dates
    date_range = pd.date_range(start=start_date, end=end_date, freq=bucket_value)
    prediction_df = pd.DataFrame({'datetime': date_range})
    prediction_df['measurement_time'] = prediction_df['datetime'].astype('int64') // 10 ** 6

    # Fit the linear regression model using the existing data
    LR = fit_linear_regression(df, column)

    # Predict values for the created DataFrame
    prediction_df = predict_for_df(LR, prediction_df, column)

    data_list = []
    for _, row in prediction_df.iterrows():
        data_list.append(ForecastData(**row.to_dict()))

    last_timestamp = None  # timestamp when free disk space reaches zero or below
    # Find out if and when Linear Regression is less than or equal to 0 (free disk space running out)
    no_disk_space_rows = prediction_df[prediction_df[column] <= 0]
    if not no_disk_space_rows.empty:
        last_timestamp = no_disk_space_rows['datetime'].iloc[0]

    return data_list, last_timestamp


def determine_full_disk_space(df: DataFrame, column: str, max_days):
    """
    Forecasts disk space allocation for a certain number of days.

    Features:
    - Training a linear regression model by existing disk space data.
    - Building a new DataFrame to be filled with data by the linear regression model later on.
    - Filling the DataFrame with prediction values.
    - Finding out when free disk space will run out and save the timestamp into "last_timestamp".

    Args:
        df (DataFrame): The DataFrame containing free disk space values.
        max_days (int): The number of days data should be forecasted for.

    Returns:
        data_list: A list of forecasted free disk space values with a timestamp.
        last_timestamp: The timestamp where free disk space reaches 0 or less.
    """

    last_timestamp = None  # timestamp when free disk space reaches zero or below
    total_days = 0
    current_days = 10
    data_list = []

    events = detect_events(df, column, 10)
    drop_indices = df.index[df.index <= events[-2]]
    df = df.drop(index=drop_indices)

    df = df.filter(['measurement_time', column])
    df = df.set_index(pd.to_datetime(df['measurement_time']).astype('int64') // 10 ** 6)
    # get latest timestamp, fit to model, extend dataframe by time input and predict values for it
    timestamp = df.index[-1]
    LR = fit_linear_regression(df, column)

    while last_timestamp is None and total_days < max_days:
        prediction_df = manipulation.create_df_between(timestamp, current_days, 'D')
        prediction_df = predict_for_df(LR, prediction_df)

        # convert timestamps to datetime
        prediction_df['datetime'] = pd.to_datetime(prediction_df.index, unit='ms')
        # find out if and when LinearRegression is less than 0 (free disk space running out)
        no_disk_space_rows = prediction_df[prediction_df['LinearRegression'] <= 0]
        total_days = total_days + current_days

        for _, row in prediction_df.iterrows():
            data_list.append(ForecastData(**row.to_dict()))

        if not no_disk_space_rows.empty:
            last_timestamp = no_disk_space_rows['datetime'].iloc[0]
        else:
            timestamp = int((pd.Timestamp(prediction_df['datetime'].iloc[-1]) + pd.DateOffset(days=1)).timestamp() * 1000)

    return data_list, last_timestamp

def fit_linear_regression(df, column):
    LR = LinearRegression()
    LR.fit(df.index.values.reshape(-1, 1), df[column].values)
    return LR


def predict_for_df(LR, df):
    prediction = LR.predict(df.index.values.reshape(-1, 1))
    df['LinearRegression'] = prediction
    return df
