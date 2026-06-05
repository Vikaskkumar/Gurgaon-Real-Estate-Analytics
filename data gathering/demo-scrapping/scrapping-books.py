import requests
import pandas as pd
from bs4 import BeautifulSoup

data = []

for page in range(1, 100):
    print(f"Scraping page-{page}")

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print(f"\nWebsite only has {page-1} pages")
        break

    for book in books:
        data.append({
            "Page": page,
            "Title": book.h3.a["title"],
            "Price": book.find("p", class_="price_color").text,
            "Availability": book.find("p", class_="instock availability").text.strip(),
            "Rating": book.find("p", class_="star-rating")["class"][1]
        })

df = pd.DataFrame(data)
df.to_csv("books.csv", index=False)

print("\nDone!")
print("Total books:", len(df))
print("Total pages:", page-1)