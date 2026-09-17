import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])
