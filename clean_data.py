import pandas as pd
df=pd.read_csv("/content/pharmeasy_orders_raw.csv")
#Remove exact duplicate rows
before=len(df)
df=df.drop_duplicates().copy()
duplicates_removed=before-len(df)
print("Duplicates Removed:",duplicates_removed)
#Normalize Region column
df["region"]=df["region"].str.strip().str.title()
print(len(df))
#Impute missing category using a product
product_category_lookup=(df.dropna(subset=["category"]).drop_duplicates(subset=["product"]).set_index("product")["category"].to_dict())
#Fill missing category
df["category"]=df["category"].fillna(df["product"].map(product_category_lookup))
#Impute missing profit_inr
#calculate profit margin for rows where profit is available
df["profit_margin"]=df["profit_inr"]/df["sales_inr"]
category_mean_margin=(df.dropna(subset=["profit_margin"]).groupby("category")["profit_margin"].mean())
missing_profit=df["profit_inr"].isna()
print("Missing profit rows:", missing_profit.sum())
df.loc[missing_profit, "profit_inr"] = (
    df.loc[missing_profit, "sales_inr"]
    * df.loc[missing_profit, "category"].map(category_mean_margin)
).round(2)
df=df.drop(columns=["profit_margin"])
#save the cleaned dataset
df.to_csv("orders_clean.csv",index=False)
print("clean dataset saved as orders_clean.csv")
print("Total number of rows:",len(df))
print("Total number of columns:",len(df.columns))
df=pd.read_csv("/content/orders_clean.csv")
def validate_schema(df,required_columns):
  missing_columns=[column for column in required_columns if column not in df.columns]
  if missing_columns:
    status="blocked_schema"
  else:
    status="validated"
  return{

    "status":status,
    "row_count":len(df),
    "missing_columns":missing_columns
}
required_columns=["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]
result=validate_schema(df,required_columns)
print(result)
broken_df=df.copy()
broken_df=broken_df.drop(columns=["sales_inr"])
broken_result=validate_schema(broken_df,required_columns)
print(broken_result)
