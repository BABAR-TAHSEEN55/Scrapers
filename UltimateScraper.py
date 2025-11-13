import os
import random
import sqlite3
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter, Retry

load_dotenv()


def Insert(quotes, cur, conn):
    for quote_data in quotes:
        tags_str = ", ".join(quote_data["tags"])
        cur.execute(
            "INSERT INTO Quotes (quote,author,tags) VALUES (?,?,?)",
            (quote_data["quote"], quote_data["author"], tags_str),
        )
        # print(f"Inserted successfully")
    print("Inserted Successfully")


def GetData(cur):
    cur.execute("SELECT * FROM Quotes")
    data = cur.fetchall()
    return data


URL2 = os.getenv("URL2")
ROBO = os.getenv("ROBO_URL")

if not URL2:
    raise ValueError("URL2 Environmental Variable is required!")
if not ROBO:
    raise ValueError("ROBO  Variable is required!")

robo = RobotFileParser()
robo.set_url(ROBO)
robo.read()

if not robo.can_fetch("*", URL2):
    raise Exception("Scraping not Allowed")

conn = sqlite3.connect("scrape.db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS Quotes (quote VARCHAR,author VARCHAR , tags VARCHAR)"
)
conn.commit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://google.com/",
}

session = requests.Session()
retries = Retry(
    total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504, 403]
)
session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount("http://", HTTPAdapter(max_retries=retries))


proxies_list = ["http://1.2.3.4:8080", "http://5.6.7.8:8080", "http://9.10.11.12:3128"]
proxy = {"http": random.choice(proxies_list), "https": random.choice(proxies_list)}


try:
    # res = session.get(URL2, headers=headers, timeout=10)
    # res.raise_for_status()

    # soup = BeautifulSoup(res.content, "lxml")
    # body = soup.body
    # # print(body)
    # href = body.find_all("a")
    # # print(href)
    # for i in href:
    #     print(i)
    #     print()
    quotes = []
    links = []
    # quote_traverse = soup.select("ul.pager li.next a")
    # quote_end = soup.select("ul.pager li.previous")
    current_url = URL2
    while True:
        print(f"Scraping {current_url}")
        res = session.get(current_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "lxml")

        # Process quotes on current page
        quote_divs = soup.select("div.quote")

        for quotes_div in quote_divs:
            quotest_text = quotes_div.select_one("span.text").get_text()
            quotest_author = quotes_div.select_one("small.author").get_text()
            quotest_tags = quotes_div.select("div.tags a.tag")
            tags = [tag.get_text(strip=True) for tag in quotest_tags]
            # print(tags)
            # print(quotest_text)
            # print(quotest_author)

            quotes.append(
                {"quote": quotest_text, "author": quotest_author, "tags": tags}
            )

        # Check for next page
        quote_traverse = soup.select("ul.pager li.next a")
        if quote_traverse:
            href = quote_traverse[0].get("href")
            if href:
                fullUrl = urljoin(URL2, href)
                current_url = fullUrl
                links.append(fullUrl)
                current_url = fullUrl
                time.sleep(3)
                # print(href)
            else:
                break
        else:
            break

        # for span in spans:
        #     print(span.get_text())
        #     print()

    # quotes = [
    #     q.select_one("span").get_text(strip=True) for q in soup.select("div.quote")
    # ]
    # print(quotes)

    # print(res.text[:500])
    for i, v in enumerate(quotes):
        print(v)
        print()

    Insert(quotes, cur, conn)
    conn.commit()

    # result = GetData(cur)
    # print(result)
    # conn.close()
    print(links)
    print(len(quotes))


except requests.exceptions.RequestException as e:
    print("Exception:", e)
