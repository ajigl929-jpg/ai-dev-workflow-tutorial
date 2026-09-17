# CLAUDE.md

This file gives Claude Code context for working in this repository.

## Project

A Streamlit sales dashboard for ShopSmart, an e-commerce retailer, built from
`prd/ecommerce-analytics.md`. It reads static transaction data from
`data/sales-data.csv` and shows Total Sales / Total Orders KPIs, a monthly
sales trend line chart, and category/region breakdown bar charts.

This repo is also a workshop tutorial repo (`workshop-build-deploy.md`,
`pre-work-setup.md`, etc.) — those top-level `.md` files are course material,
not part of the dashboard itself.

## Running the app

```bash
source venv/bin/activate   # macOS/Linux; venv\Scripts\activate on Windows
streamlit run app.py
```

## Running tests

```bash
source venv/bin/activate
pytest -v
```

`pytest.ini` sets `pythonpath = .` so `tests/test_calculations.py` can import
`calculations` from the project root without a package/`__init__.py`.

## Key files

- `app.py` — Streamlit UI only: page layout, widgets, chart rendering. Reads
  `data/sales-data.csv` via `calculations.load_sales_data`.
- `calculations.py` — pure data functions (no Streamlit imports), so they're
  testable without running the app: `load_sales_data`, `compute_total_sales`,
  `compute_total_orders`, `compute_monthly_trend`,
  `compute_category_breakdown`, `compute_region_breakdown`.
- `tests/test_calculations.py` — pytest tests for every function in
  `calculations.py`, using small hand-built DataFrame fixtures rather than the
  full CSV.
- `data/sales-data.csv` — the source data (482 transaction rows, 12 months,
  columns: `date, order_id, product, category, region, quantity, unit_price,
  total_amount`).
- `requirements.txt` — pinned lower bounds for `streamlit`, `pandas`,
  `plotly`, `pytest`. This is also what Streamlit Community Cloud reads at
  deploy time, so keep it accurate and don't add a `uv.lock`, `Pipfile`, or
  `pyproject.toml` (Streamlit Cloud prefers those over `requirements.txt` if
  present, which breaks the expected dependency set).
- `TASKS.md` — the milestone board (TASK-1..TASK-5), the durable record of
  what's done. Update it, don't just rely on chat history.
- `docs/superpowers/specs/` and `docs/superpowers/plans/` — the design doc and
  implementation plan this dashboard was built from.

## Conventions

- Keep `calculations.py` free of Streamlit imports; anything chart/page
  related belongs in `app.py`.
- Category and region breakdowns are always sorted descending by
  `total_amount` (PRD FR-3/FR-4).
- Trend chart uses monthly granularity, not daily (12 months of daily points
  is too noisy for an executive dashboard).
- Commit messages carry the `TASKS.md` milestone ID they belong to (e.g.
  `TASK-2: ...`).
- Missing `data/sales-data.csv` is handled with `st.error` + `st.stop()` in
  `app.py`, not a stack trace.

## Lessons

- **Write out sort-order test assertions by hand-summing the fixture data
  first.** While building TASK-4, a `compute_region_breakdown` test shipped
  with the wrong expected order because the fixture's per-region totals
  weren't summed correctly before writing the assertion. Caught by running
  the test (it failed against the real implementation), not by inspection.
- **`pytest` alone won't find a root-level module from `tests/`** without
  either an `__init__.py` package layout or a `pythonpath` setting — this repo
  uses `pytest.ini` with `pythonpath = .` rather than restructuring into a
  package, since the dashboard is intentionally two flat files.
