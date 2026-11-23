"""Build the interactive Plotly dashboard (dashboard.html).
Run: python dashboard.py   then open dashboard.html in a browser.
No server needed — all charts are interactive Plotly charts.
"""
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, "data", "superstore_clean.csv"), parse_dates=["Order Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
orders = df["Order ID"].nunique()

monthly = df.groupby("Month").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).reset_index()
by_cat = df.groupby("Category").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).reset_index()
by_region = df.groupby("Region").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).reset_index()
by_year_cat = df.groupby(["Year", "Category"])["Sales"].sum().reset_index()

# Monthly trend with a Category filter (dropdown switches the line)
fig1 = go.Figure()
for cat in ["All"] + sorted(df["Category"].unique()):
    d = monthly if cat == "All" else df[df["Category"] == cat].groupby("Month").agg(sales=("Sales", "sum")).reset_index()
    fig1.add_trace(go.Scatter(x=d["Month"], y=d["sales"], mode="lines+markers", name=cat, visible=(cat == "All")))
fig1.update_layout(title="Monthly Sales Trend — use the dropdown to filter by Category",
                   updatemenus=[{"buttons": [{"label": c, "method": "update",
                                              "args": [{"visible": [x == c for x in ["All"] + sorted(df["Category"].unique())]}]}
                                             for c in ["All"] + sorted(df["Category"].unique())],
                                "direction": "down", "showactive": True, "x": 0, "y": 1.15}])

fig2 = px.bar(by_cat, x="Category", y="sales", color="Category", title="Sales by Category")
fig3 = px.bar(by_region, x="Region", y="profit", color="Region", title="Profit by Region")
fig4 = px.bar(by_year_cat, x="Year", y="Sales", color="Category", barmode="group",
              title="Sales by Year and Category (filter by year in the legend)")

kpi = f"""
<h1>🛒 Sales Analysis Dashboard — Superstore</h1>
<p>By Md Emon Rana | 9,994 order lines | 2015-01-03 to 2018-12-30 | 5,009 orders</p>
<div style="display:flex;gap:16px">
<div style="background:#2563eb;color:white;padding:16px;border-radius:10px"><b>Total Sales</b><br><span style="font-size:24px">${total_sales:,.0f}</span></div>
<div style="background:#059669;color:white;padding:16px;border-radius:10px"><b>Total Profit</b><br><span style="font-size:24px">${total_profit:,.0f}</span></div>
<div style="background:#d97706;color:white;padding:16px;border-radius:10px"><b>Orders</b><br><span style="font-size:24px">{orders:,}</span></div>
<div style="background:#475569;color:white;padding:16px;border-radius:10px"><b>Profit Margin</b><br><span style="font-size:24px">{total_profit/total_sales*100:.1f}%</span></div>
</div>
<p><b>Main finding:</b> Technology makes the most money ($145k profit). Furniture sells a lot ($742k)
but keeps only $18k — Tables alone lose $17,725. Discounts over 20% lose money: 41–80% discount
lines lost $99,559. So: push Technology, fix Furniture pricing, and stop deep discounts.</p>
"""

html = "<html><head><meta charset='utf-8'><title>Sales Dashboard</title></head><body style='font-family:sans-serif;max-width:1000px;margin:auto;padding:16px'>"
html += kpi
for fig in (fig1, fig2, fig3, fig4):
    html += fig.to_html(full_html=False, include_plotlyjs="cdn")
html += "<p>Source: Sample Superstore dataset (Tableau sample data, public mirror). "
html += "Clean data: data/superstore_clean.csv — rebuild this in Power BI from that file.</p></body></html>"
with open(os.path.join(BASE, "dashboard.html"), "w") as f:
    f.write(html)
print("dashboard.html written")
