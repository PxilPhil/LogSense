
def calc_allocation(latest_total_value, column, df):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    for index, row in df.iterrows():
        allocation_map[row['name']] = str(row[column]/latest_total_value) # convert float into string to be passable via json
    return allocation_map

