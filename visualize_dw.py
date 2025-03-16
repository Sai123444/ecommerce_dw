import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# PostgreSQL Connection Details
DB_CONFIG = {
    "dbname": "ecommerce_dw",
    "user": "airflow",
    "password": "airflow",
    "host": "localhost",
    "port": 5433  # Make sure this is your correct port!
}

# Connect to PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)

# Fetch Data into Pandas DataFrames
queries = {
    "Product Sales": """
        SELECT p.name AS product_name, SUM(fs.total_price) AS total_revenue
        FROM fact_sales fs
        JOIN products p ON fs.product_id = p.product_id
        GROUP BY p.name ORDER BY total_revenue DESC;
    """,
    "Customer Spending": """
        SELECT c.name AS customer_name, SUM(fs.total_price) AS total_spent
        FROM fact_sales fs
        JOIN customers c ON fs.customer_id = c.customer_id
        GROUP BY c.name ORDER BY total_spent DESC LIMIT 5;
    """,
    "Monthly Sales Trend": """
        SELECT DATE_TRUNC('month', sale_date) AS sale_month, SUM(total_price) AS monthly_sales
        FROM fact_sales
        GROUP BY sale_month ORDER BY sale_month;
    """
}

# Load data into DataFrames
dataframes = {name: pd.read_sql(query, conn) for name, query in queries.items()}
conn.close()

# 📊 **1️⃣ Bar Chart: Sales by Product**
plt.figure(figsize=(8, 5))
sns.barplot(x="total_revenue", y="product_name", data=dataframes["Product Sales"], palette="Blues_r")
plt.xlabel("Total Revenue ($)")
plt.ylabel("Product")
plt.title("Total Sales by Product")
plt.show()

# 📊 **2️⃣ Bar Chart: Top 5 Customers by Spending**
plt.figure(figsize=(8, 5))
sns.barplot(x="total_spent", y="customer_name", data=dataframes["Customer Spending"], palette="Greens_r")
plt.xlabel("Total Amount Spent ($)")
plt.ylabel("Customer Name")
plt.title("Top 5 Customers by Spending")
plt.show()

# 📊 **3️⃣ Line Chart: Monthly Sales Trend**
plt.figure(figsize=(8, 5))
sns.lineplot(x="sale_month", y="monthly_sales", data=dataframes["Monthly Sales Trend"], marker="o", color="red")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.show()
