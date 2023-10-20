from data_analytics.manipulation import convert_column_to_list
from model.data import AnomalyData
from scipy import stats

z_limit = 1.5

"""
    We assume a normal distribution of data for our anomaly detection
    This approach seems to work really well for detecting cpu events as well
"""


def detect_anomalies(df, column):
    df['zscore'] = stats.zscore(df[column])
    anomaly_df = df.loc[stats.zscore(df[column]) > z_limit]
    print('anomaly_df')
    return anomaly_df['measurement_time'].tolist()