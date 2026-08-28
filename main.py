#.  /Users/areena/Desktop/HR_Attrition_Project/IBM Data.csv
#  /Users/areena/Desktop/dirty_cafe_sales.csv
# /Users/areena/Desktop/marketing_campaign.csv
import pandas as pd
from file_loader import load_file
from data_overview import data_summary
from schema_detection import detect_numeric, detect_date, classify_columns
from cleaning_data import(
    turning_categ,
    turning_date,
    is_ID,
    not_full_num,
    null_val,
    duplicate_val,
    null_deal,
    outliers)
from EDA import descr, num_vizual, num_rela, cat_vizual

file_path = input("Enter your file path: ")
df=load_file(file_path)

data_size, columns_Info, duplicates, missing_values = data_summary(df)
print(data_summary(df))
info=detect_numeric(df)
date_info=detect_date(df)


df,review,numric_col,cat_col,ambiguous=classify_columns(df,info,date_info)
print("----------------------")

df,numric_col,cat_col=turning_categ(df,review,numric_col,cat_col)
df=turning_date(df, review)
print("----------------------")
ID=(is_ID(review))
print("----------------------")
df,numric_col=not_full_num(df,review,numric_col)

print("----------------------")
deal_cols,df=null_val(df,missing_values)
print(df.dtypes)
df=duplicate_val(df)
df=null_deal(df,deal_cols,missing_values)
df=outliers(df)
#drop

print(descr(df,ID))
print(num_vizual(df,numric_col))
print(num_rela(df,numric_col))
print(cat_vizual(df,cat_col))