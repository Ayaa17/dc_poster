# import json
import os
import time

from selenium import webdriver
from ig_crawler import downloadpost
from ig_crawler import getinfo
from ig_crawler import init
from ig_crawler import database


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
        self._browser.get(init.url_main)
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
        self._url_Target = init.url_main + username + "/"
        return self

    def geturl(self):
        url = init.url_main + self._username + "/"
        self._browser.get(url)
        print(self._username)

    def refresh(self):
        url = init.url_main + self._username + "/"
        is_new = getinfo.refresh(self._browser, url, self.islogin, self._database_name, self._username)
        print("是否有新Post :"+str(is_new))
        # print("refresh")
        return is_new

    def downlaod(self):
        print(self._username + "get Post...", end="")
        downloadpost.main(self.islogin, self._browser, self._database_name, self._username)
        print("OVER!!")
        return

    def getNew(self):
        newPostShortcode=database.serchNew(self._database_name,self._username)
        return newPostShortcode
    def getDescription(self,shortcode):
        print(self._database_name,self._username)
        description = database.serchDescription(self._database_name,self._username,shortcode)
        return description

    def sendNew(self):
        newPostShortcode=database.serchNew(self._database_name,self._username)
        print(len(newPostShortcode))
        for i in newPostShortcode:
            database.updateSendDB(i[0],self._database_name,self._username)
        return newPostShortcode

    def sendNewPost(self,username):
        # file_dir_pre = ".\\media\\{username}\\"
        file_dir_pre = init.file_dir
        file_dir = file_dir_pre.format(username=username)
        is_new = self.setusername(username).refresh()
        # print(str(is_new))
        all_pic_loc = []
        if (is_new):
            self.downlaod()
            code_new = self.sendNew()
            for i in code_new:
                # print(i[0])
                fileExt = i[0]
                for j in os.listdir(file_dir):
                    if (j.find(fileExt) != -1):
                        # print(j)
                        # send
                        pic_loc = file_dir + j
                        all_pic_loc.append(pic_loc)
        return all_pic_loc