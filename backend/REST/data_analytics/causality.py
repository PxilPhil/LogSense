causation_limit = 0.7  # only check overlap for applications over this causation limit (max is 1)
causation_percentual_limit = 0.3  # only return data with a percentual influence of this value to the total usage
application_list = []  # list of applications with high causality to total usage


# we maybe don't need detect_causality_percentual if we just calculate the amount beforehand
def detect_causality(timestamp_df, agg_df, df,
                     column):  # alternatively just work with the processes with the largest usage
    for index, row in agg_df.iterrows():
        curr_row = df.loc[df.name == index].groupby(['timestamp']).sum(numeric_only=True).sort_values(by=['timestamp'])
        corr = timestamp_df[column].corr(curr_row[column])  # find out causality
        if corr > causation_limit:
            application_list.append(index)
    return detect_causality_percentual(df, timestamp_df, column)


def detect_causality_percentual(df, timestamp_df, column):
    causality_map = dict()
    # calculate how much in percentual values the delta of applications and
    # total ram usage overlap
    timestamp_df['Delta'] = timestamp_df[column].diff()
    timestamp_df['Delta'].fillna(1, inplace=True)

    for application in application_list:
        application_row = df.loc[df.name == application].groupby(['timestamp']).sum(numeric_only=True).sort_values(
            by=['timestamp'])
        application_row['Delta'] = application_row[column].diff()
        application_row['Delta'].fillna(1, inplace=True)

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
    print(key)
    print(value)
    if value >= causation_percentual_limit:
        return True  # filter pair out of the dictionary
    else:
        return False  # keep pair in the filtered dictionary
