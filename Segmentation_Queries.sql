-- Executed at 17:22:00 (Initial group by segment execution)
SELECT 
    c."Education", 
    c."Marital_Status", 
    COUNT(c.customer_id) AS total_profiles, 
    ROUND(AVG(c."Income"), 0) AS average_annual_income, 
    ROUND(AVG(s."Total_Spend"), 0) AS average_total_spend, 
    ROUND((SUM(r."Response") * 100.0 / COUNT(c.customer_id)), 2) AS campaign_conversion_rate_pct 
FROM customers c 
JOIN customer_spend s ON c.customer_id = s.customer_id 
JOIN campaign_responses r ON c.customer_id = r.customer_id 
GROUP BY c."Education", c."Marital_Status" 
ORDER BY total_profiles DESC, average_total_spend DESC;

-- Executed at 17:22:34 (Fixed with explicit ::numeric type casting)
SELECT 
    c."Education", 
    c."Marital_Status", 
    COUNT(c.customer_id) AS total_profiles, 
    ROUND(AVG(c."Income")::numeric, 0) AS average_annual_income, 
    ROUND(AVG(s."Total_Spend")::numeric, 0) AS average_total_spend, 
    ROUND((SUM(r."Response") * 100.0 / COUNT(c.customer_id))::numeric, 2) AS campaign_conversion_rate_pct 
FROM customers c 
JOIN customer_spend s ON c.customer_id = s.customer_id 
JOIN campaign_responses r ON c.customer_id = r.customer_id 
GROUP BY c."Education", c."Marital_Status" 
ORDER BY total_profiles DESC, average_total_spend DESC;

-- Executed at 17:23:11 (Geographic, Age, and Income Banding Analysis)
SELECT 
    c."Country", 
    CASE 
        WHEN c."Age" < 35 THEN 'Young Adults (<35)' 
        WHEN c."Age" BETWEEN 35 AND 55 THEN 'Mid-Age Adults (35-55)' 
        ELSE 'Seniors (>55)' 
    END AS age_band, 
    CASE 
        WHEN c."Income" < 40000 THEN 'Low Income (<$40k)' 
        WHEN c."Income" BETWEEN 40000 AND 75000 THEN 'Moderate Income ($40k-$75k)' 
        ELSE 'Premium Income (>$75k)' 
    END AS income_band, 
    COUNT(c.customer_id) AS absolute_customer_count, 
    ROUND(AVG(s."Total_Spend")::numeric, 2) AS group_average_spend, 
    ROUND((SUM(r."Response") * 100.0 / COUNT(c.customer_id))::numeric, 2) AS campaign_conversion_rate_pct 
FROM customers c 
JOIN customer_spend s ON c.customer_id = s.customer_id 
JOIN campaign_responses r ON c.customer_id = r.customer_id 
GROUP BY c."Country", age_band, income_band 
ORDER BY c."Country", absolute_customer_count DESC;