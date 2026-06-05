import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"

response = requests.get(url)
print("status:",response.status_code)

# parsing html
soup = BeautifulSoup(response.text,"html.parser")

quotes = soup.find_all("div",class_="quote")

data = []

for q in quotes:
    quote = q.find("span",class_="text").text
    author = q.find("small",class_="author").text
    tags = [tag.text for tag in q.find_all("a",class_="tag")]
    
    data.append({
        "Quote":quote,
        "Author":author,
        "Tags": ",".join(tags)
    })
    
# print(data)

df = pd.DataFrame(data)
# print(df.head())
df.to_csv("quotes.csv",index=False)
print("csv file saved")
