# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit sales dashboard (KPIs, trend chart, category/region breakdowns) reading from `data/sales-data.csv`, per the PRD and design doc.

**Architecture:** A pure-function `calculations.py` module (load + aggregate the CSV) tested with pytest, and a thin `app.py` that calls those functions and renders Streamlit/Plotly components. No database, no auth, no filtering — Phase 1 scope only.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly Express, pytest, plain `venv/` + `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-16-sales-dashboard-design.md`

## Global Constraints

- Work on the current branch `feature/sales-dashboard`. Do not create a git worktree.
- Dependencies live in a plain virtual environment at `venv/`, listed in `requirements.txt` (streamlit, pandas, plotly, pytest). No uv, no conda, no `pyproject.toml`/`Pipfile`.
- `calculations.py` contains no Streamlit imports — it must be importable and testable without running the app.
- Every commit message includes the `TASKS.md` milestone ID it belongs to (TASK-1 .. TASK-5).
- The plan's own task numbers (Task 1, Task 2, ...) are separate from the TASKS.md milestone IDs; each task below states which milestone it belongs to.
- Deployment (last task) is human-executed — do not run it as part of automated plan execution.

---

## Milestone: TASK-1 — Project setup and data loading

### Task 1: Project scaffold

**Files:**
- Create: `requirements.txt`
- Modify: `.gitignore` (add `venv/`, `__pycache__/`, `*.pyc`)
- Create: `venv/` (virtual environment, not committed)

**Interfaces:**
- Produces: an activated `venv/` with `streamlit`, `pandas`, `plotly`, `pytest` installed, importable by every later task.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`

- [ ] **Step 2: Write requirements.txt**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 3: Activate the venv and install dependencies**

Run: `source venv/bin/activate && pip install -r requirements.txt`
Expected: all four packages install without error.

- [ ] **Step 4: Update .gitignore**

Add these lines to `.gitignore` (create the file if it doesn't exist):

```
venv/
__pycache__/
*.pyc
```

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .gitignore
git commit -m "TASK-1: scaffold project with venv and requirements.txt"
```

---

### Task 2: `load_sales_data` (TDD)

**Files:**
- Create: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Produces: `load_sales_data(path: str) -> pandas.DataFrame` — reads a CSV at `path` with columns `date, order_id, product, category, region, quantity, unit_price, total_amount`, parses `date` as a datetime column, and raises `FileNotFoundError` if `path` doesn't exist. Used by `app.py` (Task 3) and every later `compute_*` function.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_calculations.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_calculations.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'calculations'`

- [ ] **Step 3: Write minimal implementation**

Create `calculations.py`:

```python
import pandas as pd


def load_sales_data(path):
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_calculations.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-1: add load_sales_data with tests"
```

---

### Task 3: `app.py` skeleton with missing-file handling

**Files:**
- Create: `app.py`

**Interfaces:**
- Consumes: `load_sales_data(path)` from `calculations.py` (Task 2)
- Produces: a running Streamlit page with a title and a loaded `df` variable, ready for Task 6/8/11 to render against. Defines module-level constant `DATA_PATH = "data/sales-data.csv"`, reused by no other file (each later task edits `app.py` directly).

- [ ] **Step 1: Write app.py**

```python
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
```

- [ ] **Step 2: Run the app manually to verify it starts**

Run: `streamlit run app.py`
Expected: page loads at the local URL, shows the title "ShopSmart Sales Dashboard", no errors in the terminal. Stop the server with Ctrl+C when done.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-1: add app.py skeleton with data loading"
```

---

## Milestone: TASK-2 — KPI scorecards

### Task 4: `compute_total_sales` (TDD)

**Files:**
- Modify: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Consumes: a `pandas.DataFrame` with a `total_amount` column (as produced by `load_sales_data`)
- Produces: `compute_total_sales(df: pandas.DataFrame) -> float` — sum of `total_amount`. Used by `app.py` (Task 6).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_calculations.py`:

```python
from calculations import compute_total_sales


def test_compute_total_sales_sums_total_amount_column():
    df = pd.DataFrame({"total_amount": [100.0, 250.50, 49.99]})

    result = compute_total_sales(df)

    assert result == 400.49
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py::test_compute_total_sales_sums_total_amount_column -v`
Expected: FAIL with `ImportError: cannot import name 'compute_total_sales'`

- [ ] **Step 3: Write minimal implementation**

Add to `calculations.py`:

```python
def compute_total_sales(df):
    return float(df["total_amount"].sum())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py::test_compute_total_sales_sums_total_amount_column -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-2: add compute_total_sales with test"
```

---

### Task 5: `compute_total_orders` (TDD)

**Files:**
- Modify: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Consumes: a `pandas.DataFrame` (row count only, any columns)
- Produces: `compute_total_orders(df: pandas.DataFrame) -> int` — number of rows. Used by `app.py` (Task 6).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_calculations.py`:

```python
from calculations import compute_total_orders


