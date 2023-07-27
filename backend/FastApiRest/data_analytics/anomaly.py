event_sensitivity = 0.1


class AnomalyData:
    def __init__(self, timestamp, change, value, is_event):
        self.timestamp = timestamp
        self.change = change
        self.value = value
        self.is_event = is_event


def detect_anomalies(selected_row, column, moving_avg):  # only makes sense for processes as of now
    anomaly_list = []
    selected_row['PercentageChange'] = selected_row[column] / moving_avg
    previous_was_flagged = False
    for index, row in selected_row.iterrows():
        percentage_change = row['PercentageChange']
        event_header = row['processCountDifference']

        if abs(percentage_change - 1) > event_sensitivity:
            if (percentage_change > 1 and event_header > 1) or (percentage_change < 1 and event_header < 1):
                anomaly_list.append(AnomalyData(index, percentage_change, row[column], True))
            elif not previous_was_flagged:
                anomaly_list.append(AnomalyData(index, percentage_change, row[column], False))
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return anomaly_list

def detect_custom_anomaly(df, custom_anomaly_list): #checks current dataframe if custom anomalies have occured
    return 0
