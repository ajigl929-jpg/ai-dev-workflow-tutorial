# Sales Dashboard: Tasks

This file tracks all work for the e-commerce sales dashboard.
Each milestone moves through To Do -> In Progress -> Done.

## Definition of Done (must hold before any milestone moves to Done)
- Acceptance criteria met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the message

## To Do
- [ ] **TASK-5: Test and deploy**
  - [ ] Dashboard runs without errors and is deployed to a public URL
  - Commit:

## In Progress

## Done
- [x] **TASK-1: Project setup and data loading**
  - [x] App runs with `streamlit run app.py` and shows a title
  - [x] Loads `data/sales-data.csv`; handles a missing file cleanly
  - Commit: 0038f15
  - Notes: clean
- [x] **TASK-2: KPI scorecards**
  - [x] Total Sales and Total Orders shown as formatted metrics
  - Commit: 22ee017
  - Notes: clean; values match PRD Expected Output ($116,500.21 total sales, 482 orders)
- [x] **TASK-3: Sales trend chart**
  - [x] Line chart of sales over time renders from the data
  - Commit: a291c54
  - Notes: clean; used monthly granularity (not daily) since 12 months of daily points would be noisy on an exec dashboard
- [x] **TASK-4: Category and region breakdowns**
  - [x] Bar charts for sales by category and by region, sorted by value
  - Commit: f2d66bd
  - Notes: caught a math error in my own region-breakdown test fixture while running it (expected sort order was wrong); fixed the assertion before committing
