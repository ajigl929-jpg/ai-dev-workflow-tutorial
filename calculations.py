import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def compute_total_sales(df):
    return float(df["total_amount"].sum())
