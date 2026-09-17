import streamlit as st

from calculations import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    df = load_sales_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Could not find the sales data file at `{DATA_PATH}`.")
    st.stop()
