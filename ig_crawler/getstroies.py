import os

import database
import init
import json
import time
from selenium import webdriver

from bs4 import BeautifulSoup as Soup
import requests

import postClass


def main(browser, username, islogin):
    if (islogin != True):
        print("Not login")
        return

    url_pre = 'https://www.instagram.com/stories/'
    url_main = url_pre + username + '/'
    browser.get(url_main)
    sumbit(browser)
    pause(browser)

    file_loc_str = './stories/'
    file_loc_str = file_loc_str + username + "/"
    os.makedirs(file_loc_str, exist_ok=True)
    temp = 0
    while (True):
        temp = temp+1
        time.sleep(1)
        soup = Soup(browser.page_source, "lxml")
        try:
            # 影片
            print("TRY Video")
            xhr = soup.find_all("source")[0].attrs['src']
            print("Video!!!")
            media = requests.get(xhr)
            file_type = '.mp4'
            timestamp = soup.find_all("time", class_="BPyeS Nzb55")[0]['datetime']

            file_name = timestamp.split(".")[0]
            file_name = file_name.replace(':', '-')
            print("write file : " + file_loc_str + file_name + "_" + str(temp) + file_type)
            with open(file_loc_str + file_name + "_" + str(temp) + file_type, 'wb') as f:
                f.write(media.content)

            next(browser)
            # pause(browser)

        except:
            print("TRY IMAGE")
            # 相片
            # xhr = soup.find_all("div", class_="qbCDp")
            xhr = soup.find_all("img", class_="y-yJ5")
            if len(xhr) == 0:
                print("over")
                return
            json_str = xhr[0].attrs['srcset']
            strsp = json_str.split(" ")
            strsp[0]
            # json_str = xhr[0].attrs['src']
            print("Img!!!")
            media = requests.get(strsp[0])
            file_type = '.jpg'
            timestamp = soup.find_all("time", class_="BPyeS Nzb55")[0]['datetime']

            file_name = timestamp.split(".")[0]
            file_name = file_name.replace(':', '-')
            print("write file : " + file_loc_str + file_name + "_" + str(temp) + file_type)
            with open(file_loc_str + file_name + "_" + str(temp) + file_type, 'wb') as f:
                f.write(media.content)

            next(browser)
            # pause(browser)


def pause(browser):
    # btn_stop = soup.find_all("button", class_="wpO6b")
    browser.find_element_by_class_name("wpO6b").click()


def next(browser):
    # btn_next = soup.find_all("button", class_="FhutL")
    browser.find_element_by_class_name("FhutL").click()


def sumbit(browser):
    elem_submit = browser.find_element_by_class_name('sqdOP.L3NKy.y1rQx.cB_4K').click()
