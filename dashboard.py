import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load database credentials from Streamlit secrets
DB_CONN = st.secrets["database"]

# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = psycopg2.connect(
        host=DB_CONN["host"],
        database=DB_CONN["database"],
        user=DB_CONN["user"],
        password=DB_CONN["password"],
        port=DB_CONN["port"]
    )
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
