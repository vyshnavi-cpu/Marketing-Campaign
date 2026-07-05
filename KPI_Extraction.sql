-- Executed at 16:58:48 (Initial KPI check)
SELECT 
    COUNT(DISTINCT c.customer_id) as total_customers, 
    ROUND(AVG(cr."Response") * 100, 2) || '%' as overall_response_rate, 
    ROUND(AVG(cs.total_spend), 2) as avg_spend_per_customer, 
    ROUND(AVG(ca."NumWebVisitsMonth"), 2) as avg_monthly_web_visits 
FROM customers c 
JOIN campaign_responses cr ON c.customer_id = cr.customer_id 
JOIN customer_spend cs ON c.customer_id = cs.customer_id 
JOIN customer_activity ca ON c.customer_id = ca.customer_id;

-- Executed at 17:20:46 (Refined baseline KPIs)
SELECT 
    COUNT(c.customer_id) AS total_customer_base, 
    ROUND(AVG(s."Total_Spend"), 2) AS average_spend_per_customer, 
    ROUND(AVG(a."NumWebVisitsMonth"), 1) AS average_monthly_web_visits, 
    ROUND((SUM(r."Response") * 100.0 / COUNT(c.customer_id)), 2) AS aggregate_campaign_response_rate_pct 
FROM customers c 
JOIN customer_spend s ON c.customer_id = s.customer_id 
JOIN customer_activity a ON c.customer_id = a.customer_id 
JOIN campaign_responses r ON c.customer_id = r.customer_id;