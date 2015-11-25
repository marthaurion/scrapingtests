from bs4 import BeautifulSoup
import requests
import re

#MAX_LOOPS = 504  # max page for comic list
MAX_LOOPS = 4


def load_manga_list();
    f = open('output.txt', 'w')

    for i in range(MAX_LOOPS):
        base_url = "http://www.bato.to/search"
        url = base_url+"?&p="+str(i)

        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        #print soup.prettify()
        #print soup

        anime = soup.find_all(href=re.compile("comic"))

        for element in anime:
            f.write(element['href']+'\n')
            f.write(element.getText().encode('ascii','backslashreplace').decode('ascii') + '\n')

    f.close()
    
def load_manga_series(series_url):
    pass
    
load_manga_list()