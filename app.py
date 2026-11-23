"""Streamlit dashboard — run with:  streamlit run app.py
Needs: pip install streamlit plotly pandas
If Streamlit is not installed, open dashboard.html instead —
it has the same KPIs and charts, no server needed.
"""
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard — Superstore", layout="wide")
st.title("🛒 Sales Analysis Dashboard — Superstore")
st.write("By Md Emon Rana | 9,994 order lines | 2015-01-03 to 2018-12-30")

df = pd.read_csv("data/superstore_clean.csv", parse_dates=["Order Date"])
df["Year"] = df["Order Date"].dt.year

cat = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
year = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
d = df[df["Category"].isin(cat) & df["Region"].isin(region) & df["Year"].isin(year)]

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"${d['Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${d['Profit'].sum():,.0f}")
c3.metric("Orders", f"{d['Order ID'].nunique():,}")

monthly = d.groupby(d["Order Date"].dt.to_period("M").astype(str))["Sales"].sum().reset_index()
st.plotly_chart(px.line(monthly, x="Order Date", y="Sales", title="Monthly Sales Trend"), use_container_width=True)
st.plotly_chart(px.bar(d.groupby("Category")["Sales"].sum().reset_index(), x="Category", y="Sales", title="Sales by Category"), use_container_width=True)
st.plotly_chart(px.bar(d.groupby("Region")["Profit"].sum().reset_index(), x="Region", y="Profit", title="Profit by Region"), use_container_width=True)
st.dataframe(d.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10))
