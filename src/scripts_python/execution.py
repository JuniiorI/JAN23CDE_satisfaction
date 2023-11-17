# Exécution du code
from Fonctions_python import cleaning_df, concat_extracted_companies, conversion_type, main_dataframe, split_projection


younited_url = "https://www.trustpilot.com/review/www.younited-credit.com"
cofidis_url = "https://www.trustpilot.com/review/www.cofidis.fr"
floa_url = "https://www.trustpilot.com/review/www.floabank.fr"
orange_url = "https://www.trustpilot.com/review/www.orangebank.fr"
bourso_url = "https://www.trustpilot.com/review/boursorama-banque.com"
anytime_url = "https://www.trustpilot.com/review/anyti.me"

df_all = concat_extracted_companies(younited_url, cofidis_url, orange_url, floa_url, bourso_url, anytime_url)
df_splited = split_projection(df_all.copy())
df_converted = conversion_type(df_splited.copy())
df_cleaned = cleaning_df(df_converted.copy())
main_dataframe(df_cleaned)

# Affichage du dataframe final en entier
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
df_cleaned.head()