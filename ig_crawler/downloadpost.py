import time

from bs4 import BeautifulSoup as Soup
import json
import os
import requests
from selenium import webdriver
import sqlite3

import init


def main(islogin, browser, database_name, username):
    # 提取資料庫
    # database_name = 'test.db'
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    # sql_query = "SELECT * FROM Instagram"
    # sql_query = "SELECT * FROM Instagram WHERE username='yuen_nnnnnn'"
    # sql_query = "SELECT * FROM Instagram WHERE username='mo_onbyul'"
    # sql_query = "SELECT * FROM Instagram WHERE username='whee_inthemood'"
    # sql_query = "SELECT * FROM Instagram WHERE username='_mariahwasa'"
    # sql_query = "SELECT * FROM Instagram WHERE username='mamamoo_official'"
    #
    sql_query = "SELECT * FROM '{Table_name}' WHERE ( is_download ='False' ) "
    sql_query = sql_query.format(Table_name=username)
    result = cursor.execute(sql_query).fetchall()
    if (len(result) < 1):
        print("All post is download: len(result):" + str(len(result)))
        return
    cursor.close()
    con.close()
    file_loc_str = './media/'
    file_loc_str = file_loc_str + result[0][0] + "/"

    os.makedirs(file_loc_str, exist_ok=True)
    # os.makedirs('./media/mo_onbyul/', exist_ok=True)

    post_pre_url = init.url_prefix_post
    print("total post: " + str(len(result)))
    if (islogin == False):
        browser = webdriver.Chrome()
        browser.implicitly_wait(30)

    # for i in range(20):
    for i in range(len(result)):
        # need wait some time to avoid blockade
        time.sleep(1)

        file_loc_str = './media/'
        file_loc_str = file_loc_str + result[i][0] + "/"  # username
        file_name = result[i][5]  # shortcode
        post_url = post_pre_url + file_name + "/"
        counter = 0
        while (1):
            try:
                counter = counter + 1
                browser.get(post_url)
                soup = Soup(browser.page_source, "lxml")
                xhr = soup.find_all(type='text/javascript')
                print("xhr over")
                shortcode_media = getmedia(islogin, file_name, xhr, soup)
                print("shortcode over")
                save_media(shortcode_media, file_loc_str, file_name, database_name, username)
                break
            except:
                if (soup.text.find('協助我們確認您的身分') != -1 or counter > 15):
                    print("帳號遭鎖定")
                    # os.system("pause")
                    input()
                time.sleep(2)
                print("loading webpage fail... try again")

        # shortcode_media = getmedia(islogin, file_name, xhr, soup)
        # save_media(shortcode_media, file_loc_str, file_name,database_name)


def getmedia(islogin, file_name, xhr, soup):
    if (islogin):
        print("islogin:" + str(islogin))

        for xhr_i in xhr:
            try:
                json_str = str(xhr_i)[68 + len(file_name):-11]
                js_data = json.loads(json_str, encoding='utf-8')
                shortcode_media = js_data['graphql']['shortcode_media']
                return shortcode_media
            except:
                # print("wrong xhr_i")
                if (soup.text.find('協助我們確認您的身分') != -1):
                    print("帳號遭鎖定")
                    print("loading webpage fail... try again")
                    input()
    else:
        print("islogin:" + str(islogin))
        json_str = str(xhr[15])[52:-10]  # 沒登入/
        js_data = json.loads(json_str, encoding='utf-8')
        shortcode_media = js_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        return shortcode_media


def updateDB(file_name, database_name, _Table_name):
    # 已存
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    sql_isdownload_pre = "update '{Table_name}' set is_download='Ture' where shortcode = '"
    sql_isdownload_pre = sql_isdownload_pre.format(Table_name=_Table_name)
    sql_isdownload = sql_isdownload_pre + file_name + "'"
    sql_isdownload
    cursor.execute(sql_isdownload)
    con.commit()
    cursor.close()
    con.close()
    print("DB is_download = True")


def save_media(shortcode_media, file_loc_str, file_name, database_name, _Table_name):
    if ('edge_sidecar_to_children' in shortcode_media):
        # isSingle=False
        print("True :　is multi media")
        edges = shortcode_media['edge_sidecar_to_children']['edges']
        for i in range(len(edges)):
            is_video = edges[i]['node']['is_video']
            if (is_video):
                media_link = edges[i]['node']['video_url']
                file_type = '.mp4'
            else:
                media_link = edges[i]['node']['display_resources'][-1]['src']
                file_type = '.jpg'
            media = requests.get(media_link)
            print("write file : " + file_loc_str + file_name + "_" + str(i) + file_type)
            with open(file_loc_str + file_name + '_' + str(i) + file_type, 'wb') as f:
                f.write(media.content)
    else:
        # isSingle = True
        print("False : is single media ")
        edges = shortcode_media
        is_video = edges['is_video']
        if (is_video):
            media_link = edges['video_url']
            print(media_link)
            file_type = '.mp4'
            if (media_link == 'https://static.cdninstagram.com/rsrc.php/null.jpg'):
                print('Fail in this video:' + _Table_name + ', file_name: ' + file_name)
                return
        else:
            media_link = edges['display_resources'][-1]['src']
            file_type = '.jpg'
        media = requests.get(media_link)
        print("write file : " + file_loc_str + file_name + "_" + file_type)
        with open(file_loc_str + file_name + '_' + file_type, 'wb') as f:
            f.write(media.content)

    updateDB(file_name, database_name, _Table_name)
