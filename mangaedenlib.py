import requests
#from urlparse import urlparse
#import re
import json
import sys
import win_unicode_console


class MangaObject:
    def __init__(self, json, manga_id):
        self.manga_id = manga_id
        self.title = json['title']
        self.description = json['description']
        self.image_url = json['image']
    
    def __str__(self):
        return "[" + self.manga_id + "] " + self.title + "\n" + self.description

class MangaListObject:
    def __init__(self, json):
        self.manga_id = json['i']
        self.title = json['t']
        self.alias = json['a']
        self.image_url = json['im']
        
    def __str__(self):
        return "[" + self.manga_id + "] " + self.title
    
def check_manga_count():
    manga_list = "https://www.mangaeden.com/api/list/0/"
    r = requests.get(manga_list)
    data = r.text

    result = json.loads(data)
    print(len(result['manga']))


def load_manga_list():
    manga_list = "https://www.mangaeden.com/api/list/0/"
    r = requests.get(manga_list)
    data = r.text

    result = json.loads(data)
    #print result
    
    manga_list = {}
    
    for item in result['manga']:
        temp = Manga(item)
        manga_list[item['i']] = temp
        
    print(manga_list['5372395745b9ef5a0b1d226b'])

    return manga_list

def get_manga_object(manga_id):
    manga_info_base = "https://www.mangaeden.com/api/manga/" + str(manga_id) + "/"
    manga_json = json.loads(requests.get(manga_info_base).text)
    return manga_json


# # might be better to do this as a separate function to call separately from the main batch
# def update_categories(con, cursor, cats, series_id):
    # for cat in cats:
        # # first check whether the category is already in the database
        # cursor.execute("SELECT id FROM categories WHERE title = %s;", (cat,))
        # result = cursor.fetchone()

        # # add the category if it doesn't exist
        # if result is None:
            # try:
                # cursor.execute("INSERT INTO categories(title) VALUES(%s);", (cat,))
            # except psycopg2.IntegrityError:
                # con.rollback()
            # else:
                # con.commit()

            # # now we should be able to get a category id
            # cursor.execute("SELECT id FROM categories WHERE title = %s;", (cat,))
            # cat_id = cursor.fetchone()[0]
        # else:
            # cat_id = result[0]

        # # random error checking
        # if cat_id is None:
            # print "CATEGORY IS STILL NOT FOUND."
            # return

        # # now associate with series
        # query = "INSERT INTO category_r(series_id, category_id) VALUES(%s, %s);"
        # try:
            # cursor.execute(query, (series_id, cat_id))
        # except psycopg2.IntegrityError:
            # con.rollback()
        # else:
            # con.commit()


# def update_chapters(con, cursor, manga_name):
    # cursor.execute("SELECT id, manga_id FROM manga.series WHERE title = %s", (manga_name,))
    # result = cursor.fetchone()
    # if result is not None:
        # manga_id = result[1]
        # series_id = result[0]
    # else:
        # return

    # # get metadata about each specific manga and a chapter list
    # manga_info_base = "https://www.mangaeden.com/api/manga/" + str(manga_id) + "/"
    # result = json.loads(requests.get(manga_info_base).text)

    # chaps = result['chapters']

    # # quick error check
    # if chaps is None or len(chaps) < 1:
        # return

    # query = "INSERT INTO chapters(chap_id, chap_num, series_id, chap_title) VALUES(%s, %s, %s, %s);"
    # for chap in chaps:
        # if chap[2] is None:
            # chap_title = chap[2]
        # else:
            # chap_title = chap[2].encode('utf8')

        # try:
            # cursor.execute(query, (chap[3], chap[0], series_id, chap_title))
        # except psycopg2.IntegrityError:
            # con.rollback()
        # else:
            # con.commit()
            # update_pages(con, cursor, chap[3])


# def update_pages(con, cursor, chap_id):
    # chapter_pages = "https://www.mangaeden.com/api/chapter/" + str(chap_id) + "/"
    # result = json.loads(requests.get(chapter_pages).text)

    # cursor.execute("SELECT id FROM chapters WHERE chap_id = %s;", (chap_id,))
    # c_id = cursor.fetchone()[0]

    # query = "INSERT INTO pages(chap_id, page_num, page_url) VALUES(%s, %s, %s);"
    # for item in result['images']:
        # try:
            # cursor.execute(query, (c_id, item[0], item[1]))
        # except psycopg2.IntegrityError:
            # con.rollback()
        # else:
            # con.commit()

win_unicode_console.enable()

#load_manga_list()
manga = get_manga_object('4e70e9f6c092255ef7004336')
obj = MangaObject(manga, '4e70e9f6c092255ef7004336')

manga2 = get_manga_object('5372395745b9ef5a0b1d226b')
obj2 = MangaObject(manga2, '5372395745b9ef5a0b1d226b')


print(obj)
print(obj2)