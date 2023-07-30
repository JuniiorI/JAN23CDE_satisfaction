def split_projection(df_all):
    df_all[["Number_review", "review"]] = df_all["Number_review"].str.split(" ", n=1, expand=True)
    df_all[["ExperienceDate", "Date_experience"]]= df_all["Experience Date"].str.split(":", n = 1, expand = True)
    df_all[["Experience", "Date"]]= df_all["Experience Date"].str.split("Date", n = 1, expand = True)


    new_df = df_all[["Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience"]]
    return new_df
