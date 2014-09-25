from bs4 import BeautifulSoup
import requests
import re
import psycopg2

#MAX_LOOPS = 390  # max page for comic list
MAX_LOOPS = 4

conn = psycopg2.connect("dbname=mangadb user=marth")
cur = conn.cursor()

for i in range(MAX_LOOPS):
    base_url = "http://www.batoto.net/search"
    url = base_url+"?&p="+str(i)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    #print soup.prettify()
    #print soup

    anime = soup.find_all(href=re.compile("comic"))

    for element in anime:
        print element['href']
        print element.getText().encode('ascii','xmlcharrefreplace')


cur.close()
conn.close()
