
import requests
import csv
from bs4 import BeautifulSoup

# Page produit choisie
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Télécharger la page
page = requests.get(url)

# Lire le contenu HTML
soup = BeautifulSoup(page.content, "html.parser")

# Informations du produit
title = soup.find("h1").text

table = soup.find("table")
rows = table.find_all("tr")

upc = rows[0].find("td").text
price_excluding_tax = rows[2].find("td").text
price_including_tax = rows[3].find("td").text
number_available = rows[5].find("td").text

description = soup.find("div", id="product_description")
if description:
    product_description = description.find_next_sibling("p").text
else:
    product_description = ""

category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

review_rating = soup.find("p", class_="star-rating")["class"][1]

image = soup.find("img")["src"]
image_url = "https://books.toscrape.com/" + image.replace("../", "")

# Création du fichier CSV
file = open("product.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(file)

writer.writerow([
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
])

writer.writerow([
    url,
    upc,
    title,
    price_including_tax,
    price_excluding_tax,
    number_available,
    product_description,
    category,
    review_rating,
    image_url
])

file.close()

print("Scraping terminé")