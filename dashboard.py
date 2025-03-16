import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection details
DB_CONN = {
    "host": "localhost",
    "database": "ecommerce_dw",
    "user": "airflow",
    "password": "airflow",
    "port": 5432,
}

# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = psycopg2.connect(**DB_CONN)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI
st.title("📊 E-Commerce Data Dashboard")

# Revenue by Product
st.subheader("💰 Total Revenue by Product")
query = """
    SELECT p.name AS product_name, SUM(fs.total_price) AS total_revenue
    FROM fact_sales fs
    JOIN products p ON fs.product_id = p.product_id
    GROUP BY p.name
    ORDER BY total_revenue DESC;
"""
df_revenue = fetch_data(query)
fig, ax = plt.subplots()
sns.barplot(x="total_revenue", y="product_name", data=df_revenue, ax=ax)
st.pyplot(fig)

# Sales Trend
st.subheader("📈 Monthly Sales Trend")
query = """
    SELECT DATE_TRUNC('month', sale_date) AS sale_month, SUM(total_price) AS monthly_sales
    FROM fact_sales
    GROUP BY sale_month
    ORDER BY sale_month;
"""
df_trend = fetch_data(query)
fig, ax = plt.subplots()
ax.plot(df_trend["sale_month"], df_trend["monthly_sales"], marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")
st.pyplot(fig)

st.write("📌 **Dashboard Created using Streamlit**")

