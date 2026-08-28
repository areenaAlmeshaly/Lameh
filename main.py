#.  /Users/areena/Desktop/HR_Attrition_Project/IBM Data.csv
#  /Users/areena/Desktop/dirty_cafe_sales.csv
# /Users/areena/Desktop/marketing_campaign.csv
from file_loader import load_file
from data_overview import data_summary
from schema_detection import detect_numeric, detect_date, classify_columns
from cleaning_data import(
    turning_categ,
    turning_date,
    is_ID,
    not_full_num,
    null_val,
    duplicate_val,
    null_deal,
    outliers)
from EDA import descr, num_vizual, num_rela, cat_vizual

def main():
    file_path = input("Enter your file path: ")
    df = load_file(file_path)
    data_size,columns_info,duplicates,missing_values = data_summary(df)

    info=detect_numeric(df)
    date_info=detect_date(df)

    df,review,numeric_col,cat_col=classify_columns(df,info,date_info)
    df, numeric_col,cat_col=turning_categ(df,review,numeric_col,cat_col)

    df=turning_date(df,review)
    ID=is_ID(review)

    df,numeric_col=not_full_num(df,review,numeric_col)

    deal_cols,df=null_val(df,missing_values)

    df=duplicate_val(df)

    df=null_deal(df,deal_cols,missing_values)

    df = outliers(df)
    descr(df, ID)
    num_vizual(df, numeric_col)
    num_rela(df, numeric_col)
    cat_vizual(df, cat_col)

if __name__ == "__main__":
    main()