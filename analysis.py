"""
analysis.py
Core KPI calculations, segmentation analysis, and funnel metrics.
Tracks: CAC, CTR, CVR, ROI, ROAS, spend efficiency across channels and campaigns.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")

def load(filepath="data/campaign_data_clean.csv"):
    return pd.read_csv(filepath, parse_dates=["date"])

# ── KPI SUMMARY ──────────────────────────────────────────────────────────────

def kpi_summary(df):
    total_spend       = df["spend"].sum()
    total_revenue     = df["revenue"].sum()
    total_conversions = df["conversions"].sum()
    total_clicks      = df["clicks"].sum()
    total_impressions = df["impressions"].sum()

    summary = {
        "Total Spend ($)":        round(total_spend, 2),
        "Total Revenue ($)":      round(total_revenue, 2),
        "Total Conversions":      int(total_conversions),
        "Total Clicks":           int(total_clicks),
        "Total Impressions":      int(total_impressions),
        "Overall CTR (%)":        round(total_clicks / total_impressions * 100, 2),
        "Overall CVR (%)":        round(total_conversions / total_clicks * 100, 2),
        "Average CAC ($)":        round(df["cac"].mean(), 2),
        "Overall ROI (%)":        round((total_revenue - total_spend) / total_spend * 100, 2),
        "ROAS":                   round(total_revenue / total_spend, 2),
    }

    print("\n=== KPI SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k:<30} {v}")
    return summary

# ── CHANNEL SEGMENTATION ─────────────────────────────────────────────────────

def channel_performance(df):
    grp = df.groupby("channel").agg(
        spend       =("spend",       "sum"),
        revenue     =("revenue",     "sum"),
        conversions =("conversions", "sum"),
        clicks      =("clicks",      "sum"),
        impressions =("impressions", "sum"),
        avg_cac     =("cac",         "mean"),
    ).reset_index()

    grp["roi"]  = ((grp["revenue"] - grp["spend"]) / grp["spend"] * 100).round(2)
    grp["ctr"]  = (grp["clicks"]      / grp["impressions"] * 100).round(2)
    grp["cvr"]  = (grp["conversions"] / grp["clicks"]       * 100).round(2)
    grp["roas"] = (grp["revenue"]     / grp["spend"]).round(2)
    grp = grp.sort_values("roi", ascending=False)

    print("\n=== CHANNEL PERFORMANCE ===")
    print(grp[["channel","spend","revenue","conversions","roi","avg_cac","roas"]].to_string(index=False))
    return grp

# ── FUNNEL ANALYSIS ───────────────────────────────────────────────────────────

def funnel_analysis(df):
    impressions  = df["impressions"].sum()
    clicks       = df["clicks"].sum()
    conversions  = df["conversions"].sum()

    funnel = pd.DataFrame({
        "Stage":       ["Impressions", "Clicks", "Conversions"],
        "Count":       [impressions, clicks, conversions],
        "Drop-off (%)": [
            0,
            round((1 - clicks / impressions) * 100, 1),
            round((1 - conversions / clicks) * 100, 1)
        ]
    })

    print("\n=== FUNNEL ANALYSIS ===")
    print(funnel.to_string(index=False))
    return funnel

# ── MONTHLY TREND ─────────────────────────────────────────────────────────────

def monthly_trend(df):
    trend = df.groupby("month").agg(
        spend       =("spend",       "sum"),
        revenue     =("revenue",     "sum"),
        conversions =("conversions", "sum"),
    ).reset_index()
    trend["roi"] = ((trend["revenue"] - trend["spend"]) / trend["spend"] * 100).round(2)
    return trend

# ── PLOTS ─────────────────────────────────────────────────────────────────────

def plot_channel_roi(grp):
    fig, ax = plt.subplots(figsize=(10, 5))
    colors  = ["#2ecc71" if r > 0 else "#e74c3c" for r in grp["roi"]]
    ax.barh(grp["channel"], grp["roi"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("ROI (%)")
    ax.set_title("ROI by Channel", fontweight="bold")
    plt.tight_layout()
    plt.savefig("outputs/channel_roi.png", dpi=150)
    plt.close()
    print("Saved: outputs/channel_roi.png")

def plot_spend_vs_revenue(grp):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(grp))
    ax.bar(x, grp["spend"],   label="Spend",   alpha=0.8, color="#3498db")
    ax.bar(x, grp["revenue"], label="Revenue", alpha=0.6, color="#2ecc71")
    ax.set_xticks(x)
    ax.set_xticklabels(grp["channel"], rotation=30, ha="right")
    ax.set_ylabel("USD ($)")
    ax.set_title("Spend vs Revenue by Channel", fontweight="bold")
    ax.legend()
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
    plt.tight_layout()
    plt.savefig("outputs/spend_vs_revenue.png", dpi=150)
    plt.close()
    print("Saved: outputs/spend_vs_revenue.png")

def plot_monthly_trend(trend):
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()
    ax1.bar(trend["month"], trend["spend"],   color="#3498db", alpha=0.6, label="Spend")
    ax1.bar(trend["month"], trend["revenue"], color="#2ecc71", alpha=0.6, label="Revenue")
    ax2.plot(trend["month"], trend["roi"], color="#e74c3c", marker="o", linewidth=2, label="ROI %")
    ax1.set_xticklabels(trend["month"], rotation=45, ha="right")
    ax1.set_ylabel("USD ($)")
    ax2.set_ylabel("ROI (%)")
    ax1.set_title("Monthly Spend, Revenue & ROI", fontweight="bold")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    plt.tight_layout()
    plt.savefig("outputs/monthly_trend.png", dpi=150)
    plt.close()
    print("Saved: outputs/monthly_trend.png")

def plot_cac_by_channel(grp):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(grp["channel"], grp["avg_cac"], color="#9b59b6")
    ax.set_xticklabels(grp["channel"], rotation=30, ha="right")
    ax.set_ylabel("Average CAC ($)")
    ax.set_title("Customer Acquisition Cost by Channel", fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.2f}"))
    plt.tight_layout()
    plt.savefig("outputs/cac_by_channel.png", dpi=150)
    plt.close()
    print("Saved: outputs/cac_by_channel.png")

def plot_funnel(funnel):
    fig, ax = plt.subplots(figsize=(7, 4))
    colors  = ["#3498db", "#2ecc71", "#e67e22"]
    ax.barh(funnel["Stage"][::-1], funnel["Count"][::-1], color=colors)
    ax.set_xlabel("Count")
    ax.set_title("Marketing Funnel: Impressions → Clicks → Conversions", fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    plt.tight_layout()
    plt.savefig("outputs/funnel.png", dpi=150)
    plt.close()
    print("Saved: outputs/funnel.png")

if __name__ == "__main__":
    df     = load()
    kpis   = kpi_summary(df)
    grp    = channel_performance(df)
    funnel = funnel_analysis(df)
    trend  = monthly_trend(df)

    plot_channel_roi(grp)
    plot_spend_vs_revenue(grp)
    plot_monthly_trend(trend)
    plot_cac_by_channel(grp)
    plot_funnel(funnel)

    print("\nAll analysis complete.")
