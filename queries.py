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
conn.close()
