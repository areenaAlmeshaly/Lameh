import pandas as pd 

def data_sammary(df):

    memory =df.memory_usage(deep=True).sum()
    rows, columns = df.shape

    dataSize={
        "Columns":columns,
        "Rows":rows,
        "memory":memory
    }

    types = df.dtypes
    unique = df.nunique()
    nonnull=df.notnull().sum()

    summary = pd.DataFrame({"Types":types,
    "unique":unique ,
    "non-null":nonnull})

    Duplicates=df.duplicated().sum()
    DuplicatePerc=(Duplicates/rows)*100

    data_quality={
        "Duplicates num":Duplicates,
        "Duplicates percent":DuplicatePerc,}


    null=df.isnull().sum() 
    null=null[null>0]  
    nullperc=(null/rows)*100
     
    missing_values=pd.DataFrame({
    "null num":null,
    "null perc": nullperc
    })

    return dataSize,summary,data_quality,missing_values
