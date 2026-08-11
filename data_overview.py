import pandas as pd 

def data_summary(df):

    memory =df.memory_usage(deep=True).sum()
    rows_num, columns_num = df.shape

    if rows_num <50:
        print("Warning ! : Your DataSet is too small for ML")

    data_Size={
        "Columns":columns_num,
        "Rows":rows_num,
        "memory":memory
    }

    types = df.dtypes
    unique = df.nunique()
    nonnull=df.notnull().sum()

    columns_Info = pd.DataFrame({"Types":types,
    "unique":unique ,
    "non-null":nonnull})

    duplicates_num=df.duplicated().sum()
    duplicate_Perc=(duplicates_num/rows_num)*100

    duplicates={
        "Duplicates num":duplicates_num,
        "Duplicates percent":duplicate_Perc,}


    null_num=df.isnull().sum() 
    only_null_col=null_num[null_num>0]  
    null_perc=(null_num/rows_num)*100
     
    missing_values=pd.DataFrame({
    "null num":only_null_col,
    "null perc": null_perc,
    })

    return data_Size,columns_Info,duplicates,missing_values
