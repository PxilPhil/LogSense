event_sensitivity = 0.1


class AnomalyData:
    def __init__(self, timestamp, change, value, is_event):
        self.timestamp = timestamp
        self.change = change
        self.value = value
        self.is_event = is_event


def detect_anomaly(selected_row, column, moving_avg, previous_anomaly, anomaly_map, application):
    percentual_change = selected_row[column].values[0] / moving_avg
    event_header = selected_row['processCountDifference'].values[0]

    print(percentual_change)
    if (not previous_anomaly) and (abs(percentual_change - 1) > event_sensitivity):
        if event_header != 0:
            anomaly_map[application] = (AnomalyData(selected_row.index[0], percentual_change, selected_row[column], True))
        else:
            anomaly_map[application] = (
                AnomalyData(selected_row.index[0], percentual_change, selected_row[column], False))


def detect_anomalies(selected_row, column):
    anomaly_list = []
    selected_row['PercentageChange'] = selected_row[column] / selected_row['MovingAvg'].shift()
    selected_row = selected_row.dropna()
    previous_was_flagged = False
    for index, row in selected_row.iterrows():
        percentage_change = row['PercentageChange']
        event_header = row['process_count_difference']

        if abs(percentage_change - 1) > event_sensitivity:
            if (percentage_change > 1 and event_header > 1) or (percentage_change < 1 and event_header < 1):
                anomaly_list.append(AnomalyData(index, percentage_change, row[column], True))
            elif not previous_was_flagged:
                anomaly_list.append(AnomalyData(index, percentage_change, row[column], False))
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return anomaly_list


def detect_custom_anomaly(df, custom_anomaly_list):  # checks current dataframe if custom anomalies have occured
    return 0
