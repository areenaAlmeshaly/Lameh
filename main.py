#.  /Users/areena/Desktop/HR_Attrition_Project/IBM Data.csv
#  /Users/areena/Desktop/dirty_cafe_sales.csv
import pandas as pd
from file_loader import load_file
from data_overview import data_summary
from schema_detection import detect_numeric
from schema_detection import detect_date 
from schema_detection import detect_categoral 

file_path = input("Enter your file path: ")
df=load_file(file_path)

data_size, columns_Info, duplicates, missing_values = data_summary(df)
print(data_summary(df))
print("----------------------")
print(detect_numeric(df))
print("----------------------")
print(detect_date(df))
print("----------------------")
print(detect_categoral(df))