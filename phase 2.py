import requests
import csv
from bs4 import BeautifulSoup

# Page d'une catégorie
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# Aller sur la page
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Trouver tous les livres
books = soup.find_all("h3")

# Créer le CSV
file = open("phase2_category.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(file)

# Colonnes
writer.writerow(["title", "price"])

# Boucle sur chaque livre
for book in books:

    # Lien du livre
    link = book.find("a")["href"]
    book_url = "https://books.toscrape.com/catalogue/" + link.replace("../", "")

    # Aller sur la page du livre
    book_page = requests.get(book_url)
    book_soup = BeautifulSoup(book_page.content, "html.parser")

    # Infos du livre
    title = book_soup.find("h1").text
    price = book_soup.find("p", class_="price_color").text

    # Écrire dans le CSV
    writer.writerow([title, price])

# Fermer le fichier
file.close()
print("Scraping terminé")