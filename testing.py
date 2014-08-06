from bs4 import BeautifulSoup
import requests
from urlparse import urlparse

HARD_LIMIT = 200

links = set()
links.add("http://www.marthaurion.com")
saved = set()

while len(saved) < HARD_LIMIT:
    next_iter = set()
    for url in links:
        if len(saved) >= HARD_LIMIT:
            break

        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        for link in soup.find_all('a'):
            if len(saved) >= HARD_LIMIT:
                break

            link = link.get('href')
            if link is None or "http" not in link:
                continue

            parsed_link = urlparse(link)
            base_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)
            if base_link not in saved:
                next_iter.add(base_link)
                saved.add(base_link)

    links = set()
    for link in next_iter:
        links.add(link)

ctr = 0
for link in saved:
    ctr += 1
    print ctr, link