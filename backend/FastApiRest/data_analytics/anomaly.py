from model.data import AnomalyData

event_sensitivity = 0.1

def detect_anomaly(selected_row, column, moving_avg, previous_anomaly, anomaly_list, application):
    percentual_change = selected_row[column].values[0] / moving_avg
    event_header = selected_row['processCountDifference'].values[0]

    print(percentual_change)
    if (not previous_anomaly) and (abs(percentual_change - 1) > event_sensitivity):
        if event_header != 0:
            anomaly_data=AnomalyData(anomaly_type=1, timestamp=selected_row.index[0], change=percentual_change, application=application, column=column)
            anomaly_list.append(anomaly_data)
        else:
            anomaly_data=AnomalyData(anomaly_type=2, timestamp=selected_row.index[0], change=percentual_change, application=application, column=column)
            anomaly_list.append(anomaly_data)

def detect_anomalies(selected_row, column, application_name):
    anomaly_list = []
    selected_row['PercentageChange'] = selected_row[column] / selected_row['MovingAvg'].shift()
    selected_row = selected_row.dropna()
    previous_was_flagged = False
    for index, row in selected_row.iterrows():
        percentual_change = row['PercentageChange']
        event_header = row['process_count_difference']

        if abs(percentual_change - 1) > event_sensitivity:
            if (percentual_change > 1 and event_header > 1) or (percentual_change < 1 and event_header < 1):
                anomaly_data = AnomalyData(anomaly_type=1, timestamp=selected_row.index[0], change=percentual_change, application=application_name, column=column)
                anomaly_list.append(anomaly_data)
            elif not previous_was_flagged:
                anomaly_data = AnomalyData(anomaly_type=2, timestamp=selected_row.index[0], change=percentual_change, application=application_name, column=column)
                anomaly_list.append(anomaly_data)
            previous_was_flagged = True
        else:
            previous_was_flagged = False
    return anomaly_list


def detect_custom_anomaly(df, custom_anomaly_list):  # checks current dataframe if custom anomalies have occured

    return 0
