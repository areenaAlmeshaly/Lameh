#.  /Users/areena/Desktop/HR_Attrition_Project/IBM Data.csv
#  /Users/areena/Desktop/dirty_cafe_sales.csv
# /Users/areena/Desktop/marketing_campaign.csv
import pandas as pd
from file_loader import load_file
from data_overview import data_summary
from schema_detection import detect_numeric
from schema_detection import classify_columns 
from cleaning_data import turning_categ
from cleaning_data import is_ID
from cleaning_data import not_full_num
from cleaning_data import null_val

file_path = input("Enter your file path: ")
df=load_file(file_path)

data_size, columns_Info, duplicates, missing_values = data_summary(df)
print(data_summary(df))
print("----------------------")
info=detect_numeric(df)

print("----------------------")
print(classify_columns(df,info))
review=classify_columns(df,info)
df=turning_categ(df,review)
print("----------------------")
print(is_ID(df,review))
print("----------------------")
df=not_full_num(df,review)
print("----------------------")
deal_cols,df=null_val(df,missing_values)
print(df.dtypes)