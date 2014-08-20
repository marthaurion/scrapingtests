import requests
#from urlparse import urlparse
#import re
import json
import psycopg2
import sys


def load_manga_list(con, cursor):
    manga_list = "https://www.mangaeden.com/api/list/0/"
    r = requests.get(manga_list)
    data = r.text

    result = json.loads(data)
    #print result

    # check for source information
    cursor.execute("SELECT id, title FROM manga.sources WHERE title = %s;", ("MangaEden",))
    temp_source = cursor.fetchone()
    if temp_source is None:
        cursor.execute("INSERT INTO manga.sources(title) VALUES(%s);", ("MangaEden",))
        con.commit()
        cursor.execute("SELECT id, title FROM manga.sources WHERE title = %s;", ("MangaEden",))
        source_id = cursor.fetchone()[0]
    else:
        source_id = temp_source[0]

    query = "INSERT INTO manga.series(manga_id, title, alias, image_url, source_site) values(%s, %s, %s, %s, %s);"
    for item in result['manga']:
        # loop through all items in the manga list and insert them into the manga database if they don't exist already
        try:
            cursor.execute(query, (item['i'], item['t'].encode('utf8'), item['a'], item['im'], source_id))
        # the intent is that this will skip an insert if a duplicate key is found
        except psycopg2.IntegrityError:
            con.rollback()
        else:
            con.commit()


# given a manga id load its metadata and chapter information
def manga_metadata(con, cursor, manga_name):
    cursor.execute("SELECT manga_id FROM manga.series WHERE title = %", (manga_name,))
    manga_id = cursor.fetchone()[0]
    if manga_id is None:
        return

    # get metadata about each specific manga and a chapter list
    manga_info_base = "https://www.mangaeden.com/api/manga/" + str(manga_id) + "/"
    result = json.loads(requests.get(manga_info_base).text)

    desc = result['description'].encode('utf8')
    cursor.execute("UPDATE manga.series SET description = %s WHERE manga_id = %s;", (desc, manga_id))
    con.commit()

    cursor.execute("SELECT id FROM manga.series WHERE manga_id = %s;", (manga_id,))
    series_id = cursor.fetchone()[0]

    update_categories(con, cursor, result['categories'], series_id)

    update_chapters(con, cursor, result['chapters'], series_id)


# might be better to do this as a separate function to call separately from the main batch
def update_categories(con, cursor, cats, series_id):
    for cat in cats:
        # first try to add the category if it doesn't exist
        try:
            cursor.execute("INSERT INTO manga.categories(title) VALUES(%s);", (cat,))
        except psycopg2.IntegrityError:
            con.rollback()
        else:
            con.commit()

        cursor.execute("SELECT id FROM manga.categories WHERE title = %s;", (cat,))
        cat_id = cursor.fetchone()[0]

        # now associate with series
        query = "INSERT INTO manga.ser_cat_r(series_id, category_id) VALUES(%s, %s);"
        try:
            cursor.execute(query, (series_id, cat_id))
        except psycopg2.IntegrityError:
            con.rollback()
        else:
            con.commit()


def update_chapters(con, cursor, chaps, series_id):
    # quick error check
    if chaps is None or len(chaps) < 1:
        return

    query = "INSERT INTO manga.chapters(chap_id, chap_num, series_id, chap_title) VALUES(%s, %s, %s, %s);"
    for chap in chaps:
        if chap[2] is None:
            chap_title = chap[2]
        else:
            chap_title = chap[2].encode('utf8')

        try:
            cursor.execute(query, (chap[3], chap[0], series_id, chap_title))
        except psycopg2.IntegrityError:
            con.rollback()
        else:
            con.commit()
            update_pages(con, cursor, chap[3])


def update_pages(con, cursor, chap_id):
    chapter_pages = "https://www.mangaeden.com/api/chapter/" + str(chap_id) + "/"
    result = json.loads(requests.get(chapter_pages).text)

    cursor.execute("SELECT id FROM manga.chapters WHERE chap_id = %s;", (chap_id,))
    c_id = cursor.fetchone()[0]

    query = "INSERT INTO manga.pages(chap_id, page_num, page_url) VALUES(%s, %s, %s);"
    for item in result['images']:
        try:
            cursor.execute(query, (c_id, item[0], item[1]))
        except psycopg2.IntegrityError:
            con.rollback()
        else:
            con.commit()

conn = psycopg2.connect("dbname=scratchdb user=marth")
cur = conn.cursor()

comm = int(sys.argv[1])
title = str(sys.argv[2])

if title is None:
    load_manga_list(conn, cur)
else:
    manga_metadata(conn, cur, title)

cur.close()
conn.close()
