import pandas as pd
import pytest

from calculations import load_sales_data


def test_load_sales_data_returns_dataframe_with_expected_columns(tmp_path):
    csv_content = (
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Widget,Electronics,North,1,10.00,10.00\n"
    )
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(csv_content)

    df = load_sales_data(str(csv_path))

    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_missing_file_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_sales_data("data/does-not-exist.csv")


from calculations import compute_total_sales


def test_compute_total_sales_sums_total_amount_column():
    df = pd.DataFrame({"total_amount": [100.0, 250.50, 49.99]})

    result = compute_total_sales(df)

    assert result == 400.49


from calculations import compute_total_orders


def test_compute_total_orders_counts_rows():
    df = pd.DataFrame({"order_id": ["ORD-1", "ORD-2", "ORD-3"]})

    result = compute_total_orders(df)

    assert result == 3


from calculations import compute_monthly_trend


def test_compute_monthly_trend_groups_by_calendar_month():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-03", "2024-01-20", "2024-02-05"]),
        "total_amount": [100.0, 50.0, 75.0],
    })

    result = compute_monthly_trend(df)

    assert list(result["month"]) == [
        pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01"),
    ]
    assert list(result["total_amount"]) == [150.0, 75.0]


from calculations import compute_category_breakdown


def test_compute_category_breakdown_sorted_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Electronics", "Audio", "Wearables"],
        "total_amount": [50.0, 200.0, 30.0, 100.0],
    })

    result = compute_category_breakdown(df)

    assert list(result["category"]) == ["Electronics", "Wearables", "Audio"]
    assert list(result["total_amount"]) == [200.0, 100.0, 80.0]
