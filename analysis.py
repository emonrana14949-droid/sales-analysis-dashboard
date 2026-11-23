"""
Sales Analysis Dashboard — Superstore Sales
By Md Emon Rana, CSE, Southeast University

What I did here:
- Loaded the Sample Superstore data (9,994 order lines, 2015-2018)
- Cleaned it (dates, missing postal codes)
- Found which category / region / product makes money, and where
  discount eats the profit
- Saved 6 charts + a clean CSV for Power BI

Run:  python analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "superstore.csv")
OUT = os.path.join(BASE, "outputs")
os.makedirs(OUT, exist_ok=True)
plt.style.use("ggplot")

# 1. Load
df = pd.read_csv(DATA, encoding="latin-1")
print("rows, cols:", df.shape)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin %"] = df["Profit"] / df["Sales"].replace(0, np.nan) * 100

# 2. Clean — only 11 Postal Code values are missing, nothing else.
# I leave them blank, I do not fill them with a made-up code.
print("missing values:\n", df.isna().sum()[df.isna().sum() > 0])
clean = df.copy()
clean.to_csv(os.path.join(BASE, "data", "superstore_clean.csv"), index=False)

# 3. KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order ID"].nunique()
margin = total_profit / total_sales * 100
print(f"Total sales: ${total_sales:,.0f}")
print(f"Total profit: ${total_profit:,.0f}  (margin {margin:.2f}%)")
print(f"Orders: {orders}, order lines: {len(df)}")
print(f"Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")

by_cat = df.groupby("Category").agg(sales=("Sales", "sum"), profit=("Profit", "sum"), lines=("Sales", "size")).sort_values("sales", ascending=False)
by_region = df.groupby("Region").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).sort_values("sales", ascending=False)
by_sub = df.groupby("Sub-Category").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).sort_values("sales", ascending=False)
by_month = df.groupby("Month").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).reset_index()
top_products = df.groupby("Product Name").agg(sales=("Sales", "sum"), profit=("Profit", "sum"), qty=("Quantity", "sum")).sort_values("sales", ascending=False).head(10)
loss_products = df.groupby("Product Name").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).sort_values("profit").head(10)
discount_bins = pd.cut(df["Discount"], bins=[-0.01, 0, 0.2, 0.4, 0.8], labels=["0%", "1-20%", "21-40%", "41-80%"])
disc = df.groupby(discount_bins, observed=True).agg(sales=("Sales", "sum"), profit=("Profit", "sum"), lines=("Sales", "size"))
print("\nBy category:\n", by_cat)
print("\nBy region:\n", by_region)
print("\nTop 5 sub-categories:\n", by_sub.head())
print("\nDiscount vs profit:\n", disc)

with open(os.path.join(OUT, "results.txt"), "w") as f:
    f.write("SALES ANALYSIS DASHBOARD — RESULTS\n")
    f.write("Dataset: Sample Superstore, 9,994 order lines, 2015-01-03 to 2018-12-30\n")
    f.write(f"Total sales: ${total_sales:,.2f}\nTotal profit: ${total_profit:,.2f} (margin {margin:.2f}%)\n")
    f.write(f"Orders: {orders}, order lines: {len(df)}\n\n")
    f.write("SALES BY CATEGORY\n" + by_cat.to_string() + "\n\n")
    f.write("PROFIT BY REGION\n" + by_region.to_string() + "\n\n")
    f.write("TOP 10 PRODUCTS BY SALES\n" + top_products.to_string() + "\n\n")
    f.write("10 MOST LOSS-MAKING PRODUCTS\n" + loss_products.to_string() + "\n\n")
    f.write("DISCOUNT VS PROFIT\n" + disc.to_string() + "\n\n")
    f.write("MONTHLY SALES (first 12 months)\n" + by_month.head(12).to_string(index=False) + "\n")

# 4. Charts
def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=150)
    plt.close(fig)
    print("saved", name)

# 1 monthly trend
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pd.to_datetime(by_month["Month"]), by_month["sales"], marker="o", ms=3)
ax.set_title("Monthly Sales Trend (2015-2018)"); ax.set_ylabel("Sales ($)")
save(fig, "01_monthly_sales_trend.png")

# 2 sales by category
fig, ax = plt.subplots(figsize=(8, 4))
by_cat["sales"].plot(kind="bar", ax=ax, color=["#2563eb", "#059669", "#d97706"])
ax.set_title("Sales by Category"); ax.set_ylabel("Sales ($)")
save(fig, "02_sales_by_category.png")

# 3 profit by region
fig, ax = plt.subplots(figsize=(8, 4))
by_region["profit"].plot(kind="bar", ax=ax, color="#059669")
ax.set_title("Profit by Region"); ax.set_ylabel("Profit ($)")
save(fig, "03_profit_by_region.png")

# 4 top 10 products
fig, ax = plt.subplots(figsize=(10, 5))
top_products["sales"].sort_values().plot(kind="barh", ax=ax, color="#2563eb")
ax.set_title("Top 10 Products by Sales"); ax.set_xlabel("Sales ($)")
save(fig, "04_top10_products.png")

# 5 discount vs profit
fig, ax = plt.subplots(figsize=(8, 4))
disc["profit"].plot(kind="bar", ax=ax, color="#dc2626")
ax.set_title("Profit by Discount Level — high discount = loss"); ax.set_ylabel("Profit ($)")
save(fig, "05_discount_vs_profit.png")

# 6 sales distribution
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["Sales"], bins=50, color="#2563eb")
ax.set_title("Distribution of Sales per Order Line"); ax.set_xlabel("Sales ($)")
save(fig, "06_sales_distribution.png")

# 7 profit margin by sub-category (extra, used in dashboard)
fig, ax = plt.subplots(figsize=(10, 5))
sub_margin = df.groupby("Sub-Category")["Profit"].sum().sort_values()
sub_margin.plot(kind="barh", ax=ax, color="#059669")
ax.set_title("Profit by Sub-Category"); ax.set_xlabel("Profit ($)")
save(fig, "07_profit_by_subcategory.png")

print("Done. Charts in outputs/, clean data in data/superstore_clean.csv")
