def calc_allocation(latest_total_value, column, df):  # ONLY PASS THE MOST CURRENT DATAFRAME
    allocation_map = dict()
    for index, row in df.iterrows():  # TODO: If iterrows dont work, access values directly
        allocation_map[row['name']] = row[column] / latest_total_value
    return allocation_map
