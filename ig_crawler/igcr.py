# import json
# import os
# import sqlite3
import time

from selenium import webdriver

from bs4 import BeautifulSoup as Soup
# import requests
# import ig_crawler.database
# import downloadpost
# import getindex
import ig_crawler.getinfo as getinfo
# import getstroies
import ig_crawler.init


class Singleton(object):
    _browser = webdriver.Chrome()
    _islogin = False
    _database_name = 'Instagram_forbot.db'
    _username = '''uf0123'''
    _url_Target = None
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.login(Singleton())
        return cls.instance

    def __init__(self):
        pass

    def login(self):
        self._browser.get(ig_crawler.init.url_main)
        print("Enter account: ")
        account = input()
        print("Enter password:　")
        password = input()
        elem_user = self._browser.find_element_by_name("username").send_keys(account)
        elem_password = self._browser.find_element_by_name("password").send_keys(password)
        elem_submit = self._browser.find_element_by_class_name('sqdOP.L3NKy.y3zKF').click()
        self.islogin = True
        time.sleep(10)

    def setusername(self, username):
        self._username = username
        return self

    def geturl(self):
        url = ig_crawler.init.url_main + self._username + "/"
        self._browser.get(url)
        print(self._username)

    def refresh(self):
        url = ig_crawler.init.url_main + self._username + "/"
        getinfo.refresh(self._browser, url, self.islogin, self._database_name, self._username)

        print("refresh")
