import requests
from bs4 import BeautifulSoup
import pandas as pd
import dateparser
import re
import os
import time

def extract_reviews(url):
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Your User Agent String'
    }

    response = requests.get(url, headers=headers)
    print(f"Request to {url} - Status Code: {response.status_code}")

    # Sleep for a few seconds to avoid hitting the server too frequently
    time.sleep(3)    
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    pagination = soup.find("div", class_="styles_pagination__6VmQv")
    if pagination is None:
        last_page = 1
    else:
        last_page = pagination.find_all("a")[-2].text

    for i in range(1, int(last_page) + 1):
        page_url = url + "?page=" + str(i)
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')

        reviews = page_soup.find_all("div", class_="styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ")

        for review in reviews:
            review_data = {}

            review_data["Company"] = soup.find("h1", class_="typography_default__hIMlQ typography_appearance-default__AAY17 title_title__i9V__").span.get_text(strip=True)
            review_data["Customer"] = review.find("span", class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17").text
            review_data["Number_review"] = review.find("div", class_="styles_consumerExtraDetails__fxS4S").find("span").text
            language_element = review.find("div", class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua")
            review_data["Language"] = language_element.text if language_element else None
            review_data["Title"] = review.find("h2", class_="typography_heading-s__f7029 typography_appearance-default__AAY17").text
            review_data["Date_review"] = review.find("div", class_="styles_reviewHeader__iU9Px").time.text
            reply = review.find("div").find("p", class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX")
            review_data['Reply'] = reply.text if reply else None
            review_data['Date_reply'] = review.find("div", class_="styles_content__Hl2Mi").time.text if reply else None
            review_data["Rating"] = review.find("section", class_="styles_reviewContentwrapper__zH_9M").div["data-service-review-rating"]
            type_element = review.find_next("div", class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__yqwWi")
            review_data["Status"] = type_element.find("span").text if type_element else None
            review_data["Experience Date"] = review.find("div", class_="styles_reviewContent__0Q2Tg").text

            data.append(review_data)

    df = pd.DataFrame(data)
    return df

# Fonction pour concaténer les avis de différentes entreprises et les ré-extraire
def concat_extracted_companies(company_urls, previous_dfs=None):
    dfs = {}

    for company, (url, file_path) in company_urls.items():
        if os.path.isfile(file_path):
            dfs[company] = pd.read_csv(file_path)
        else:
            dfs[company] = extract_reviews(url)
            dfs[company].to_csv(file_path, index=False)

    df_all = pd.concat(list(dfs.values()), axis=0)

    # Print the structure of df_all after concatenation
    df_all = df_all.reset_index(drop=True)

    if df_all.empty and previous_dfs is not None:
        print("Le DataFrame est vide. Utilisation des données précédentes.")
        return previous_dfs
    else:
        return df_all

def split_projection(df_all):
    if df_all.empty:
        print("Le DataFrame est vide. Re-scraping le site.")
        return df_all  # Renvoie le DataFrame original non modifié

    print(df_all.columns)  # Affiche les colonnes dans la console pour le débogage
    df_all[["Number_review", "review"]] = df_all["Number_review"].str.split(" ", n=1, expand=True)
    df_all[["ExperienceDate", "Date_experience"]] = df_all["Experience Date"].str.split(":", n=1, expand=True)
    df_all[["Experience", "Date"]] = df_all["Experience Date"].str.split("Date", n=1, expand=True)

    new_df = df_all[["Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience"]]
    return new_df

def convert_date(date_str):
    try:
        return dateparser.parse(date_str).strftime('%Y-%m-%d')
    except:
        # Handle different date formats here
        formats_to_try = ['%Y-%m-%d', 'Updated %b %d, %Y']
        for format_str in formats_to_try:
            try:
                if 'Updated' in date_str:
                    # Handle the "Updated" format separately
                    return dateparser.parse(date_str, date_formats=[format_str]).strftime('%Y-%m-%d')
                else:
                    return dateparser.parse(date_str, date_formats=[format_str]).strftime('%Y-%m-%d')
            except:
                pass
        # If all formats fail, return the original string
        return date_str

def conversion_type(new_df):
    # Create a regular expression to match the date format
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    # Identify the invalid dates
    invalid_dates = []
    for date in new_df['Date_review']:
        if not date_regex.match(date):
            invalid_dates.append(date)

    # Print the number of invalid dates
    print(len(invalid_dates))

    # Vérifier la présence des colonnes avant de les utiliser
    if 'Date_review' in new_df.columns:
        new_df["Date_review"] = new_df["Date_review"].apply(convert_date)

    if 'Date_reply' in new_df.columns:
        new_df["Date_reply"] = new_df["Date_reply"].apply(convert_date)

    if 'Date_experience' in new_df.columns:
        new_df["Date_experience"] = new_df["Date_experience"].apply(convert_date)

    # Convertir la colonne "Date_reply" en dates
    new_df["Date_reply"] = new_df["Date_reply"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)
    # Remplacer les valeurs manquantes de "Date_reply" par les valeurs de "Date_review"
    new_df["Date_reply"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_reply"]) else row["Date_reply"], axis=1)
    # Convertir la colonne "Date_reply" en dates
    new_df["Date_experience"] = new_df["Date_experience"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)
    # Remplacer les valeurs manquantes de "Date_reply" par les valeurs de "Date_review"
    new_df["Date_experience"] = new_df.apply(lambda row: row["Date_experience"] if pd.isna(row["Date_experience"]) else row["Date_experience"], axis=1)
    # Convertir la colonne "Date_reply" en dates
    new_df["Date_review"] = new_df["Date_review"].apply(lambda x: dateparser.parse(x) if isinstance(x, str) else x)
    # Remplacer les valeurs manquantes de "Date_reply" par les valeurs de "Date_review"
    new_df["Date_review"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_review"]) else row["Date_review"], axis=1)

    new_df[["Number_review", "Rating"]] = new_df[["Number_review", "Rating"]].astype("int64")
    return new_df

def cleaning_df(new_df):
    # Check if 'Status' column exists
    new_df["Status"] = new_df["Status"].fillna(method="bfill")
    new_df["Reply"] = new_df["Reply"].fillna("No Reply")
    new_df["Date_reply"] = new_df["Date_reply"].fillna(new_df["Date_review"])
    new_df["Date_reply"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_reply"]) else row["Date_reply"], axis=1)

    return new_df

def create_response_time(new_df):
    columns_to_convert = ['Date_review', 'Date_experience', 'Date_reply']
    for col in columns_to_convert:
        new_df[col] = pd.to_datetime(new_df[col], format='%Y-%m-%d')

    # Calculate 'Response_time' as the difference between 'Date_reply' and 'Date_review'
    #min_date = min(new_df['Date_review'])
    new_df["Response_time"] = new_df["Date_reply"] - new_df['Date_review']

    # Convert 'Response_time' to a timedelta format
    new_df["Response_time"] = new_df["Response_time"].dt.days

    # Replace NaN values with 0
    new_df["Response_time"].fillna(0)
    new_df = new_df[["Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience", "Response_time"]]
    new_df = new_df.dropna(subset=["Language", "Date_experience"])

    return new_df
def load_existing_dataframe(file_path):
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Your User Agent String'
    }

    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        print(f"Loaded DataFrame from {file_path}")
        return df
    else:
        print(f"No existing DataFrame found at {file_path}")
        return pd.DataFrame()

def main_dataframe(new_df, df_anytime, df_bourso, df_orange, df_floa, df_cofidis, df_younited):
    # Convertir le DataFrame en une liste de dictionnaires
    review_data = df_cleaned.to_dict(orient='records')

    new_df.to_json("../data/processed/reviews.json", orient='records')
    new_df.to_csv("../data/processed/reviews.csv", index=False)
    new_df.to_csv("../data/processed/avis_clients.csv", index=False)
    df_anytime.to_csv("../data/raw/anytime.csv", index=False)
    df_bourso.to_csv("../data/raw/bourso.csv", index=False)
    df_orange.to_csv("../data/raw/orange.csv", index=False)
    df_floa.to_csv("../data/raw/floa.csv", index=False)
    df_cofidis.to_csv("../data/raw/cofidis.csv", index=False)
    df_younited.to_csv("../data/raw/younited.csv", index=False)

# Exécution du code
younited_url = "https://www.trustpilot.com/review/www.younited-credit.com"
cofidis_url = "https://www.trustpilot.com/review/www.cofidis.fr"
floa_url = "https://www.trustpilot.com/review/www.floabank.fr"
orange_url = "https://www.trustpilot.com/review/www.orangebank.fr"
bourso_url = "https://www.trustpilot.com/review/boursorama-banque.com"
anytime_url = "https://www.trustpilot.com/review/anyti.me"

# Liste des URLs et des noms de fichiers
company_urls = {
    "younited": (younited_url, "../data/raw/younited.csv"),
    "cofidis": (cofidis_url, "../data/raw/cofidis.csv"),
    "floa": (floa_url, "../data/raw/floa.csv"),
    "orange": (orange_url, "../data/raw/orange.csv"),
    "bourso": (bourso_url, "../data/raw/bourso.csv"),
    "anytime": (anytime_url, "../data/raw/anytime.csv")
}

#charger les DataFrames existants s'ils existent déjà
anytime_file_path = "../data/raw/anytime.csv"
bourso_file_path = "../data/raw/bourso.csv"
orange_file_path = "../data/raw/orange.csv"
floa_file_path = "../data/raw/floa.csv"
cofidis_file_path = "../data/raw/cofidis.csv"
younited_file_path = "../data/raw/younited.csv"

# Vérifiez l'existence des fichiers avant de les lire
df_anytime = pd.read_csv(anytime_file_path) if os.path.isfile(anytime_file_path) else pd.DataFrame()
df_bourso = pd.read_csv(bourso_file_path) if os.path.isfile(bourso_file_path) else pd.DataFrame()
df_orange = pd.read_csv(orange_file_path) if os.path.isfile(orange_file_path) else pd.DataFrame()
df_floa = pd.read_csv(floa_file_path) if os.path.isfile(floa_file_path) else pd.DataFrame()
df_cofidis = pd.read_csv(cofidis_file_path) if os.path.isfile(cofidis_file_path) else pd.DataFrame()
df_younited = pd.read_csv(younited_file_path) if os.path.isfile(younited_file_path) else pd.DataFrame()

# Exécution du code
df_all = concat_extracted_companies(company_urls)
df_splited = split_projection(df_all)
df_converted = conversion_type(df_splited)
df_cleaned = cleaning_df(df_converted)
new_df = create_response_time(df_cleaned)

df_anytime = extract_reviews(anytime_url)
df_bourso = extract_reviews(bourso_url)
df_orange = extract_reviews(orange_url)
df_floa = extract_reviews(floa_url)
df_cofidis = extract_reviews(cofidis_url)
df_younited = extract_reviews(younited_url)

# Pass the extracted dataframes to main_dataframe
main_dataframe(new_df, df_anytime, df_bourso, df_orange, df_floa, df_cofidis, df_younited)
print(new_df)
