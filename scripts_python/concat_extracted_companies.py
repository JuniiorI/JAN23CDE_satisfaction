def concat_extracted_companies(younited_url, cofidis_url, orange_url, floa_url, bourso_url, anytime_url):
    df_younited = extract_reviews(younited_url)
    df_cofidis = extract_reviews(cofidis_url)
    df_floa = extract_reviews(floa_url)
    df_orange = extract_reviews(orange_url)
    df_bourso = extract_reviews(bourso_url)
    df_anytime = extract_reviews(anytime_url)

    df_all = pd.concat([df_younited, df_cofidis, df_orange, df_floa, df_bourso, df_anytime], ignore_index=True)
    return df_all