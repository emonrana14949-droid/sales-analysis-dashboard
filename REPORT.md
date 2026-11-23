# Sales Analysis Dashboard — Superstore Sales: Short Report

**Md Emon Rana, BSc CSE, Southeast University, Dhaka**

## 1. Introduction
A shop needs to know three things: what sells, what earns, and what loses money.
This project answers that from 9,994 order lines of the Sample Superstore
dataset (2015–2018), with a dashboard anyone can open in a browser.

## 2. Data
Source: Sample Superstore, Tableau sample data (public mirror,
nadeem-majeedch/Machine-Learning-Pipeline-Step-by-Step, 08-Sales-Forecasting).
9,994 rows, 21 columns: Order Date, Category, Sub-Category, Product Name,
Region, Sales, Quantity, Discount, Profit, and more.
Date range 2015-01-03 to 2018-12-30, United States only.
Only 11 Postal Code values are missing; they were left blank.
Honest note: this is Tableau's sample dataset, not a real shop's live
transactions, so results show the method, not a real market.

## 3. Method
Python + Pandas for cleaning and grouping, Matplotlib for charts,
Plotly for the interactive dashboard, Streamlit for the app version.
Steps: load → parse dates → clean (no invented values) → group by
category / region / sub-category / month / discount → KPIs and charts.
The cleaned file is saved as `data/superstore_clean.csv` for Power BI.

## 4. Results
- Total sales **$2,297,201**, total profit **$286,397**, margin **12.47%**,
  5,009 orders.
- By category: Technology $836,154 sales / $145,455 profit;
  Furniture $741,999 / $18,451; Office Supplies $719,047 / $122,491.
- By region: West $725,458 / $108,418 profit; East $678,781 / $91,523;
  Central $501,240 / $39,706; South $391,722 / $46,749.
- Top sub-categories: Phones $330,007, Chairs $328,449, Tables $206,966
  (Tables profit **−$17,725**).
- Top product: Canon imageCLASS 2200 Copier, $61,600 sales.
- Discount vs profit: 0% → +$320,988; 1–20% → +$100,785;
  21–40% → −$35,817; 41–80% → −$99,559.
- Monthly sales rise in September–December each year (holiday season).

## 5. What to do next
Push Technology, re-price Furniture (especially Tables), and cap discounts
at 20% — deep discounts are the biggest profit leak in this data.

## 6. Limitations
Sample (not real) data; US only; 2015–2018, so prices and habits are old;
no cost, marketing, or stock data, so I cannot say *why* a product lost money,
only *that* it did. No forecasting was claimed — this is descriptive analysis.
