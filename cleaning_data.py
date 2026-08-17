import pandas as pd 
def turning_categ(df,review):
  for item in review:
            if item["reason"] == "Numeric column with few unique values - may be categorical":
                 column = item["column"]
                 dec=input(f"Is {column} a categorical column ? (y/n)")
                 if dec.lower()=="y" and df[column].dtype != "object":
                      df[column] = df[column].astype("object")
  return df


def is_ID(df,review):
  ID = []
  for item in review:
            if item["reason"] == "High unique ratio - possible identifier":
                 column = item["column"]
                 dec=input(f"Is {column} an ID column ? (y/n) ")
                 if dec.lower()=="y" and df[column].dtype != "object":
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


def duplicate_val(df):
    duplicates_num = df.duplicated().sum()
    if duplicates_num > 0:
        print("Found", duplicates_num, "duplicate rows.")

        dec = input("Do you want to drop them? (y/n) ")

        if dec.lower() == "y":
            df = df.drop_duplicates(keep="first")
    return df


def null_val(df,missing_values):
     deal_cols=[]
     for col in missing_values.index:
          perc = missing_values.loc[col, "null perc"]

          if perc>0:
                if perc>=50:
                      print(f"WARNING : missing values in {col} To high to drop it ! ")

                dec=input(f"what do you want to do with null values in {col} it has a percent {perc}% drop OR Deal with it ?")
                if dec.lower()=="drop":
                  df = df.dropna(subset=[col])

                elif dec.lower() == "deal":    
                            deal_cols.append(col)
     return deal_cols,df


def null_deal(df,deal_cols,missing_values):
    for i in deal_cols:
     per=missing_values.loc[i, "null perc"]
     column=df[i]
     if column.dtype != "object":
        skew = column.skew()

        if abs(skew)<0.5:
           reco="mean"

        elif abs(skew)>0.5:
           reco="median"

        dec=input(f"{i} has {per} missing values.\n" f"Recommended method: {reco} \n" f"skew is {skew} \n""Do you want to use it ? (y/n) ")
        if dec.lower()=="y":
               if reco=="mean":
                    column= column.fillna(column.mean())
               else:
                    column= column.fillna(column.median())

        elif dec.lower()=="n":
              dec2=input("would you like to\n""1- keep it as null\n""2-use median?\n")

              if dec2==2:
                 if reco=="mean":
                      column= column.fillna(column.median())
                 else:
                      column= column.fillna(column.mean())

     elif column.dtype == "object" :
        top_ratio =column.value_counts(normalize=True).iloc[0]
        cate=column.value_counts(normalize=True).index[0]
        dec=input(f"No dominant category was detected for {i} column.\n""Mode imputation is not recommended." "What would you like to do?\n""1. Leave missing values\n""2. Fill with mode anywayn")

        if top_ratio >= 0.5:
           print(f"{i} has {per} missing values.\n" f"most Category is {cate}.\n" f"with {top_ratio}% ratio" f"Recommended method: mode \n" "Do you want to use it ? (y/n)")
           column= column.fillna(column.mode()[0])

        elif dec:
             if dec==2:
                  column= column.fillna(column.mode()[0])
    return df



"""def outliers(df):
     for i in df.columns:
          column=df[i]
          if not pd.api.types.is_numeric_dtype(column):
            continue

          med=column.median()
          q1=column.quantile(0.25)
          q3=column.quantile(0.75)
          iqr=q3-q1
          lower_inner=q1-1.5 *iqr
          upper_inner=q3+1.5*iqr
          lower_outer = q1 - 3 * iqr
          upper_outer = q3 + 3 * iqr

          mild_outliers=column[((column<lower_inner)&(column>=lower_outer))|((column>upper_inner)&(column<=upper_outer))]
          extreme_outliers=column[(column<lower_outer)|(column>upper_outer)]
          non_null = column.notna().sum()
          mild_outliers_per=(mild_outliers/non_null)*100


          if len(mild_outliers) > 0 or len(extreme_outliers) > 0:
               dec=input(f"column {i} \n"f"Q1={q1} \n"f"median={med}\n"f"Q3={q3}\n"
                         f"IQR={iqr}\n"f"Potential outliers :{mild_outliers_per}%\n"
                         f"Extreme outliers ({len(extreme_outliers)}): {extreme_outliers.tolist()}\n""These values are statistically unusual \n"
                         "An extreme outlier is not automatically an error.\n""Do you want to:\n""1. Keep\n""2. Remove \n")
               if dec=="2":
                    dec2=input("Would you like to remove\n" "1.Extreme potential outlier\n""2.Potential outliers\n""3.ALL\n")
                    if dec2 =="1":
                         df.drop(index=extreme_outliers.index)
                    elif dec2=="2":
                         df.drop(index=mild_outliers.index)
                    elif dec2=="3":
                         df.drop(index=mild_outliers.index)&df.drop(index=extreme_outliers.index)
     return df"""

def outliers(df):
     for i in df.columns:
          column=df[i]
          if not pd.api.types.is_numeric_dtype(column):
            continue

          med=column.median()
          q1=column.quantile(0.25)
          q3=column.quantile(0.75)
          iqr=q3-q1
          lower_inner=q1-1.5 *iqr
          upper_inner=q3+1.5*iqr
          lower_outer = q1 - 3 * iqr
          upper_outer = q3 + 3 * iqr

          mild_outliers=column[((column<lower_inner)&(column>=lower_outer))|((column>upper_inner)&(column<=upper_outer))]
          extreme_outliers=column[(column<lower_outer)|(column>upper_outer)]
          non_null = column.notna().sum()

          mild_outliers_num=len(mild_outliers)
          extreme_outliers_num=len(extreme_outliers)

          if non_null > 0:
               mild_outliers_per=(mild_outliers_num/non_null)*100

          if len(mild_outliers) > 0 or len(extreme_outliers) > 0:

               if len(extreme_outliers) == 0:
                    dec=input(f"column {i} \n"f"Q1={q1} \n"f"median={med}\n"f"Q3={q3}\n"
                              f"IQR={iqr}\n"f"Potential outliers ({mild_outliers_num}): {mild_outliers_per:.2f}%\n"
                              f"Potential outlier range: {mild_outliers.min()} - {mild_outliers.max()}\n"
                              "These values are statistically unusual, but they are not necessarily a data problem.\n"
                              "Do you want to:\n""1. Keep\n""2. Remove \n")

                    if dec=="2":
                         df=df.drop(index=mild_outliers.index)

               else:
                    dec=input(f"column {i} \n"f"Q1={q1} \n"f"median={med}\n"f"Q3={q3}\n"
                              f"IQR={iqr}\n"f"Potential outliers ({mild_outliers_num}): {mild_outliers_per:.2f}%\n"
                              f"Potential outlier range: {mild_outliers.min()} - {mild_outliers.max()}\n"
                              f"Extreme outliers ({extreme_outliers_num}): {extreme_outliers.tolist()}\n"
                              "These values are statistically unusual.\n"
                              "An extreme outlier is not automatically an error.\n"
                              "Do you want to:\n""1. Keep\n""2. Remove \n")

                    if dec=="2":
                         dec2=input("Would you like to remove\n" "1.Extreme potential outlier\n""2.Potential outliers\n""3.ALL\n")

                         if dec2 =="1":
                              df=df.drop(index=extreme_outliers.index)
                         elif dec2=="2":
                              df=df.drop(index=mild_outliers.index)
                         elif dec2=="3":
                              df=df.drop(index=mild_outliers.index.union(extreme_outliers.index))

     return df