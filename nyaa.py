from bs4 import BeautifulSoup
import requests
# from urlparse import urlparse
import re

FOLLOWED_SHOWS = {"Sword Art Online": ["Commie", "HorribleSubs"],
                  "Aldnoah": ["HorribleSubs", "Commie"],
                  "Majimoji Rurumo": ["HorribleSubs"]}
MAX_LOOPS = 10


def valid_download(file_name):
    # standard check for null and make sure the file type is mkv
    if file_name is None or ".mkv" not in file_name:
        return False
    found = False

    if "[480p]" in file_name or "[1080p]" in file_name:
        return False

    # check a list of followed shows
    for key in FOLLOWED_SHOWS:
        for show in FOLLOWED_SHOWS[key]:
            if key in file_name and "["+show+"]" in file_name:
                found = True

    # this weird style is in case I want to add logic after this
    if not found:
        return False

    # check a list of approved fansub groups
    return True

base_url = "http://www.nyaa.se/?cats=1_37"  # category for english-translated anime
url2 = "http://www.nyaa.se"  # base url in case the category doesn't work

for i in range(1, MAX_LOOPS):
    url = base_url+"&offset="+str(i)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #print soup.prettify()

    anime = soup.find_all(href=re.compile("view"))
    to_download = set()

    for element in anime:
        dl_link = str(element['href']).replace("?page=view", "?page=download")
        text = element.getText().replace("_", " ")
        if valid_download(text):
            print dl_link, text
            to_download.add(dl_link)

    #parsed_link = urlparse(link)
    #base_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)