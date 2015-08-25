from bs4 import BeautifulSoup
import requests
import re
import os
import urllib

FOLLOWED_SHOWS = {"Teekyu": ["Commie", "HorribleSubs"],
                  "Joukamachi no Dandelion": ["HorribleSubs"],
				  "Million Doll": ["HorribleSubs"],
                  "Jitsu wa Watashi wa": ["HorribleSubs"]}
MAX_LOOPS = 20


def valid_download(file_name, show_list):
    # standard check for null and make sure the file type is mkv
    if file_name is None or ".mkv" not in file_name:
        return False

    if "[480p]" in file_name or "[1080p]" in file_name:
        return False

    # check a list of followed shows
    for key in show_list:
        for sub in show_list[key]:
            sub_test = "["+sub.lower()+"]" in file_name.lower()
            if key.lower() in file_name.lower() and sub_test:
                return True

    # default to false
    return False


def download_anime(show_list, base_url, base_dir):
    dirname = base_dir + "/torrents/"
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for i in range(1, MAX_LOOPS):
        url = base_url+"&offset="+str(i)

        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        anime = soup.find_all(href=re.compile("view"))

        for element in anime:
            dl_link = str(element['href']).replace("?page=view", "?page=download")
            text = element.getText().replace("_", " ")
            if valid_download(text, show_list):
                print (dl_link, text)
                # if we haven't downloaded the files, download them
                filename = dirname + text + ".torrent"
                if not os.path.exists(filename):
                    with urllib.request.urlopen(dl_link) as response, open(filename, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)

def browse_site(base_url, loops=1):
    for i in range(1, loops+1):
        url = base_url+"&offset="+str(i)
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        anime = soup.find_all(href=re.compile("view"))
        for element in anime:
            text = element.getText().replace("_", " ").encode("utf8")
            print(text)

wurl = "http://www.nyaa.se/?cats=1_37"  # category for english-translated anime
wdir = os.getcwd()

#browse_site(wurl,2)
download_anime(FOLLOWED_SHOWS, wurl, wdir)
