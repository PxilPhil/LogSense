
from model.data import AnomalyData
from scipy import stats

z_limit = 2

def detect_anomalies(df, column):
    anomaly_list = []
    df['zscore'] = stats.zscore(df[column])
    anomaly_df = df.loc[stats.zscore(df[column]) > z_limit]
    detect_anomalies_via_score(anomaly_list, anomaly_df, column)

    return anomaly_list


def detect_anomalies_via_score(anomaly_list, anomaly_df, column):
    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']),
                                   application=row['name'],
                                   column=column)
        anomaly_list.append(anomaly_data)
