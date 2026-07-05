-- Executed at 16:34:03 / 16:34:13
CREATE TABLE customers ( 
    customer_id INT PRIMARY KEY, 
    year_birth INT, 
    education VARCHAR(50), 
    marital_status VARCHAR(50), 
    income NUMERIC(12, 2), 
    kidhome INT, 
    teenhome INT, 
    dt_customer DATE, 
    recency INT, 
    complain INT, 
    country VARCHAR(50), 
    customer_tenure_days INT, 
    age INT, 
    children INT 
);

-- Executed at 16:35:08
CREATE TABLE campaign_responses ( 
    customer_id INT PRIMARY KEY REFERENCES customers(customer_id) ON DELETE CASCADE, 
    accepted_cmp1 INT, 
    accepted_cmp2 INT, 
    accepted_cmp3 INT, 
    accepted_cmp4 INT, 
    accepted_cmp5 INT, 
    response INT 
);

-- Executed at 16:35:37
CREATE TABLE customer_spend ( 
    customer_id INT PRIMARY KEY REFERENCES customers(customer_id) ON DELETE CASCADE, 
    mnt_wines NUMERIC(10, 2), 
    mnt_fruits NUMERIC(10, 2), 
    mnt_meat_products NUMERIC(10, 2), 
    mnt_fish_products NUMERIC(10, 2), 
    mnt_sweet_products NUMERIC(10, 2), 
    mnt_gold_prods NUMERIC(10, 2), 
    total_spend NUMERIC(12, 2) 
);

-- Executed at 16:36:22
CREATE TABLE customer_activity ( 
    customer_id INT PRIMARY KEY REFERENCES customers(customer_id) ON DELETE CASCADE, 
    num_deals_purchases INT, 
    num_web_purchases INT, 
    num_catalog_purchases INT, 
    num_store_purchases INT, 
    num_web_visits_month INT, 
    total_purchases INT 
);