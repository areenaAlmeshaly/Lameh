import pandas as pd

def detect_numeric(df):
    info={}
    for i in df.columns:
        column=df[i]
        converted = pd.to_numeric(column, errors="coerce")
        numeric_ratio = converted.notna().sum()/column.notna().sum()

        n_unique = column.nunique()
        unique_ratio = n_unique / column.notna().sum()

        if numeric_ratio>=0.95:
                info[i]={
                    "numericـratio" : numeric_ratio,
                   "n_unique" :n_unique,
                    "unique_ratio" : unique_ratio
                }
    return info


def detect_date(df):
    date_info = {}
    for i in df.columns:
        column = df[i]
        if column.dtype == "object":
            converted = pd.to_datetime(
                column,
                errors="coerce",
                format="mixed")
            date_ratio = converted.notna().sum() / column.notna().sum()
            if date_ratio >= 0.95:
                date_info[i] = {
                    "date_ratio": date_ratio}
    return date_info
 

def classify_columns(df,info,date_info):
    review = []
    ambiguous = []
    numric_col=[]
    cat_col=[]
    for i in df.columns:
         if i in date_info:
             review.append({
        "column": i,
        "reason": "May be date"
    })
         elif i in info:
              numeric_ratio = info[i]["numericـratio"]
              unique_ratio = info[i]["unique_ratio"]
              n_unique=info[i]["n_unique"]

              if numeric_ratio < 1.0:
                  review.append({
        "column": i,
        "reason": "Not fully numeric"})

              elif n_unique <= 10:
                review.append({
                    "column": i,
                    "reason": "Numeric column with few unique values - may be categorical"}) 
                
              elif unique_ratio >= 0.95:
                  review.append({
        "column": i,
        "reason": "High unique ratio - possible identifier"})
              else:
                  numric_col.append(i)
                  df[i] = pd.to_numeric(df[i], errors="coerce")

                   
         elif df[i].dtype == "object":
              
              unique_ratio = df[i].nunique() / df[i].notna().sum()
              if unique_ratio >= 0.95:
                review.append({"column": i,
                                   "reason":"High unique ratio - possible identifier"})  
              else:
                  cat_col.append(i)
    
         else:

                ambiguous.append({
                    "column": i,
                    "reason":"Object column - ambiguous for automatic EDA"})
    
    return df,review,numric_col,cat_col,ambiguous