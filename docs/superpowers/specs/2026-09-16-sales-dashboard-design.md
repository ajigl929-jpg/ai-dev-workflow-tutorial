# Sales Dashboard: Design

**Date:** 2026-09-16
**Status:** Approved (autopilot build — see TASKS.md and prd/ecommerce-analytics.md)

## Purpose

Build a Streamlit dashboard that gives ShopSmart stakeholders (finance, marketing,
regional managers, CEO) immediate, self-service visibility into sales performance,
replacing the current weekly manual Excel report. Scope is PRD Phase 1 only: KPIs,
a sales trend chart, and category/region breakdowns, read from a static CSV.

## Architecture

Two Python modules plus tests, kept deliberately small:

```
app.py            Streamlit entry point: layout, widgets, chart rendering
calculations.py   Pure functions: load + aggregate the sales data (no Streamlit imports)
tests/
  test_calculations.py   pytest tests for every function in calculations.py
data/
  sales-data.csv  Existing source data (unchanged)
requirements.txt  streamlit, pandas, plotly, pytest
venv/             Local virtual environment (gitignored)
```

Keeping calculations out of `app.py` is what makes them testable without starting
the Streamlit server, and keeps `app.py` focused on presentation.

## Data flow

1. `calculations.load_sales_data(path)` reads the CSV with `pandas.read_csv`,
   parsing `date` as a datetime column. Raises `FileNotFoundError` if the path
   doesn't exist (the caller in `app.py` handles this, per "Error handling" below).
2. `app.py` calls the aggregation functions on the loaded DataFrame:
   - `compute_total_sales(df)` -> float, sum of `total_amount`
   - `compute_total_orders(df)` -> int, row count
   - `compute_monthly_trend(df)` -> DataFrame with `month`, `total_amount`, grouped
     by calendar month (chosen over daily granularity: 482 records over 12 months
     would make a daily line noisy and hard to read on an executive dashboard)
   - `compute_category_breakdown(df)` -> DataFrame with `category`, `total_amount`,
     sorted descending by `total_amount` (per FR-3)
   - `compute_region_breakdown(df)` -> DataFrame with `region`, `total_amount`,
     sorted descending by `total_amount` (per FR-4)
3. `app.py` renders each result: `st.metric` for the two KPIs, `plotly.express`
   for the line chart and the two bar charts.

## Layout

- Page title: "ShopSmart Sales Dashboard", wide layout
- Row 1: two KPI cards side by side (`st.columns(2)`) — Total Sales formatted as
  `$X,XXX`, Total Orders formatted with a thousands separator
- Row 2: sales trend line chart, full width, with interactive tooltips
- Row 3: category bar chart and region bar chart side by side (`st.columns(2)`),
  both with interactive tooltips

## Error handling

Scope is deliberately narrow, matching the PRD (Phase 2 items like auth, filtering,
and exports are explicitly out of scope):

- **Missing data file:** `app.py` catches `FileNotFoundError` from
  `load_sales_data`, shows `st.error("...")` with the expected path, and calls
  `st.stop()` so the rest of the page doesn't render on top of a crash.
- No other failure modes are handled specially; the CSV format is fixed and
  controlled (FR-5), so malformed-input handling is not part of this scope.

## Testing

- `tests/test_calculations.py` covers the five functions in `calculations.py`
  against a small, hand-built DataFrame fixture (not the full CSV), so expected
  values are easy to verify by inspection.
- Chart rendering and page layout are not unit-tested — Streamlit/Plotly
  components are hard to test meaningfully outside a running app. They're
  verified manually against the PRD's Acceptance Criteria and Expected Output
  table (`~$116,500` total sales, `482` orders).

## Milestone mapping

| TASKS.md milestone | Covers |
|---|---|
| TASK-1 | Project scaffold, `venv/`, `requirements.txt`, `calculations.load_sales_data`, `app.py` skeleton with title, missing-file handling |
| TASK-2 | `compute_total_sales`, `compute_total_orders`, KPI rendering |
| TASK-3 | `compute_monthly_trend`, trend line chart |
| TASK-4 | `compute_category_breakdown`, `compute_region_breakdown`, both bar charts |
| TASK-5 | Full local test pass against PRD acceptance criteria; deployment (human-executed, out of this plan's build steps) |

## Out of scope (per PRD Phase 2)

Authentication, real-time/database data source, export, email alerts, filtering,
drill-down, mobile-responsive design.