def test_compute_total_orders_counts_rows():
    df = pd.DataFrame({"order_id": ["ORD-1", "ORD-2", "ORD-3"]})

    result = compute_total_orders(df)

    assert result == 3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py::test_compute_total_orders_counts_rows -v`
Expected: FAIL with `ImportError: cannot import name 'compute_total_orders'`

- [ ] **Step 3: Write minimal implementation**

Add to `calculations.py`:

```python
def compute_total_orders(df):
    return int(len(df))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py::test_compute_total_orders_counts_rows -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-2: add compute_total_orders with test"
```

---

### Task 6: Render KPI metrics in app.py

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `compute_total_sales(df)` (Task 4), `compute_total_orders(df)` (Task 5), the `df` loaded in Task 3

- [ ] **Step 1: Add the KPI row**

In `app.py`, update the import line and append below the `st.stop()` block:

```python
from calculations import compute_total_sales, compute_total_orders, load_sales_data
```

```python
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${compute_total_sales(df):,.0f}")
col2.metric("Total Orders", f"{compute_total_orders(df):,}")
```

- [ ] **Step 2: Run the app manually to verify the KPIs render**

Run: `streamlit run app.py`
Expected: two metric cards show, Total Sales near `$116,500` and Total Orders `482`. Stop the server with Ctrl+C when done.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-2: render Total Sales and Total Orders KPI cards"
```

---

## Milestone: TASK-3 — Sales trend chart

### Task 7: `compute_monthly_trend` (TDD)

**Files:**
- Modify: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Consumes: a `pandas.DataFrame` with `date` (datetime) and `total_amount` columns
- Produces: `compute_monthly_trend(df: pandas.DataFrame) -> pandas.DataFrame` with columns `month` (Timestamp, first of month) and `total_amount` (float), sorted ascending by `month`. Used by `app.py` (Task 8).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_calculations.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py::test_compute_monthly_trend_groups_by_calendar_month -v`
Expected: FAIL with `ImportError: cannot import name 'compute_monthly_trend'`

- [ ] **Step 3: Write minimal implementation**

Add to `calculations.py`:

```python
def compute_monthly_trend(df):
    trend = df.copy()
    trend["month"] = trend["date"].dt.to_period("M").dt.to_timestamp()
    result = trend.groupby("month", as_index=False)["total_amount"].sum()
    return result.sort_values("month").reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py::test_compute_monthly_trend_groups_by_calendar_month -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-3: add compute_monthly_trend with test"
```

---

### Task 8: Render trend line chart in app.py

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `compute_monthly_trend(df)` (Task 7)

- [ ] **Step 1: Add the trend chart**

In `app.py`, add to the imports:

```python
import plotly.express as px

from calculations import compute_monthly_trend
```

Append below the KPI row:

```python
st.subheader("Sales Trend Over Time")
trend = compute_monthly_trend(df)
fig_trend = px.line(
    trend, x="month", y="total_amount", markers=True,
    labels={"month": "Month", "total_amount": "Sales ($)"},
)
st.plotly_chart(fig_trend, use_container_width=True)
```

- [ ] **Step 2: Run the app manually to verify the chart renders**

Run: `streamlit run app.py`
Expected: a line chart appears below the KPIs, showing 12 monthly points, with hover tooltips showing exact values. Stop the server with Ctrl+C when done.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-3: render sales trend line chart"
```

---

## Milestone: TASK-4 — Category and region breakdowns

### Task 9: `compute_category_breakdown` (TDD)

**Files:**
- Modify: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Consumes: a `pandas.DataFrame` with `category` and `total_amount` columns
- Produces: `compute_category_breakdown(df: pandas.DataFrame) -> pandas.DataFrame` with columns `category`, `total_amount`, sorted descending by `total_amount`. Used by `app.py` (Task 11).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_calculations.py`:

```python
from calculations import compute_category_breakdown


