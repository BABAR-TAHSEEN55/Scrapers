import re

import requests
from bs4 import BeautifulSoup

# Url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# result = requests.get(Url)
# # print(result.text)
# doc = BeautifulSoup(result.text, "html.parser")
# title = doc.title
# print(title.string)

# print(res)
# res = doc.find_all(string="51")


# print(doc.prettify())

with open("index.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")
    title = doc.title
    # result = doc.find("option")
    # resutl = doc.find_all(["p"], class_="yolo")
    result = doc.find_all(string=re.compile("\$.*"), limit=1)

print(result)
for i in result:
    print(i.strip())
# result[""] = "new Value"
# result["color"] = "blue"
# print(result)
# print(title.string)
# print(result.attrs)
