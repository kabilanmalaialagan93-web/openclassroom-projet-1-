import requests
import csv
import os
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"

# 👉 ajout : dossier images
os.makedirs("images", exist_ok=True)

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
for category in categories:

    category_name = category.text.strip()
    category_url = base_url + category["href"]

    # 👉 ajout pagination
    next_page = category_url

    while next_page:

        page_cat = requests.get(next_page)
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

            # 👉 modif : nom + dossier images
            image_name = image.split("/")[-1]
            image_path = os.path.join("images", image_name)

            request_image = requests.get(image_url)
            with open(image_path, "wb") as f:
                f.write(request_image.content)

            # écrire dans le csv
            writer.writerow([
                book_url,
                title,
                price,
                category_name,
                image_url
            ])

        # 👉 ajout : passer à la page suivante
        next_button = soup_cat.find("li", class_="next")

        if next_button:
            next_link = next_button.find("a")["href"]
            next_page = base_url + "catalogue/" + next_link
        else:
            next_page = None

file.close()

print("Scraping terminé")