import pandas as pd 
def turning_categ(df,review):
  for item in review:
            if item["reason"] == "Numeric column with few unique values - may be categorical":
                 column = item["column"]
                 dec=input(f"Is {column} a categorical column ? (yes)(no)")
                 if dec.lower()=="yes" and df[column].dtype != "object":
                      df[column] = df[column].astype("object")
  return df

def is_ID(df,review):
  ID = []
  for item in review:
            if item["reason"] == "High unique ratio - possible identifier":
                 column = item["column"]
                 dec=input(f"Is {column} an ID column ? (yes)(no) ")
                 if dec.lower()=="yes" and df[column].dtype != "object":
                      df[column] = df[column].astype("object")
                      ID.append(column)
  return ID

def not_full_num(df,review):
     for item in review:
                  if item["reason"] == "Not fully numeric":
                       column = item["column"]
                       converted = pd.to_numeric(df[column], errors="coerce")
                       invalid_values = df[column][converted.isna() & df[column].notna()]
                       print(column)
                       print("Invalid values:")
                       print(invalid_values)
                       df[column] = converted
     return df

def drop_dupl(df):
    return df.drop_duplicates(keep="first")

def null_val(df,missing_values):
     deal_cols=[]
     for col in missing_values.index:
          perc = missing_values.loc[col, "null perc"]

          if perc>0:
                if perc>=50:
                      print(f"WARNING : missing values in {col} To high to drop it ! ")

                dec=input(f"what do you want to do with null values in {col} it has a percent {perc} drop OR Deal with it ?")
                if dec.lower()=="drop":
                  df = df.dropna(subset=[col])

                elif dec.lower() == "deal":    
                            deal_cols.append(col)
     return deal_cols,df
                