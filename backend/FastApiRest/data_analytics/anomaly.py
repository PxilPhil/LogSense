from model.data import EventData
from model.data import AnomalyData
from scipy import stats
from datetime import datetime

event_sensitivity = 0.1
z_limit = 3


def detect_event(selected_row, column, moving_avg, previous_anomaly, anomaly_list, application):
    percentual_change = selected_row[column].values[0] / moving_avg
    event_header = selected_row['processCountDifference'].values[0]
    if (not previous_anomaly) and (abs(percentual_change - 1) > event_sensitivity):
        if event_header != 0:
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=1, change=percentual_change,
                                   application=application, column=column)
            anomaly_list.append(event_data)
        else:
            event_data = EventData(timestamp=selected_row.index.values[0], anomaly_type=2, change=percentual_change,
                                   application=application, column=column)
            anomaly_list.append(event_data)


def detect_multiple_events(selected_row, column, application_name):
    event_list = []
    selected_row['percentage_change'] = selected_row[column] / selected_row['rolling_avg_ram'].shift()
    selected_row = selected_row.dropna()
    previous_was_flagged = False
    for index, row in selected_row.iterrows():
        percentual_change = row['percentage_change']
        event_header = row['process_count_difference']

        if abs(percentual_change - 1) > event_sensitivity:
            if (percentual_change > 1 and event_header > 1) or (percentual_change < 1 and event_header < 1):
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=1, change=percentual_change,
                                       application=application_name, column=column)
                event_list.append(event_data)
            elif not previous_was_flagged:
                event_data = EventData(timestamp=row['measurement_time'], anomaly_type=2, change=percentual_change,
                                       application=application_name, column=column)
                event_list.append(event_data)
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return event_list


def detect_anomalies(df, first_column, second_column):
    anomaly_list = []
    # Calculate Z-Score for first column
    df['zscore'] = stats.zscore(df[first_column])
    anomaly_df = df.loc[stats.zscore(df[first_column]) > z_limit]

    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']), application=row['name'],
                                   column=first_column)
        anomaly_list.append(anomaly_data)

    # Calculate Z-Score for second column
    df['zscore'] = stats.zscore(df[second_column])
    anomaly_df = df.loc[stats.zscore(df[second_column]) > z_limit]

    for index, row in anomaly_df.iterrows():
        anomaly_data = AnomalyData(timestamp=row['measurement_time'], severity=int(row['zscore']), application=row['name'],
                                   column=second_column)
        anomaly_list.append(anomaly_data)
    return anomaly_list

# TODO: Implement
def detect_custom_anomaly(df, custom_anomaly_list):  # checks current dataframe if custom anomalies have occured
    return 0