def test_compute_category_breakdown_sorted_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Electronics", "Audio", "Wearables"],
        "total_amount": [50.0, 200.0, 30.0, 100.0],
    })

    result = compute_category_breakdown(df)

    assert list(result["category"]) == ["Electronics", "Wearables", "Audio"]
    assert list(result["total_amount"]) == [200.0, 100.0, 80.0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py::test_compute_category_breakdown_sorted_descending -v`
Expected: FAIL with `ImportError: cannot import name 'compute_category_breakdown'`

- [ ] **Step 3: Write minimal implementation**

Add to `calculations.py`:

```python
def compute_category_breakdown(df):
    result = df.groupby("category", as_index=False)["total_amount"].sum()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py::test_compute_category_breakdown_sorted_descending -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-4: add compute_category_breakdown with test"
```

---

### Task 10: `compute_region_breakdown` (TDD)

**Files:**
- Modify: `calculations.py`
- Test: `tests/test_calculations.py`

**Interfaces:**
- Consumes: a `pandas.DataFrame` with `region` and `total_amount` columns
- Produces: `compute_region_breakdown(df: pandas.DataFrame) -> pandas.DataFrame` with columns `region`, `total_amount`, sorted descending by `total_amount`. Used by `app.py` (Task 11).

- [ ] **Step 1: Write the failing test**

Add to `tests/test_calculations.py`:

```python
from calculations import compute_region_breakdown


def test_compute_region_breakdown_sorted_descending():
    df = pd.DataFrame({
        "region": ["North", "South", "North", "East"],
        "total_amount": [40.0, 90.0, 60.0, 20.0],
    })

    result = compute_region_breakdown(df)

    assert list(result["region"]) == ["South", "North", "East"]
    assert list(result["total_amount"]) == [90.0, 100.0, 20.0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_calculations.py::test_compute_region_breakdown_sorted_descending -v`
Expected: FAIL with `ImportError: cannot import name 'compute_region_breakdown'`

- [ ] **Step 3: Write minimal implementation**

Add to `calculations.py`:

```python
def compute_region_breakdown(df):
    result = df.groupby("region", as_index=False)["total_amount"].sum()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_calculations.py::test_compute_region_breakdown_sorted_descending -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-4: add compute_region_breakdown with test"
```

---

### Task 11: Render category and region bar charts in app.py

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `compute_category_breakdown(df)` (Task 9), `compute_region_breakdown(df)` (Task 10)

- [ ] **Step 1: Add the breakdown charts**

In `app.py`, add to the imports:

```python
from calculations import compute_category_breakdown, compute_region_breakdown
```

Append below the trend chart:

```python
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    category = compute_category_breakdown(df)
    fig_category = px.bar(
        category, x="category", y="total_amount",
        labels={"category": "Category", "total_amount": "Sales ($)"},
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col4:
    st.subheader("Sales by Region")
    region = compute_region_breakdown(df)
    fig_region = px.bar(
        region, x="region", y="total_amount",
        labels={"region": "Region", "total_amount": "Sales ($)"},
    )
    st.plotly_chart(fig_region, use_container_width=True)
```

- [ ] **Step 2: Run the app manually to verify both charts render**

Run: `streamlit run app.py`
Expected: two bar charts side by side, categories/regions sorted highest to lowest, hover tooltips show exact values. Stop the server with Ctrl+C when done.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-4: render category and region breakdown bar charts"
```

---

## Milestone: TASK-5 — Test and deploy

### Task 12: Full test suite and PRD acceptance check

**Files:**
- None created or modified (verification task)

**Interfaces:**
- Consumes: the full `calculations.py` test suite and the running `app.py`

- [ ] **Step 1: Run the full test suite**

Run: `pytest -v`
Expected: all tests pass (9 tests: 2 for `load_sales_data`, 1 each for the five `compute_*` functions, plus the two breakdown-sort tests already counted).

- [ ] **Step 2: Run the app and check it against the PRD**

Run: `streamlit run app.py`

Open the local URL and check every item in `prd/ecommerce-analytics.md`'s Acceptance Criteria section: KPIs visible, trend chart correct, category chart sorted, region chart sorted, data matches the Expected Output table (~$116,500 total sales, 482 orders), no errors in the terminal. Stop the server with Ctrl+C when done.

- [ ] **Step 3: Commit anything outstanding**

If step 2 required any code fixes, commit them:

```bash
git add -A
git commit -m "TASK-5: fix issues found in acceptance check"
```

If nothing needed fixing, no commit is required for this step.

---

### Task 13: Deploy to Streamlit Community Cloud — HUMAN-EXECUTED

**This step is not run as part of automated plan execution.** The user deploys it themselves, after this branch is reviewed and merged to `main` (see `workshop-build-deploy.md` Section 4.5 and Section 5).

- [ ] Merge `feature/sales-dashboard` into `main` (Section 4.5 of the workshop guide)
- [ ] Push `main` to GitHub
- [ ] Deploy from `main` on [share.streamlit.io](https://share.streamlit.io), main file `app.py`
- [ ] Record the live URL in `TASKS.md` and `README.md` (Section 5.2 of the workshop guide)

---

## Self-Review Notes

- **Spec coverage:** every design-doc milestone mapping row (TASK-1..TASK-5) has at least one task above; every FR in the PRD (FR-1 KPIs, FR-2 trend, FR-3 category, FR-4 region, FR-5 CSV load) is covered by a task.
- **Placeholder scan:** no TBD/TODO; every step has runnable code or an exact command.
- **Type consistency:** all `compute_*` functions take a `pandas.DataFrame` and return either a scalar (`compute_total_sales` -> float, `compute_total_orders` -> int) or a `pandas.DataFrame` with named columns, consistently referenced by name across tasks (`month`/`total_amount`, `category`/`total_amount`, `region`/`total_amount`).
