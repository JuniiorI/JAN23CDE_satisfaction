import requests
from bs4 import BeautifulSoup
import pandas as pd
import dateparser

def extract_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []

    pagination = soup.find("div", class_="styles_pagination__6VmQv")
    last_page = pagination.find_all("a")[-2].text
    last_page = pd.to_numeric(last_page)

    for i in range(1, last_page + 1):
        page_url = url + "?page=" + str(i)
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')

        reviews = page_soup.find_all("div", class_="styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ")

        for review in reviews:
            review_data = {}

            review_data["Company"] = soup.find("h1", class_="typography_default__hIMlQ typography_appearance-default__AAY17 title_title__i9V__").span.get_text(strip=True)
            review_data["Customer"] = review.find("span", class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17").text
            review_data["Number_review"] = review.find("div", class_="styles_consumerExtraDetails__fxS4S").find("span").text
            review_data["Language"] = review.find("div", class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua").text
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


def concat_extracted_companies(younited_url, cofidis_url, orange_url, floa_url, bourso_url, anytime_url):
    df_younited = extract_reviews(younited_url)
    df_cofidis = extract_reviews(cofidis_url)
    df_floa = extract_reviews(floa_url)
    df_orange = extract_reviews(orange_url)
    df_bourso = extract_reviews(bourso_url)
    df_anytime = extract_reviews(anytime_url)

    df_all = pd.concat([df_younited, df_cofidis, df_orange, df_floa, df_bourso, df_anytime], ignore_index=True)
    return df_all


def split_projection(df_all):
    df_all[["Number_review", "review"]] = df_all["Number_review"].str.split(" ", n=1, expand=True)
    df_all[["ExperienceDate", "Date_experience"]]= df_all["Experience Date"].str.split(":", n = 1, expand = True)
    df_all[["Experience", "Date"]]= df_all["Experience Date"].str.split("Date", n = 1, expand = True)


    new_df = df_all[["Company", "Customer", "Number_review", "Language", "Title", "Date_review", "Reply", "Date_reply", "Rating", "Status", "Experience", "Date_experience"]]
    return new_df


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


def cleaning_df(new_df):
    new_df["Status"] = new_df["Status"].fillna(method="bfill")
    new_df["Reply"] = new_df["Reply"].fillna("No Reply")
    new_df["Date_reply"] = new_df["Date_reply"].fillna(new_df["Date_review"])
    new_df["Date_reply"] = new_df.apply(lambda row: row["Date_review"] if pd.isna(row["Date_reply"]) else row["Date_reply"], axis=1)
    new_df = new_df.dropna(how="any")
    return new_df


def main_dataframe(new_df):
    new_df.to_csv("data/satisfaction_client.csv", index=False)


# Exécution du code
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

