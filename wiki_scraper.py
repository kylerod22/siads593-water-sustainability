import requests
import pandas as pd
from io import StringIO

# Scrape a list of rivers from South Africa @ https://en.wikipedia.org/wiki/List_of_rivers_of_South_Africa
# Custom headers to mimic a real browser
def wiki_scraper(url="https://en.wikipedia.org/wiki/List_of_rivers_of_South_Africa", headers={"User-Agent": "Chrome/107.0.0.0 Safari/537.36"}, table=1, subset='Mouth / junction coordinates'):

    # Wikipedia URL
    url = url

    # Send HTTP request with headers
    response = requests.get(url, headers=headers) #https://requests.readthedocs.io/en/latest/

    # Read HTML tables from the response content
    tables = pd.read_html(StringIO(response.text))

    # the second table happens to be where it's at
    rivers = tables[table].dropna(subset=subset)

    # clean columns
    def split_join_lower(string: str):
        # a = "Drainage basin[A] "
        lst = string.split()
        return ''.join(lst).lower()
    rivers.columns = [split_join_lower(s) for s in rivers.columns] # .strip() could be added
    # df.columns = df.columns.str.strip().str.lower()

    return rivers