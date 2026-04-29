import os

import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

st.title("BasketCraft Dashboard")


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


@st.cache_data(ttl=600)
def get_product_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM PRODUCTS")
    return cur.fetchone()[0]


@st.cache_data(ttl=600)
def get_headline_metrics():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        WITH latest_month AS (
            SELECT DATE_TRUNC('month', MAX(TO_TIMESTAMP_NTZ(CREATED_AT, 9))) AS latest
            FROM ORDERS
        ),
        monthly AS (
            SELECT
                DATE_TRUNC('month', TO_TIMESTAMP_NTZ(CREATED_AT, 9)) AS month,
                SUM(PRICE_USD)       AS revenue,
                COUNT(ORDER_ID)      AS orders,
                AVG(PRICE_USD)       AS aov,
                SUM(ITEMS_PURCHASED) AS items_sold
            FROM ORDERS
            GROUP BY 1
        )
        SELECT m.month, m.revenue, m.orders, m.aov, m.items_sold
        FROM monthly m, latest_month l
        WHERE m.month IN (l.latest, DATEADD('month', -1, l.latest))
        ORDER BY m.month DESC
    """)
    return cur.fetchall()


# --- Headline metrics ---
st.subheader("Headline Metrics")

rows = get_headline_metrics()

if len(rows) >= 2:
    curr, prev = rows[0], rows[1]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue",    f"${curr[1]:,.0f}",  f"${curr[1] - prev[1]:+,.0f}")
    col2.metric("Total Orders",     f"{curr[2]:,}",      f"{curr[2] - prev[2]:+,}")
    col3.metric("Avg Order Value",  f"${curr[3]:.2f}",   f"${curr[3] - prev[3]:+.2f}")
    col4.metric("Items Sold",       f"{curr[4]:,}",      f"{curr[4] - prev[4]:+,}")
elif len(rows) == 1:
    curr = rows[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue",   f"${curr[1]:,.0f}")
    col2.metric("Total Orders",    f"{curr[2]:,}")
    col3.metric("Avg Order Value", f"${curr[3]:.2f}")
    col4.metric("Items Sold",      f"{curr[4]:,}")

# --- Smoke test ---
st.divider()
count = get_product_count()
st.metric("Products (row count)", count)
