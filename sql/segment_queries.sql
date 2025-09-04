
-- Create table for consumer_survey
CREATE TABLE consumer_survey (
    id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50),
    age_group VARCHAR(20),
    order_frequency_per_week INT,
    avg_spend_inr INT,
    cuisine_preference VARCHAR(50),
    order_time VARCHAR(20),
    uses_subscription TINYINT,
    prefers_veg TINYINT,
    orders_via VARCHAR(20)
);

-- Load data (adjust LOCAL INFILE path as needed)
-- NOTE: Ensure MySQL is configured with: local_infile=1
-- Example:
-- LOAD DATA LOCAL INFILE 'PATH/TO/raw_survey_data.csv'
-- INTO TABLE consumer_survey
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 LINES
-- (@respondent_id, city, age_group, order_frequency_per_week, avg_spend_inr, cuisine_preference, order_time, uses_subscription, prefers_veg, orders_via)
-- SET city=city, age_group=age_group, order_frequency_per_week=order_frequency_per_week, avg_spend_inr=avg_spend_inr, cuisine_preference=cuisine_preference, order_time=order_time, uses_subscription=uses_subscription, prefers_veg=prefers_veg, orders_via=orders_via;

-- 1) Most profitable segment by age
SELECT age_group, ROUND(AVG(avg_spend_inr),2) AS avg_spend
FROM consumer_survey
GROUP BY age_group
ORDER BY avg_spend DESC;

-- 2) Peak ordering window
SELECT order_time, ROUND(AVG(order_frequency_per_week),2) AS avg_orders
FROM consumer_survey
GROUP BY order_time
ORDER BY avg_orders DESC;

-- 3) Cuisine share
SELECT cuisine_preference, COUNT(*) AS cnt
FROM consumer_survey
GROUP BY cuisine_preference
ORDER BY cnt DESC;

-- 4) Subscription propensity by age group
SELECT age_group, ROUND(100*AVG(uses_subscription),1) AS subscription_pct
FROM consumer_survey
GROUP BY age_group
ORDER BY subscription_pct DESC;

-- 5) Story recommendation signals
-- Late-night demand spike if 'Late Night' avg orders >= Dinner avg * 0.7
WITH freq AS (
    SELECT order_time, ROUND(AVG(order_frequency_per_week),2) AS avg_orders
    FROM consumer_survey GROUP BY order_time
)
SELECT 
    CASE WHEN (SELECT avg_orders FROM freq WHERE order_time='Late Night') >= 0.7 * (SELECT avg_orders FROM freq WHERE order_time='Dinner')
         THEN 'Story: Youth culture and the rise of late-night food economy in Bengaluru.'
         ELSE 'Story: Dinner-time remains dominant—battle for meal-time mindshare.' END AS story_hint;
