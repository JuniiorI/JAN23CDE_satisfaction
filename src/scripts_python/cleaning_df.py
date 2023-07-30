def cleaning_df(new_df):
    new_df["Status"] = new_df["Status"].fillna(method="bfill")
    new_df["Reply"] = new_df["Reply"].fillna("No Reply")
    new_df["Date_reply"] = new_df["Date_reply"].fillna(new_df["Date_review"])
    new_df["Date_reply"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_reply"]) else row["Date_reply"], axis=1)
    new_df = new_df.dropna(how="any")
    return new_df
