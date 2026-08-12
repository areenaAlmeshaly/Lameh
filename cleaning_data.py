import pandas as pd 
def turning_categ(df,review):
  for item in review:
            if item["reason"] == "Numeric column with few unique values - may be categorical":
                 column = item["column"]
                 dec=input(print("Is",column ,"a categorical column ? (YES)(NO) "))
                 if dec=="YES" and df[column].dtype != "object":
                      df[column] = df[column].astype("object")
  return df.dtypes

def is_ID(df,review):
  ID = []
  for item in review:
            if item["reason"] == "High unique ratio - possible identifier":
                 column = item["column"]
                 dec=input(print("Is",column ,"an ID column ? (YES)(NO) "))
                 if dec=="YES" and df[column].dtype != "object":
                      df[column] = df[column].astype("object")
                      ID.append(column)
  return ID