from pandas import DataFrame
import ruptures as rpt

from db_access.application import get_latest_application_data, get_application_data_before

penalty_value = 0.5  # value used for "penalizing" the pelting model for overfitting, decrease to detect more insignicant events and vice versa -> sensitivity in other words

"""
    Change detection works well for RAM but not for things like cpu
    -> penalty_value should be 0.5 to 1 depending on sensitivity
    It highlights data points when large changes have occured (
    
    Solution for CPU:
    -> run pelting on it and sort out false positives
    -> use anomaly detection instead (current approach) and bucket if necessary
    
    Approach for finding meaningful events:
    Run pelting algorithm on the total pcdataframe to find change points
    Then fetch all available application data for the last few entries from change points to check if applications or processes were closed or opened
    Keep in mind to check on time gaps as well
"""

def detect_change_events(df: DataFrame, column: str):  # should not be used for data with very high variance like cpu usage
    df_values = df[column].values  # Access values
    detector = rpt.Pelt(model="rbf").fit(df_values.reshape(-1, 1))  # Reshape data
    change_points = detector.predict(pen=penalty_value)  # data points where significant change was detected

    for data_point in change_points:
        print(data_point)
    return change_points

def check_on_events(change_points: list, pc_id: int):
    """
    Function to loop through event list to call gather_event_logs()

    :return:
    """
    for entry in change_points:
        applications_df, application_data_list = get_application_data_before(1, entry, 10)
        for index, row in applications_df.iterrows():
            #TODO: Find out where large changes have happened
            print(row)
def gather_event_logs():
    """
    Function to gather information on why an event was caused like an application closing, processes closing or similiar
    :return:
    """


