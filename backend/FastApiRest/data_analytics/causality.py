causation_limit = 0.7  # only check overlap for applications over this causation limit (max is 1)
causation_percentual_limit = 0.3  # only return data with a percentual influence of this value to the total usage
relevancy_limit = 0.05
application_list = []  # list of applications with high causality to total usage


def detect_relevancy(timestamp_df, df, column):

    pc_mean = timestamp_df[column].mean()
    application_mean = df.groupby("name").mean(numeric_only=True)
    for index, row in application_mean.iterrows():
        mean = row[column]
        if mean/pc_mean > relevancy_limit:
            application_list.append(index)
    return detect_causality_percentual(df, timestamp_df, column)


def detect_causality_percentual(df, timestamp_df, column):
    causality_map = dict()
    # calculate how much in percentual values the delta of applications and
    # total ram usage overlap
    timestamp_df['Delta'] = timestamp_df[column].diff().dropna()

    for application in application_list:
        application_row = df.loc[df.name == application].groupby(['timestamp']).sum(numeric_only=True).sort_values(
            by=['timestamp'])

        application_row['Delta'] = application_row[column].diff().dropna()

        causality_list = []
        for index, row in application_row.iterrows():
            causality_list.append(abs(row['Delta'] / timestamp_df.loc[index]['Delta']))  # abs because negative values

        if len(causality_list) > 0:
            causality_map[application] = sum(causality_list) / len(causality_list)

    return convert_to_list(causality_map)


def convert_to_list(
        causality_map):  # helper method to convert map into list as only allowed applications are contained in it
    causality_map = dict(filter(filter_causation, causality_map.items()))
    return list(causality_map.keys())


def filter_causation(pair):
    key, value = pair
    if value >= causation_percentual_limit:
        return True  # filter pair out of the dictionary
    else:
        return False  # keep pair in the filtered dictionary
