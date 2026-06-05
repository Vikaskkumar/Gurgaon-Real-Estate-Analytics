import requests
from bs4 import BeautifulSoup
import pandas as pd

all_data = []

for page in range(1, 51):
    print("Scraping page:", page)

    url = f"https://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    if len(quotes) == 0:
        print(f"\nWebsite has only {page-1} pages.")
        print(f"Stopping at page {page}")
        break

    for q in quotes:
        quote = q.find("span", class_="text").text
        author = q.find("small", class_="author").text

        tags = []
        all_tags = q.find_all("a", class_="tag")

        for tag in all_tags:
            tags.append(tag.text)

        all_data.append({
            "Page": page,
            "Quote": quote,
            "Author": author,
            "Tags": ", ".join(tags)
        })

df = pd.DataFrame(all_data)
df.to_csv("quotes.csv", index=False)

print("\nScraping completed!")
print("Total rows:", len(df))