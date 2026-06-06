-- =============================================================================
-- Campaign Analytics Dashboard — SQL Queries
-- Author: Liebe Oosthuizen
-- Description: Core KPI queries for marketing campaign performance analysis
-- =============================================================================


-- =============================================================================
-- 1. OVERALL KPI SUMMARY
-- =============================================================================
SELECT
    COUNT(*)                                                        AS total_records,
    ROUND(SUM(spend), 2)                                           AS total_spend,
    ROUND(SUM(revenue), 2)                                         AS total_revenue,
    SUM(conversions)                                                AS total_conversions,
    SUM(clicks)                                                     AS total_clicks,
    SUM(impressions)                                                AS total_impressions,
    ROUND(SUM(clicks)       * 100.0 / SUM(impressions), 2)        AS overall_ctr_pct,
    ROUND(SUM(conversions)  * 100.0 / SUM(clicks), 2)             AS overall_cvr_pct,
    ROUND(AVG(cac), 2)                                             AS avg_cac,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS overall_roi_pct,
    ROUND(SUM(revenue) / SUM(spend), 2)                            AS roas
FROM campaign_data;


-- =============================================================================
-- 2. CHANNEL PERFORMANCE — ROI, CAC, ROAS RANKED
-- =============================================================================
SELECT
    channel,
    ROUND(SUM(spend), 2)                                           AS total_spend,
    ROUND(SUM(revenue), 2)                                         AS total_revenue,
    SUM(conversions)                                                AS total_conversions,
    ROUND(AVG(cac), 2)                                             AS avg_cac,
    ROUND(SUM(clicks) * 100.0 / SUM(impressions), 2)              AS ctr_pct,
    ROUND(SUM(conversions) * 100.0 / SUM(clicks), 2)              AS cvr_pct,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS roi_pct,
    ROUND(SUM(revenue) / SUM(spend), 2)                            AS roas
FROM campaign_data
GROUP BY channel
ORDER BY roi_pct DESC;


-- =============================================================================
-- 3. CAMPAIGN PERFORMANCE SUMMARY
-- =============================================================================
SELECT
    campaign,
    ROUND(SUM(spend), 2)                                           AS total_spend,
    ROUND(SUM(revenue), 2)                                         AS total_revenue,
    SUM(conversions)                                                AS total_conversions,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS roi_pct,
    ROUND(SUM(revenue) / SUM(spend), 2)                            AS roas
FROM campaign_data
GROUP BY campaign
ORDER BY roi_pct DESC;


-- =============================================================================
-- 4. MONTHLY TREND — SPEND, REVENUE, ROI
-- =============================================================================
SELECT
    strftime('%Y-%m', date)                                        AS month,
    ROUND(SUM(spend), 2)                                           AS total_spend,
    ROUND(SUM(revenue), 2)                                         AS total_revenue,
    SUM(conversions)                                                AS total_conversions,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS roi_pct
FROM campaign_data
GROUP BY month
ORDER BY month;


-- =============================================================================
-- 5. REGIONAL SEGMENTATION
-- =============================================================================
SELECT
    region,
    ROUND(SUM(spend), 2)                                           AS total_spend,
    ROUND(SUM(revenue), 2)                                         AS total_revenue,
    SUM(conversions)                                                AS total_conversions,
    ROUND(AVG(cac), 2)                                             AS avg_cac,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS roi_pct
FROM campaign_data
GROUP BY region
ORDER BY roi_pct DESC;


-- =============================================================================
-- 6. FUNNEL ANALYSIS — IMPRESSIONS → CLICKS → CONVERSIONS
-- =============================================================================
SELECT
    channel,
    SUM(impressions)                                               AS impressions,
    SUM(clicks)                                                    AS clicks,
    SUM(conversions)                                               AS conversions,
    ROUND(SUM(clicks)      * 100.0 / SUM(impressions), 2)        AS impression_to_click_pct,
    ROUND(SUM(conversions) * 100.0 / SUM(clicks), 2)             AS click_to_conversion_pct
FROM campaign_data
GROUP BY channel
ORDER BY click_to_conversion_pct DESC;


-- =============================================================================
-- 7. TOP 10 HIGHEST ROI CAMPAIGN + CHANNEL COMBINATIONS
-- =============================================================================
SELECT
    campaign,
    channel,
    ROUND(SUM(spend), 2)                                           AS spend,
    ROUND(SUM(revenue), 2)                                         AS revenue,
    SUM(conversions)                                                AS conversions,
    ROUND((SUM(revenue) - SUM(spend)) * 100.0 / SUM(spend), 2)   AS roi_pct
FROM campaign_data
GROUP BY campaign, channel
HAVING SUM(conversions) > 0
ORDER BY roi_pct DESC
LIMIT 10;


-- =============================================================================
-- 8. BUDGET ALLOCATION EFFICIENCY — SPEND SHARE VS REVENUE SHARE
-- =============================================================================
SELECT
    channel,
    ROUND(SUM(spend), 2)                                                       AS spend,
    ROUND(SUM(spend) * 100.0 / SUM(SUM(spend)) OVER (), 2)                    AS spend_share_pct,
    ROUND(SUM(revenue), 2)                                                     AS revenue,
    ROUND(SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 2)                AS revenue_share_pct,
    ROUND(
        SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER ()
        - SUM(spend) * 100.0 / SUM(SUM(spend)) OVER ()
    , 2)                                                                       AS efficiency_gap_pct
FROM campaign_data
GROUP BY channel
ORDER BY efficiency_gap_pct DESC;
