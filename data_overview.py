import pandas as pd 

def Data_sammary(df):

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

    Data_Quality={
        "Duplicates":DuplicatePerc
    }

    return dataSize,summary,Data_Quality
