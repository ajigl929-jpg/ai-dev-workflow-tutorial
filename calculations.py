import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def compute_total_sales(df):
    return float(df["total_amount"].sum())


def compute_total_orders(df):
    return int(len(df))


def compute_monthly_trend(df):
    trend = df.copy()
    trend["month"] = trend["date"].dt.to_period("M").dt.to_timestamp()
    result = trend.groupby("month", as_index=False)["total_amount"].sum()
    return result.sort_values("month").reset_index(drop=True)


def _breakdown_by(df, column):
    result = df.groupby(column, as_index=False)["total_amount"].sum()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)


def compute_category_breakdown(df):
    return _breakdown_by(df, "category")


def compute_region_breakdown(df):
    return _breakdown_by(df, "region")
