import pandas as pd

def concat_extracted_companies(df_company, df_cofidis, df_orange, df_floa, df_bourso, df_anytime):
    df_all = pd.concat([df_company, df_cofidis, df_orange, df_floa, df_bourso, df_anytime], axis=0)
    df_all = df_all.reset_index(drop=True)
    return df_all