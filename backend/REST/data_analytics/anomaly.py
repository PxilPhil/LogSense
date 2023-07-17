event_map = dict()

event_sensitivity = 0.1


class AnomalyData:
    def __init__(self, timestamp, change, value, is_event):
        self.timestamp = timestamp
        self.change = change
        self.value = value
        self.is_event = is_event


def detect_anomalies(selected_row, selected_value, column):
    selected_row['PercentageChange'] = selected_row[column] / selected_row['MovingAvg'].shift()
    previous_was_flagged = False

    event_map[selected_value] = []
    for index, row in selected_row.iterrows():
        percentage_change = row['PercentageChange']
        event_header = row['eventHeader']

        if abs(percentage_change - 1) > event_sensitivity:
            if (percentage_change > 1 and event_header > 1) or (percentage_change < 1 and event_header < 1):
                print('Event')
                event_map[selected_value].append(AnomalyData(index, percentage_change, row[column], True))
            elif previous_was_flagged:
                print('Continue')
            else:
                print('Anomaly')
                event_map[selected_value].append(AnomalyData(index, percentage_change, row[column], False))
            previous_was_flagged = True
        else:
            previous_was_flagged = False
