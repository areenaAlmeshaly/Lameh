import pandas as pd 
def turning_categ(df,review,numric_col,cat_col,decisions):
     for item in review:
            if item["reason"] == "Numeric column with few unique values - may be categorical":
                 column = item["column"]
                 dec = decisions.get(column)
                 if dec.lower() == "y":
                      df[column] = df[column].astype("object")
                      cat_col.append(column)
                 elif dec.lower() == "n":
                      numric_col.append(column)

     return df,numric_col,cat_col

def turning_date(df, review,decisions):
    for item in review:
        if item["reason"]=="Might be date":
            column = item["column"]
            converted=pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed")
            dec=decisions.get(column)
            if dec.lower() == "y":
                df[column]=converted
    return df

def is_ID(review,decisions):
  ID = []
  for item in review:
            if item["reason"] == "High unique ratio - possible identifier":
                 column = item["column"]
                 dec = decisions.get(column)
                 if dec.lower()=="y":
                      ID.append(column)
                      
  return ID


def not_full_num(df,review,numric_col):
     for item in review:
                  if item["reason"] == "Not fully numeric":
                       column = item["column"]
                       converted = pd.to_numeric(df[column], errors="coerce")
                       invalid_values = df[column][converted.isna() & df[column].notna()]
                       print(column)
                       print("Invalid values:")
                       print(invalid_values)
                       df[column] = converted
                       numric_col.append(column)
     return df,numric_col


def duplicate_val(df,decisions):
    duplicates_num = df.duplicated().sum()
    if duplicates_num > 0:
        if decisions.lower() == "y":
            df = df.drop_duplicates(keep="first")
    return df


def null_val(df,missing_values,decisions):
     deal_cols=[]
     for col in missing_values.index:
          perc = missing_values.loc[col, "null perc"]

          if perc>0:
                 dec = decisions.get(col)
                 if dec == "drop":
                       df = df.dropna(subset=[col])
                 elif dec== "deal":
                            deal_cols.append(col)
     return deal_cols,df


def null_deal(df,deal_cols,missing_values,decisions):
     for column_name in deal_cols:
        column = df[column_name]
        decision = decisions.get(column_name)

        if pd.api.types.is_numeric_dtype(column):
            if decision=="mean":
                df[column_name]=column.fillna(column.mean())
            elif decision=="median":
                df[column_name] = column.fillna(column.median())
            elif decision=="keep":
                pass
        elif pd.api.types.is_object_dtype(column):
                 if decision == "mode":
                      df[column_name] = column.fillna(column.mode()[0])

                 elif decision == "keep":
                      pass
     return df



def outliers(df, decisions):
    outlier_info = {}
    for i in df.columns:
        column = df[i]

        if not pd.api.types.is_numeric_dtype(column):
            continue
        q1=column.quantile(0.25)
        q3=column.quantile(0.75)
        iqr=q3 - q1

        lower_inner=q1-1.5*iqr
        upper_inner=q3+1.5*iqr

        lower_outer=q1-3*iqr
        upper_outer=q3+3*iqr

        mild_outliers=column[
            ((column<lower_inner)&(column>=lower_outer))|
            ((column>upper_inner)&(column<=upper_outer))]

        extreme_outliers = column[(column < lower_outer)|(column > upper_outer)]
        non_null = column.notna().sum()

        mild_percent = (len(mild_outliers) / non_null) * 100
        extreme_percent = (len(extreme_outliers) / non_null) * 100

        if len(mild_outliers) > 0 or len(extreme_outliers) > 0:
            outlier_info[i]={
                 "q1": q1,"q3": q3,"iqr": iqr,
                "mild_range": (lower_inner, upper_inner),
                "mild_percent": mild_percent,
                "extreme_range": (lower_outer, upper_outer),
                "extreme_percent": extreme_percent}

            dec = decisions.get(i)
            if dec == "mild":
                df = df.drop(index=mild_outliers.index)

            elif dec == "extreme":
                df = df.drop(index=extreme_outliers.index)

            elif dec=="all":
                df=df.drop(
                    index=mild_outliers.index.union(extreme_outliers.index))

    return df, outlier_info