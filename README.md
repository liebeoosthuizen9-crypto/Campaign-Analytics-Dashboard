# Campaign Analytics Dashboard

A full marketing analytics pipeline tracking 10+ channels and $50,000+ in campaign spend. Built with Python and SQL, designed for Tableau dashboard integration.

---

## Overview

This project simulates a real-world marketing analytics workflow — from raw data ingestion and cleaning through to KPI tracking, segmentation analysis, funnel modelling, and visualisation. It was built to mirror the kind of analysis performed during a marketing analytics internship, where data-driven decisions directly impacted budget allocation and campaign ROI.

**Key results:**
- Identified highest and lowest ROI channels across a $50,000+ campaign budget
- Reduced simulated customer acquisition cost (CAC) by 15% through channel reallocation
- Built a KPI framework tracking CTR, CVR, CAC, ROI, and ROAS across 10 channels

---

## Project Structure

```
Campaign-Analytics-Dashboard/
│
├── data/
│   ├── campaign_data_raw.csv        # Raw generated campaign data
│   └── campaign_data_clean.csv      # Cleaned and structured dataset
│
├── outputs/
│   ├── channel_roi.png              # ROI by channel bar chart
│   ├── spend_vs_revenue.png         # Spend vs revenue by channel
│   ├── monthly_trend.png            # Monthly spend, revenue & ROI trend
│   ├── cac_by_channel.png           # CAC by channel
│   └── funnel.png                   # Marketing funnel visualisation
│
├── generate_data.py                 # Simulates 500 rows of campaign data
├── clean_data.py                    # Data cleaning and feature engineering
├── analysis.py                      # KPI calculations, segmentation, plots
├── queries.sql                      # SQL queries for all KPI metrics
└── README.md
```

---

## KPIs Tracked

| KPI | Description |
|-----|-------------|
| CTR | Click-through rate (clicks / impressions) |
| CVR | Conversion rate (conversions / clicks) |
| CAC | Customer acquisition cost (spend / conversions) |
| ROI | Return on investment ((revenue - spend) / spend) |
| ROAS | Return on ad spend (revenue / spend) |
| Spend Share vs Revenue Share | Budget efficiency gap per channel |

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl

# 2. Create data folder
mkdir data outputs

# 3. Generate simulated data
python generate_data.py

# 4. Clean the data
python clean_data.py

# 5. Run analysis and generate charts
python analysis.py
```

---

## SQL

The `queries.sql` file contains 8 queries covering:
- Overall KPI summary
- Channel performance ranked by ROI
- Campaign performance
- Monthly trend analysis
- Regional segmentation
- Funnel analysis
- Top 10 ROI combinations
- Budget allocation efficiency

Run against any SQLite or SQL database after loading `campaign_data_clean.csv` as a table.

---

## Skills Demonstrated

`Python` `Pandas` `NumPy` `Matplotlib` `Seaborn` `SQL` `Data Cleaning` `KPI Tracking` `Funnel Analysis` `Segmentation` `A/B Testing` `Tableau`

---

## Author

**Liebe Oosthuizen**  
linkedin.com/in/liebe-oosthuizen/
