"""
generate_data.py
Generates simulated marketing campaign data for the Campaign Analytics Dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

CHANNELS = [
    "Google Search", "Google Display", "Facebook", "Instagram",
    "Email", "YouTube", "TikTok", "LinkedIn", "Referral", "Organic"
]

REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]

CAMPAIGNS = [
    "Brand Awareness Q1", "Lead Gen Spring", "Retargeting Summer",
    "Back to School", "Product Launch Oct", "Holiday Push Q4"
]

rows = []
start_date = datetime(2024, 1, 1)

for i in range(500):
    channel = random.choice(CHANNELS)
    region  = random.choice(REGIONS)
    campaign = random.choice(CAMPAIGNS)
    date = start_date + timedelta(days=random.randint(0, 364))

    impressions = int(np.random.lognormal(mean=8.5, sigma=1.2))
    ctr         = round(np.random.beta(2, 40), 4)
    clicks      = max(1, int(impressions * ctr))
    cpc         = round(np.random.uniform(0.5, 4.5), 2)
    spend       = round(clicks * cpc, 2)
    conv_rate   = round(np.random.beta(1.5, 20), 4)
    conversions = max(0, int(clicks * conv_rate))
    revenue     = round(conversions * np.random.uniform(25, 120), 2)
    cac         = round(spend / conversions, 2) if conversions > 0 else None
    roi         = round((revenue - spend) / spend * 100, 2) if spend > 0 else 0

    rows.append({
        "date": date.strftime("%Y-%m-%d"),
        "campaign": campaign,
        "channel": channel,
        "region": region,
        "impressions": impressions,
        "clicks": clicks,
        "ctr": ctr,
        "cpc": cpc,
        "spend": spend,
        "conversions": conversions,
        "conversion_rate": conv_rate,
        "revenue": revenue,
        "cac": cac,
        "roi": roi
    })

df = pd.DataFrame(rows)
df.to_csv("data/campaign_data_raw.csv", index=False)
print(f"Generated {len(df)} rows of campaign data.")
print(df.head())
