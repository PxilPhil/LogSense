causation_limit = 0.7  # only check overlap for applications over this causation limit (max is 1)
causation_percentual_limit = 0.3  # only return data with a percentual influence of this value to the total usage
relevancy_limit = 0.05 # how much percentage a application makes up of ram or cpu


def detect_relevancy(pc_total_df, df):
    application_list = []  # list of applications with high causality to total usage
    pc_ram = pc_total_df.iloc[0]['residentSetSize']
    pc_cpu = pc_total_df.iloc[0]['cpuUsage']
    for index, row in df.iterrows():
        if row['residentSetSize']/pc_ram > relevancy_limit or row['cpuUsage']/pc_cpu>relevancy_limit:
            application_list.append(row['name'])
    return application_list


def detect_involvement_percentual(df, timestamp_df, column, application_list):
    involvement = dict()
    # calculate how much in percentual values the delta of applications and
    # total ram usage overlap
    timestamp_df['Delta'] = timestamp_df[column].diff().dropna()
    timestamp_df = timestamp_df.dropna()
    for application in application_list:
        application_row = df.loc[df.name == application].groupby(['timestamp']).sum(numeric_only=True).sort_values(
            by=['timestamp'])


        application_row['Delta'] = application_row[column].diff()
        application_row=application_row.dropna()

        causality_list = []
        for index, row in application_row.iterrows():
            causality_list.append(row['Delta'] / timestamp_df.loc[index]['Delta'])
            # TODO: Save actual change on top of percentual

        if len(causality_list) > 0:
            involvement[application] = sum(causality_list) / len(causality_list)

    return involvement
