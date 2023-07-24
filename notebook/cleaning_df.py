
from datetime import datetime
def cleaning_df(new_df):

    # backfill / bfill: use next valid observation to fill gap.
    new_df[["Status"]] = new_df[["Status"]].fillna(method = "bfill")
    new_df[["Reply"]] = new_df[["Reply"]].fillna("No Reply")
    new_df[["Date_reply"]] = new_df[["Date_reply"]].fillna(new_df[["Date_review"]])

    return new_df
