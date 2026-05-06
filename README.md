# BasketCraft Dashboard

**Live app:** https://lillianalexalabra-basket-craft-dashboard-app-tlrq0n.streamlit.app/

A Streamlit dashboard connected to a Snowflake data warehouse, built for BasketCraft sales analytics.

## Features

- **Headline Metrics** — total revenue, orders, average order value, and items sold with month-over-month deltas
- **Revenue Trend** — monthly area chart filterable by date range
- **Top Products by Revenue** — bar chart ranked by revenue within the selected date range
- **Bundle Finder** — pick any product and see which products are most often bought together with it

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Snowflake credentials:

```
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ROLE=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...
```

## Run locally

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.
