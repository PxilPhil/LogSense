trend_limit = 0 # TODO: Implement trend limit
class TrendData:  # can remove curr or prev_value since it can be calculated with change but its easier this way
    def __init__(self, prev, curr, prev_value, curr_value, change):
        self.prev = prev
        self.curr = curr
        self.prev_value = prev_value
        self.curr_value = curr_value
        self.change = change


def detect_trends(selected_row, selected_column):
    trend_list = []

    last_row_change = 0
    remembered_row = selected_row.iloc[0];
    prev_row = remembered_row
    for index, row in selected_row.iterrows():
        curr_row_change = row[selected_column] / prev_row[selected_column]
        if (not ((last_row_change < 1 and curr_row_change < 1) or (last_row_change > 1 and curr_row_change > 1) or (
                last_row_change == 1 and curr_row_change == 1))):
            change = prev_row[selected_column] / remembered_row[selected_column]
            if change>1+trend_limit or change<1-trend_limit:
                trend = TrendData(remembered_row.name, prev_row.name, remembered_row[selected_column], prev_row[selected_column],
                              change)
                remembered_row = prev_row
                trend_list.append(trend)
        prev_row = row
        last_row_change = curr_row_change
    return trend_list
