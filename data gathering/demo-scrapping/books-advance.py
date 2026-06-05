import requests
import pandas as pd
import time

data = []

print("Scraping Open Library...")

for page in range(1, 5):  

    url = "https://openlibrary.org/search.json"

    params = {
        "q":        "fiction",   # change to any topic you like
        "limit":    100,
        "page":     page,
        "fields":   "title,author_name,first_publish_year,isbn,"
                    "publisher,language,subject,number_of_pages_median,"
                    "ratings_average,ratings_count,want_to_read_count,"
                    "currently_reading_count,already_read_count"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error on page {page}: {response.status_code}")
        break

    books = response.json().get("docs", [])

    if not books:
        print("No more books found.")
        break

    for book in books:
        data.append({
            "Title":           book.get("title", ""),
            "Author":          ", ".join(book.get("author_name", [])),
            "First Published": book.get("first_publish_year", ""),
            "Publisher":       ", ".join(book.get("publisher", [])[:2]),  # first 2
            "ISBN":            (book.get("isbn") or [""])[0],
            "Language":        ", ".join(book.get("language", [])),
            "Pages":           book.get("number_of_pages_median", ""),
            "Subjects":        ", ".join(book.get("subject", [])[:3]),    # first 3
            "Avg Rating":      book.get("ratings_average", ""),
            "Rating Count":    book.get("ratings_count", ""),
            "Want to Read":    book.get("want_to_read_count", ""),
            "Reading Now":     book.get("currently_reading_count", ""),
            "Already Read":    book.get("already_read_count", ""),
        })

    print(f"Page {page}/500 done — total rows: {len(data)}")
    time.sleep(0.5)   # be polite


df = pd.DataFrame(data)
df.to_csv("openlibrary_50k.csv", index=False)

print(f"\nDone! Rows: {len(df)} | Columns: {len(df.columns)}")