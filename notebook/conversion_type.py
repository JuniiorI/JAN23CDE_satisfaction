import pandas as pd
def conversion_type(new_df):

    new_df[["Number_review", "Rating"]] = new_df[["Number_review", "Rating"]].astype("int64")
    new_df[["Date_review", "Date_reply", "Date_experience"]] = new_df[["Date_review", "Date_reply","Date_experience"]].apply(pd.to_datetime, errors='ignore', format="%d%m%y")
