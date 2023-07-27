event_sensitivity = 0.1


class AnomalyData:
    def __init__(self, timestamp, change, value, is_event):
        self.timestamp = timestamp
        self.change = change
        self.value = value
        self.is_event = is_event


def detect_anomalies(selected_row, column, moving_avg, previous_anomaly, anomaly_map, application):  # only makes sense for processes as of now
    percentual_change = selected_row[column].values[0] / moving_avg
    event_header = selected_row['processCountDifference'].values[0]

    print(percentual_change)
    if (not previous_anomaly) and (abs(percentual_change - 1) > event_sensitivity):
        if event_header != 0:
            anomaly_map[application] = (AnomalyData(selected_row.index[0], percentual_change, selected_row[column], True))
        else:
            anomaly_map[application] = (
                AnomalyData(selected_row.index[0], percentual_change, selected_row[column], False))

def detect_custom_anomaly(df, custom_anomaly_list):  # checks current dataframe if custom anomalies have occured
    return 0
