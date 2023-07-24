import requests
from bs4 import BeautifulSoup
import pandas as pd

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
