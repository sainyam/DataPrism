import pandas as pd

def get_runtime(df):
    if df.shape[0] < 10000:
        return 1  # Pass
    else:
        return 0  # Fail


def run(data, threshold, bugs):
    df = pd.read_csv(data)
    violation = get_runtime(df)
    return violation > int(threshold), violation
