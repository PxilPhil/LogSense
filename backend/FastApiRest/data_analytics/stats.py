
def calc_allocation(df, column, application_list):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    sum = df[column].sum()
    for application in application_list:
        result = df.loc[df.name == application, 'residentSetSize'].iloc[0]
        allocation_map[application] = result/sum
    return allocation_map

