# import random
# import time
# from random import choice
# from socket import timeout

# import requests
# from bs4 import BeautifulSoup
# from requests.adapters import HTTPAdapter, Retry
# from requests.sessions import Session

# URL = "https://quotes.toscrape.com"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Referer": "https://google.com/",
# }

# session = requests.Session()

# # Max retries Logic
# retries = Retry(
#     total=5,
#     backoff_factor=0.5,
#     status_forcelist=[429, 500, 502, 503, 504],
#     allowed_methods=["GET", "HEAD", "OPTIONS"],
# )
# session.mount("https://", HTTPAdapter(max_retries=retries))
# session.mount("http://", HTTPAdapter(max_retries=retries))

# response = session.get(URL, timeout=10)

# # Proxies to avoid Banning of IP

# proxies_list = ["http://1.2.3.4:8080", "http://5.6.7.8:8080", "http://9.10.11.12:3128"]
# proxy = {"https": random.choice(proxies_list), "http": random.choice(proxies_list)}


# response = session.get(URL, timeout=10, proxies=proxy)

# with requests.Session() as session:
#     res = session.get(
#         URL, headers=headers, timeout=(5, 10)
#     )  # 5s-> Connect : 15s -> Read
#     res.raise_for_status()  # Status Code
#     soup = BeautifulSoup(res.content, "lxml")
#     quotes = [
#         q.select_one("span.text").get_text(strip=True) for q in soup.select("div.quote")
#     ]
#     print(quotes[:3])


# Robots txt
# from urllib.robotparser import RobotFileParser

# import requests

# robo = RobotFileParser()
# robo.set_url("https://quotes.toscrape.com/robots.txt")
# robo.read()

# if robo.can_fetch("*", "https://google.com/private/data"):
#     print("Allowed")
# else:
#     print("Not Allowed")
