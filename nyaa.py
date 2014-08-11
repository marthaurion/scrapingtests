from bs4 import BeautifulSoup
import requests
# from urlparse import urlparse
# from subprocess import call
import re
import os
import urllib

FOLLOWED_SHOWS = {"Sword Art Online": ["Commie", "HorribleSubs"],
                  "Aldnoah": ["HorribleSubs", "Commie"],
                  "Majimoji Rurumo": ["HorribleSubs"],
                  "Prisma Ilya": ["HorribleSubs", "UTW"]}
MAX_LOOPS = 10


def valid_download(file_name):
    # standard check for null and make sure the file type is mkv
    if file_name is None or ".mkv" not in file_name:
        return False

    if "[480p]" in file_name or "[1080p]" in file_name:
        return False

    # check a list of followed shows
    for key in FOLLOWED_SHOWS:
        for sub in FOLLOWED_SHOWS[key]:
            sub_test = "["+sub.lower()+"]" in file_name.lower()
            if key.lower() in file_name.lower() and sub_test:
                return True

    # default to false
    return False

base_url = "http://www.nyaa.se/?cats=1_37"  # category for english-translated anime
url2 = "http://www.nyaa.se"  # base url in case the category doesn't work

base_dir = os.getcwd()
dirname = base_dir + "/torrents/pending/"
if not os.path.exists(dirname):
    os.makedirs(dirname)

random_file = urllib.URLopener()

for i in range(1, MAX_LOOPS):
    url = base_url+"&offset="+str(i)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #print soup.prettify()

    anime = soup.find_all(href=re.compile("view"))

    for element in anime:
        dl_link = str(element['href']).replace("?page=view", "?page=download")
        text = element.getText().replace("_", " ")
        if valid_download(text):
            print dl_link, text
            # if we haven't downloaded the files, download them
            if not os.path.exists(dirname + text):
                random_file.retrieve(dl_link, dirname + text)

    #parsed_link = urlparse(link)
    #base_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)

#call(["rtorrent", to_download.pop()])
