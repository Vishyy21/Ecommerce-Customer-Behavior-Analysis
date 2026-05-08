-- Total Revenue
SELECT SUM(Total_Spend) AS Total_Revenue
FROM ecommerce;

-- Revenue by Membership Type
SELECT Membership_Type,
       SUM(Total_Spend) AS Total_Revenue,
       AVG(Total_Spend) AS Avg_Spend,
       COUNT(*) AS Customers
FROM ecommerce
GROUP BY Membership_Type
ORDER BY Total_Revenue DESC;

-- City-wise Revenue
SELECT City,
       SUM(Total_Spend) AS Total_Revenue
FROM ecommerce
GROUP BY City
ORDER BY Total_Revenue DESC;

-- Average Ratings by Membership
SELECT Membership_Type,
       ROUND(AVG(Average_Rating), 2) AS Avg_Rating
FROM ecommerce
GROUP BY Membership_Type
ORDER BY Avg_Rating DESC;

-- Retention Segments
SELECT Customer_ID,
       Days_Since_Last_Purchase,
       CASE
         WHEN Days_Since_Last_Purchase <= 15 THEN 'Active'
         WHEN Days_Since_Last_Purchase <= 30 THEN 'Warm'
         WHEN Days_Since_Last_Purchase <= 45 THEN 'At Risk'
         ELSE 'Churned'
       END AS Retention_Segment
FROM ecommerce;

-- Discount Impact
SELECT Discount_Applied,
       COUNT(*) AS Customers,
       ROUND(AVG(Total_Spend), 2) AS Avg_Spend
FROM ecommerce
GROUP BY Discount_Applied;

-- Satisfaction Breakdown
SELECT Satisfaction_Level,
       COUNT(*) AS Customers
FROM ecommerce
GROUP BY Satisfaction_Level;