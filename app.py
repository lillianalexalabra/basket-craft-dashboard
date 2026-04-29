import datetime
import os

import pandas as pd
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

@st.cache_data(ttl=600)
def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT PRODUCT_ID, PRODUCT_NAME FROM PRODUCTS ORDER BY PRODUCT_ID")
    return cur.fetchall()


@st.cache_data(ttl=600)
def get_bundles(product_id: int, start_date: datetime.date, end_date: datetime.date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.PRODUCT_NAME, COUNT(DISTINCT oi2.ORDER_ID) AS orders_together
        FROM ORDER_ITEMS oi1
        JOIN ORDER_ITEMS oi2 ON oi1.ORDER_ID = oi2.ORDER_ID
            AND oi1.PRODUCT_ID != oi2.PRODUCT_ID
        JOIN PRODUCTS p ON oi2.PRODUCT_ID = p.PRODUCT_ID
        WHERE oi1.PRODUCT_ID = %s
          AND TO_TIMESTAMP_NTZ(oi1.CREATED_AT, 9)::DATE BETWEEN %s AND %s
        GROUP BY 1
        ORDER BY 2 DESC
    """, (product_id, start_date, end_date))
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["Bought Together With", "Orders"])


@st.cache_data(ttl=600)
def get_top_products(start_date: datetime.date, end_date: datetime.date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.PRODUCT_NAME, SUM(oi.PRICE_USD) AS revenue
        FROM ORDER_ITEMS oi
        JOIN PRODUCTS p ON oi.PRODUCT_ID = p.PRODUCT_ID
        WHERE TO_TIMESTAMP_NTZ(oi.CREATED_AT, 9)::DATE BETWEEN %s AND %s
        GROUP BY 1
        ORDER BY 2 DESC
    """, (start_date, end_date))
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["Product", "Revenue"])


@st.cache_data(ttl=600)
def get_revenue_trend(start_date: datetime.date, end_date: datetime.date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            DATE_TRUNC('month', TO_TIMESTAMP_NTZ(CREATED_AT, 9))::DATE AS month,
            SUM(PRICE_USD) AS revenue
        FROM ORDERS
        WHERE TO_TIMESTAMP_NTZ(CREATED_AT, 9)::DATE BETWEEN %s AND %s
        GROUP BY 1
        ORDER BY 1
    """, (start_date, end_date))
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["Month", "Revenue"])


# --- Revenue trend ---
st.subheader("Revenue Trend")

DATA_START = datetime.date(2023, 3, 19)
DATA_END   = datetime.date(2026, 3, 19)

date_range = st.date_input(
    "Date range",
    value=(DATA_START, DATA_END),
    min_value=DATA_START,
    max_value=DATA_END,
)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    df = get_revenue_trend(date_range[0], date_range[1])
    st.area_chart(df.set_index("Month"), y="Revenue")

    st.subheader("Top Products by Revenue")
    df_products = get_top_products(date_range[0], date_range[1])
    st.bar_chart(df_products, x="Product", y="Revenue")

    st.subheader("Bundle Finder")
    products = get_products()
    name_to_id = {name: pid for pid, name in products}
    selected = st.selectbox("Pick a product", list(name_to_id.keys()))
    df_bundles = get_bundles(name_to_id[selected], date_range[0], date_range[1])
    if df_bundles.empty:
        st.info("No co-purchases found for this product in the selected date range.")
    else:
        st.bar_chart(df_bundles, x="Bought Together With", y="Orders")

# --- Smoke test ---
st.divider()
count = get_product_count()
st.metric("Products (row count)", count)
