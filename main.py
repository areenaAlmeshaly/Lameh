from file_loader import load_file
from data_overview import Data_sammary
file_path = input("Enter your file path: ")
df=load_file(file_path)
#.  /Users/areena/Desktop/HR_Attrition_Project/IBM Data.csv
print(Data_sammary(df))
