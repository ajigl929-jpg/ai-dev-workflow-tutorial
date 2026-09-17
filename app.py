import plotly.express as px
import streamlit as st

from calculations import (
    compute_monthly_trend,
    compute_total_orders,
    compute_total_sales,
    load_sales_data,
)

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    df = load_sales_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Could not find the sales data file at `{DATA_PATH}`.")
    st.stop()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${compute_total_sales(df):,.0f}")
col2.metric("Total Orders", f"{compute_total_orders(df):,}")

st.subheader("Sales Trend Over Time")
trend = compute_monthly_trend(df)
fig_trend = px.line(
    trend, x="month", y="total_amount", markers=True,
    labels={"month": "Month", "total_amount": "Sales ($)"},
)
st.plotly_chart(fig_trend, use_container_width=True)
