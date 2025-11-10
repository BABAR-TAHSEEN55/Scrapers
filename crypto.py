# Extracts the Crypto Currency Present Rate
import os
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

URl = os.getenv("URL")


result = requests.get(URl).text

doc = BeautifulSoup(result, "html.parser")
tbody = doc.tbody
trs = tbody.contents
# print(trs)

prices = {}
for tr in trs[:10]:
    name = tr.find("p", class_="coin-item-name")
    price = tr.find(string=re.compile(r"\$.*"))

    if price and name:
        print(f"{name.text}    {price}")
        prices[name.text] = price.strip()

print(prices)
