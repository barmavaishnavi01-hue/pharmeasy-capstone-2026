##Data quality report

#Uniqueness:
-The raw dataset pharmeasy_orders_raw.csv contains 59 duplicate records.
-These duplicate records are identified during data cleaning.
#Consistency:
-Some regions in raw dataset have inconsistent formatting.
 -Like examples include:
'hyderabad'
'HYDERABAD'
 'hyderabad'
'Bengaluru''
'BENGALURU'
which are identified during data cleaning.
-These are consistency issues which are represented in different formats.
#Completeness:
-The raw dataset contains 48 missing category values in category column.
-The raw dataset contains 94 missing values in profit_inr column which are identified during data cleaning.

#Zero-order region:
-'Kurnool'is present in the region_master.csv but has zero orders in pharmacy_orders_raw.csv.
-This is intentional condition in the dataset and not considered as a data_quality error.



