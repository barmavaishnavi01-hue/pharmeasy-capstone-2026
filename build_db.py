import pandas as pd
import sqlite3
regions_df=pd.read_csv("/content/regions_master.csv")
orders_df=pd.read_csv("/content/orders_clean.csv")
conn=sqlite3.connect("pharmeasy.db")
regions_table=regions_df.to_sql("regions_master",conn,if_exists="replace",index=False)
orders_table=orders_df.to_sql("orders_clean",conn,if_exists="replace",index=False)
conn.close()
print("Database created successfully:pharmeasy.db")
print("region_master rows:",len(regions_df))
print("orders_clean rows:",len(orders_df))

