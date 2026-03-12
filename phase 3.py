import requests
import csv
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"

# ouvrir la page principale
page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")

# trouver les catégories
categories = soup.find("ul", class_="nav-list").find_all("a")

# créer le fichier csv
file = open("books.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(file)

# écrire les colonnes
writer.writerow([
"product_page_url",
"title",
"price",
"category",
"image_url"
])

# boucle sur les catégories
for category in categories[1:]:

    category_name = category.text.strip()
    category_url = base_url + category["href"]

    page_cat = requests.get(category_url)
    soup_cat = BeautifulSoup(page_cat.content, "html.parser")

    books = soup_cat.find_all("h3")

    # boucle sur les livres
    for book in books:

        link = book.find("a")["href"]
        book_url = base_url + "catalogue/" + link.replace("../", "")

        page_book = requests.get(book_url)
        soup_book = BeautifulSoup(page_book.content, "html.parser")

        # titre
        title = soup_book.find("h1").text

        # prix
        price = soup_book.find("p", class_="price_color").text

        # image
        image = soup_book.find("img")["src"]
        image_url = base_url + image.replace("../", "")

        # écrire dans le csv
        writer.writerow([
        title,
        price,
        category_name,
        image_url
        ])

file.close()

print("Scraping terminé")