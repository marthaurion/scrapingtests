from bs4 import BeautifulSoup
import requests
from urlparse import urlparse
import re

FOLLOWED_SHOWS = ["Akame ga Kill", "Blade Dance", "Gundam SEED Destiny"]
FANSUBS = ["HorribleSubs", "Commie", "Hatsuyuki"]
MAX_LOOPS = 10

def valid_download(input):
    # standard check for null and make sure the filetype is mkv
    if input is None or ".mkv" not in input:
        return False
    found = False

    # check a list of followed shows
    for show in FOLLOWED_SHOWS:
        if show in input:
            found = True

    # check a list of fansub groups
    for sub in FANSUBS:
        if sub in input:
            found = True

    # right now, using OR logic for fansub groups and episode titles
    # might need to change this later to be more specific
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
        dl_link = str(element['href']).replace("?page=view","?page=download")
        text = element.getText().replace("_"," ")
        if valid_download(text):
            print dl_link, text
            to_download.add(dl_link)

    #parsed_link = urlparse(link)
    #base_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)