import sqlite3
conn=sqlite3.connect("pharmeasy.db")
#Row count check-Left Join
left_count=conn.execute("""select count(*) from regions_master r left join orders_clean o on r.region=o.region;""").fetchone()[0]
print("Left join row count:",left_count)
# Row count check-Inner join
inner_count=conn.execute("""select count(*) from regions_master r inner join orders_clean o on r.region=o.region;""").fetchone()[0]
print("Inner join row count:",inner_count)
#Duplicate key check
duplicates=conn.execute("""SELECT order_id,count(*) from orders_clean group by order_id HAVING count(*)>1""").fetchall()
print("Duplicate order_id's:",duplicates)
#Null Check using both count(*) and count(o.order_id)
region_counts=conn.execute("""select r.region,count(*) as count,count(o.order_id) as count_order_id from regions_master r left join orders_clean o on r.region=o.region group by r.region;""").fetchall()
print("orders by region:",region_counts)
#show disagreement
disagreements=conn.execute("""select r.region,count(*) as count,count(o.order_id) as count_order_id from regions_master r left join orders_clean o on r.region=o.region group by r.region having count(*)<>count(o.order_id);""").fetchall()
print("showing disagreement:",disagreements)
#order counts Ascending
order_counts_order=conn.execute("""select r.region,count(o.order_id) as count_order_id from regions_master r left join orders_clean o on r.region=o.region group by r.region order by count_order_id asc;"""
).fetchall()
print("Per region order counts:",order_counts_order)
monthly_sales=conn.execute("SELECT region,strftime('%m', order_date) AS month,ROUND(SUM(sales_inr),2) AS total_sales FROM orders_clean WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01' GROUP BY region, month ORDER BY region, month;""").fetchall()
print("sum of sales:",monthly_sales)
MoM_query=conn.execute("""with monthly_sales as (SELECT
    region,
    strftime('%m', order_date) AS month,
    ROUND(SUM(sales_inr),2) AS total_sales
FROM orders_clean
WHERE order_date >= '2026-04-01'
  AND order_date < '2026-07-01'
GROUP BY region, month
),region_sales as (select region,
      SUM(CASE WHEN month= '04' then total_sales else 0 end) as april_sales,
      SUM(CASE WHEN month= '05' then total_sales else 0 end) as may_sales,
      SUM(CASE WHEN month= '06' then total_sales else 0 end) as june_sales
      from monthly_sales
      group by region
      )select region,april_sales,may_sales,june_sales,ROUND((may_sales-april_sales)/april_sales*100,2) as april_to_may_growth,
                  ROUND((june_sales-may_sales)/may_sales*100,2) as may_to_june_growth
                  from region_sales order by region;""").fetchall()
print("MoM growth%:",MoM_query)
conn.close()
