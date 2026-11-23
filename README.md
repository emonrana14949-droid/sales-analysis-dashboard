# 🛒 Sales Analysis Dashboard — Superstore

Hi, I am **Md Emon Rana**, CSE student at Southeast University, Dhaka.
I built this to answer a simple business question: **which products make money,
and where does discount eat the profit?**

## What I found (real numbers, from the data)

| KPI | Value |
|---|---|
| Total sales | **$2,297,201** |
| Total profit | **$286,397** (margin 12.47%) |
| Orders | 5,009 (9,994 order lines) |
| Date range | 2015-01-03 to 2018-12-30 |

- **Technology** sells most ($836k) and earns most ($145k profit).
- **Furniture** sells $742k but keeps only **$18k** — Tables alone lose **$17,725**.
- **West** is the best region ($725k sales, $108k profit); Central is weakest on profit.
- **Discount is the killer:** 0% discount lines made $320,988 profit, but
  21–40% discount lost $35,817 and 41–80% discount lost **$99,559**.
- Top product: **Canon imageCLASS 2200 Copier — $61,600 sales**.

So the fix is simple: push Technology, fix Furniture pricing, stop deep discounts.

## Dataset — honest note

**Sample Superstore** (Tableau sample data, public mirror):
https://github.com/nadeem-majeedch/Machine-Learning-Pipeline-Step-by-Step/blob/main/08-Sales-Forecasting/data/superstore.csv
— 9,994 rows, 21 columns, US retail, 2015–2018.
It is Tableau's well-known *sample* dataset, not a real shop's live transactions,
so the findings show the method, not a real market. Only 11 Postal Code values
are missing; I left them blank, I did not fill them in.

## How to run

```bash
pip install -r requirements.txt
python analysis.py          # EDA + 7 charts in outputs/, results in outputs/results.txt
python dashboard.py         # builds dashboard.html — open it in a browser, no server needed
streamlit run app.py        # interactive dashboard (needs streamlit installed)
```

Or open the notebook — it runs the same steps in Jupyter:

```bash
jupyter notebook analysis.ipynb
```

## Power BI

The cleaned file `data/superstore_clean.csv` is ready for Power BI:
Get Data → Text/CSV → pick that file → build the same visuals
(Sales by Category, Profit by Region, Monthly Trend, Discount vs Profit).

## Files

```
analysis.py            # full analysis, run it first
analysis.ipynb         # same steps in Jupyter, easy words
app.py                 # Streamlit dashboard (Category / Region / Year filters)
dashboard.py           # builds the interactive Plotly dashboard.html
dashboard.html         # open in browser — KPIs + interactive charts
data/superstore.csv    # original data (as downloaded)
data/superstore_clean.csv
outputs/               # 7 charts + results.txt
REPORT.md              # short report
```

## Skills used
Python, Pandas, Matplotlib, Plotly, Streamlit, Power BI, Excel
