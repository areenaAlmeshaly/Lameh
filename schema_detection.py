import pandas as pd

def detect_numeric(df):
    info={}
    for i in df.columns:
        column=df[i]
        converted = pd.to_numeric(column, errors="coerce")
        numeric_ratio = converted.notna().sum()/column.notna().sum()
        if numeric_ratio!=0:
            info[i]=numeric_ratio

            if numeric_ratio>=0.95:
                df[i] = converted
    return info,df.dtypes


def detect_date(df):
    info={} 
    for i in df.columns:
        column=df[i]
        if column.dtype=="object":
            converted = pd.to_datetime(column, errors="coerce", format="mixed")
            date_ratio = converted.notna().sum()/column.notna().sum()
            if date_ratio!=0:
                info[i]=date_ratio
                if date_ratio>=0.95:
                    df[i] = converted            
    return info,df.dtypes

def detect_categoral(df):
    info={} 
    for i in df.columns:
            column=df[i]
            if column.dtype=="object":
                values_ratio=(column.value_counts()/column.count())
                for value in values_ratio.index:
                    if values_ratio[value] <= 0.1:
                        info[i] = values_ratio[value]
    return info