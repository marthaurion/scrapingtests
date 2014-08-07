from bs4 import BeautifulSoup
import requests
from urlparse import urlparse
import re

MAX_LOOPS = 390 # max page for comic list

#base_url = "http://www.batoto.net/search"
#url = base_url+"?&p="+str(i)

url = "http://www.batoto.net/search"

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

#print soup.prettify()
print soup;

#anime = soup.find_all(href=re.compile("view"))
#to_download = set()

#for element in anime:
#    dl_link = str(element['href']).replace("?page=view","?page=download")
#    text = element.getText().replace("_"," ")
#    if valid_download(text):
#        print dl_link, text
#        to_download.add(dl_link)

#parsed_link = urlparse(link)
#base_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_link)
