SELECT
    campaign_id,
    channel,
    DATE(campaign_date) AS date,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    SUM(cost) AS total_cost
FROM campaign_metrics
GROUP BY campaign_id, channel, date
ORDER BY date;