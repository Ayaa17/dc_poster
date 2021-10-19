import ig_crawler.database as database
import ig_crawler.init as init
import json
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
import requests

import ig_crawler.postClass as postClass


def main(browser, url, islogin, database_name, username):
    """
    :param browser:
    :param url:
    :return:
    """

    # 確認DB是否有該表
    database.check(database_name, username)

    counter = 0
    (cursor, flag, user, list_temp) = getfirstxhr(browser, url, islogin)
    print(str(user["id"]))
    database.main_getinfo(list_temp, database_name, username)

    while (flag):
        try:
            counter = counter + 1
            (cursor, flag, list_temp) = getnextxhr(browser, cursor, user["id"], database_name, username)
            database.main_getinfo(list_temp, database_name, username)

            print(cursor, flag)
            print("aleady save : " + str(12 * counter))

        except:
            print("something wrong userid : " + user["id"])
            print("something wrong cursor : " + cursor)

            return


def main_continue(browser, url, islogin, cursor, user_id, database_name, username):
    """
    :param browser:
    :param url:
    :return:
    """
    counter = 0
    flag = True
    while (flag):
        try:
            counter = counter + 1
            (cursor, flag, list_temp) = getnextxhr(browser, cursor, user_id, database_name, username)
            print(cursor, flag)
            # print(list)
            # print(list_temp)
            print("aleady save : " + str(12 * counter))
            # list = list + list_temp
        except:
            print("something wrong userid : " + str(user_id))
            print("something wrong cursor : " + cursor)
            uri_page2 = init.uri_query3.format(user_id=user_id, cursor=cursor)
            print("something wrong cursor : " + str(uri_page2))
            return
            # print(len(list), list[0])


def getfirstxhr(browser, url, islogin):
    """
    :param browser: webdriver
    :param url: Target page
    :return: cursor for next page, Boolean for next page
    """
    if (islogin):
        bias = 1
    else:
        bias = 0
    browser.get(url)
    soup = Soup(browser.page_source, "lxml")
    xhr = soup.find_all(type='text/javascript')
    json_str = str(xhr[13 + bias])[52:-10]
    js_data = json.loads(json_str, encoding='utf-8')
    user = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
    user_name = user["username"]
    user_id = user["id"]
    user_fbid = user["fbid"]

    edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
    cursor = page_info['end_cursor']
    flag = page_info['has_next_page']

    list_temp = []
    edge = edges[0]
    for edge in edges:
        if edge['node']['display_url']:
            post = postClass.Post()

            display_url = edge['node']['display_url']

            post.username = edge['node']['owner']['username']
            post.id = edge['node']['owner']['id']
            # post.fbid = user_fbid
            post.url = display_url
            post.typename = edge['node']['__typename']
            post.is_video = edge['node']['is_video']
            if (len(edge['node']['edge_media_to_caption']['edges'])):
                post.edge_media_to_caption = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            # post.edge_media_to_caption = edge['node']['edge_media_to_caption']
            post.shortcode = edge['node']['shortcode']
            post.taken_at_timestamp = edge['node']['taken_at_timestamp']
            post.edge_media_preview_like = edge['node']['edge_media_preview_like']

            list_temp.append(post)
            print(display_url)

    print(cursor, flag)
    print(len(list_temp))

    return cursor, flag, user, list_temp


def getnextxhr(browser, cursor, user_id, database_name, username):
    """
    :param browser: webdriver
    :param cursor: cursor
    :param user_id: user_id
    :return:
    """
    list_tmp = []

    uri_page2 = init.uri_query3.format(user_id=user_id, cursor=cursor)
    # print(uri_page2)
    browser.get(uri_page2)
    soup = browser.page_source
    pre = "<html><head></head><body><pre style='word-wrap: break-word; white-space: pre-wrap;'>"
    len(pre.strip())
    ssss = str(soup)[84:-20]
    js_data = json.loads(ssss, encoding='utf-8')

    edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
    page_info = js_data["data"]["user"]["edge_owner_to_timeline_media"]['page_info']
    cursor = page_info['end_cursor']
    flag = page_info['has_next_page']
    edge = edges[1]
    for edge in edges:
        if edge['node']['display_url']:
            display_url = edge['node']['display_url']
            # print(display_url)    #預覽照片
            post = postClass.Post()

            post.username = edge['node']['owner']['username']
            post.id = edge['node']['owner']['id']
            # post.fbid = user_fbid
            post.url = display_url
            post.typename = edge['node']['__typename']
            post.is_video = edge['node']['is_video']
            # print(edge['node']['edge_media_to_caption']['edges'])  #內容
            len(edge['node']['edge_media_to_caption']['edges']) > 0
            if (len(edge['node']['edge_media_to_caption']['edges']) > 0):
                post.edge_media_to_caption = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            post.shortcode = edge['node']['shortcode']
            post.taken_at_timestamp = edge['node']['taken_at_timestamp']
            post.edge_media_preview_like = edge['node']['edge_media_preview_like']
            list_tmp.append(post)

    # database.main_getinfo(list_tmp, database_name, username)
    return cursor, flag, list_tmp


def refresh(browser, url, islogin, database_name, username):
    # 確認DB是否有該表
    database.check(database_name, username)
    is_new_post = False
    counter = 0
    (cursor, flag, user, list_temp) = getfirstxhr(browser, url, islogin)
    print(str(user["id"])+":"+username)
    # print(cursor)
    for i in list_temp:
        # try:
        shortcode = i.shortcode
        fetch_result = database.serchShortcode(database_name, username, shortcode)
        # print(shortcode)

        if (len(fetch_result) > 0):
            print("is Old post")
            return is_new_post
        else:
            print("is New post")
            is_new_post = True
            database.main_getinfo([i], database_name, username)
        # except:
        #     print("serchShortcode WRONG"+username+"+"+shortcode)

    while (flag):
        try:
            counter = counter + 1
            (cursor, flag, list_temp) = getnextxhr(browser, cursor, user["id"], database_name, username)
            # print(cursor, flag)
            # print("aleady save : " + str(12 * counter))

            for i in list_temp:
                try:
                    shortcode = i.shortcode
                    fetch_result = database.serchShortcode(database_name, username, shortcode)
                    if (len(fetch_result) > 0):
                        print("is Old post")
                        return is_new_post
                    else:
                        print("is New post")
                        is_new_post = True
                        database.main_getinfo([i], database_name, username)
                except:
                    print("serchShortcode WRONG"+username+"+"+shortcode)

        except:
            print("something wrong userid : " + user["id"])
            print("something wrong cursor : " + cursor)

            return is_new_post
