import pandas as pd

def load_file(file_path):
    extension=file_path.split(".")[-1].casefold()
    readers={"csv":pd.read_csv,
             "xlsx":pd.read_excel,
             "json":pd.read_json }
    
    if extension in readers:
        return(readers[extension](file_path))
    else:
        raise ValueError(f"Unsupported file extension: {extension}")
