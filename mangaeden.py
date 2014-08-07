import requests
#from urlparse import urlparse
#import re
import json

MAX_LOOPS = 390 # max page for comic list

manga_list = "https://www.mangaeden.com/api/list/0/"
r = requests.get(manga_list)
data = r.text

result = json.loads(data)
print result

#get metadata about each specific manga and a chapter list
#manga_info_base = "https://www.mangaeden.com/api/manga/" # add manga.id at the end of the url to get the manga info

#get image urls for chapter pages for each chapter
#chapter_pages = "https://www.mangaeden.com/api/chapter/" # add chapter.id at the end of the url to get the chapter info

#print data

#soup = BeautifulSoup(data)

#print soup.prettify()
#print soup;

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
