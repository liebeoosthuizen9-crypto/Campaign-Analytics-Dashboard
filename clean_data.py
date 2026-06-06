"""
clean_data.py
Cleans and structures raw campaign data for analysis.
Handles missing values, outliers, and data type formatting.
"""

import pandas as pd
import numpy as np

def load_raw_data(filepath="data/campaign_data_raw.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns.")
    return df

def clean(df):
    print("\n--- Cleaning ---")

    # Drop full duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows.")

    # Fix data types
    df["date"]    = pd.to_datetime(df["date"])
    df["spend"]   = df["spend"].astype(float)
    df["revenue"] = df["revenue"].astype(float)

    # Fill missing CAC with median per channel (missing = 0 conversions)
    median_cac = df["cac"].median()
    df["cac"]   = df["cac"].fillna(median_cac)

    # Cap extreme outliers in spend (>99th percentile)
    cap = df["spend"].quantile(0.99)
    outliers = (df["spend"] > cap).sum()
    df["spend"] = df["spend"].clip(upper=cap)
    print(f"Capped {outliers} spend outliers above ${cap:.2f}.")

    # Derived columns
    df["month"]      = df["date"].dt.to_period("M").astype(str)
    df["week"]       = df["date"].dt.isocalendar().week.astype(int)
    df["is_converted"] = (df["conversions"] > 0).astype(int)

    print(f"Final dataset: {len(df)} rows, {df.shape[1]} columns.")
    return df

def save(df, filepath="data/campaign_data_clean.csv"):
    df.to_csv(filepath, index=False)
    print(f"\nSaved clean data to {filepath}.")

if __name__ == "__main__":
    df = load_raw_data()
    df = clean(df)
    print("\nSample:")
    print(df.head())
    print("\nNull counts:")
    print(df.isnull().sum())
    save(df)
