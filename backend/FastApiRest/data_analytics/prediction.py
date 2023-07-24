from sklearn.linear_model import LinearRegression


def fit_linear_regression(df):
    LR = LinearRegression()
    LR.fit(df.index.values.reshape(-1, 1), df['freeDiskSpace'].values)
    return LR


def predict_for_df(LR, df):
    prediction = LR.predict(df.index.values.reshape(-1, 1))
    df['LinearRegression'] = prediction
    return df
