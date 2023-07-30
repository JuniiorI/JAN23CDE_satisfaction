def conversion_type(new_df):

    new_df[["Number_review", "Rating"]] = new_df[["Number_review", "Rating"]].astype("int64")
    # Convertir les colonnes "Date_review", "Date_reply" et "Date_experience" en dates
    new_df["Date_review"] = new_df["Date_review"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)

    # Convertir la colonne "Date_experience" en date
    new_df["Date_experience"] = new_df["Date_experience"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)

    #Convertir la colonne "Date_reply" en dates
    new_df["Date_reply"] = new_df["Date_reply"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)

    #Remplacer les valeurs manquantes de "Date_reply" par les valeurs de "Date_review"
    new_df["Date_reply"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_reply"]) else row["Date_reply"], axis=1)


    return new_df
