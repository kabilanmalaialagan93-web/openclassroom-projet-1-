import requests
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL du site
base_url = "https://books.toscrape.com/"

# créer un dossier pour les images
os.makedirs("images", exist_ok=True)

# ouvrir la page principale
page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")

# récupérer les catégories
categories = soup.find("ul", class_="nav-list").find_all("a")

# créer le fichier CSV
with open("books.csv", "w", newline="", encoding="utf-8") as file:
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
        category_url = urljoin(base_url, category["href"])

        # pagination
        next_page = category_url

        while next_page:

            print("Page :", next_page)

            page_cat = requests.get(next_page)
            soup_cat = BeautifulSoup(page_cat.content, "html.parser")

            # récupérer les livres
            books = soup_cat.find_all("h3")

            # boucle sur les livres
            for book in books:

                link = book.find("a")["href"]
                book_url = urljoin(next_page, link)

                page_book = requests.get(book_url)
                soup_book = BeautifulSoup(page_book.content, "html.parser")

                # récupérer les infos
                title = soup_book.find("h1").text
                price = soup_book.find("p", class_="price_color").text

                # image
                image = soup_book.find("img")["src"]
                image_url = urljoin(book_url, image)

                # nom du fichier image
                image_name = image_url.split("/")[-1]
                image_path = os.path.join("images", image_name)

                # télécharger l'image
                response = requests.get(image_url, stream=True)
                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        if chunk:
                            f.write(chunk)

                # écrire dans le CSV
                writer.writerow([
                    book_url,
                    title,
                    price,
                    category_name,
                    image_url
                ])

            # passer à la page suivante
            next_button = soup_cat.find("li", class_="next")

            if next_button:
                next_link = next_button.find("a")["href"]
                next_page = urljoin(next_page, next_link)
            else:
                next_page = None

print("Scraping terminé")