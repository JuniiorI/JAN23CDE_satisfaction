
def split_projection(df_all):

    #split number et review in different columns, expand = True: nous rend des dataframes
    # expand = False: nous rend une serie
    df_all[["Number_review", "review"]]= df_all["Number_review"].str.split(" ", n = 1, expand = True)
    #split Experience et Date in different columns
    df_all[["Experience", "Date"]]= df_all["Experience Date"].str.split("Date", n = 1, expand = True)

    new_df = df_all[["Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience"]]

    return new_df

