import datetime

import ig_crawler.database as database
# import init
import json
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
import requests
import lxml
# import postClass
import ig_crawler.userClass as userClass


def main(islogin, browser, url):
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

    user_index = userClass.user

    user_index.id = user["id"]
    user_index.username = user["username"]
    user_index.full_name = user["full_name"]
    user_index.fbid = user["fbid"]
    user_index.biography = user["biography"]
    user_index.edge_owner_to_timeline_media = user['edge_owner_to_timeline_media']['count']
    user_index.edge_followed_by = user['edge_followed_by']['count']
    user_index.edge_follow = user['edge_follow']['count']
    user_index.edge_mutual_followed_by = user['edge_mutual_followed_by']['count']
    user_index.external_url = user['external_url']
    user_index.country_block = user['country_block']
    user_index.has_ar_effects = user['has_ar_effects']
    user_index.has_clips = user['has_clips']
    user_index.has_guides = user['has_guides']
    user_index.has_channel = user['has_channel']
    user_index.highlight_reel_count = user['highlight_reel_count']
    user_index.hide_like_and_view_counts = user['hide_like_and_view_counts']
    user_index.is_business_account = user['is_business_account']
    user_index.is_professional_account = user['is_professional_account']
    user_index.is_joined_recently = user['is_joined_recently']
    user_index.business_address_json = user['business_address_json']
    user_index.business_contact_method = user['business_contact_method']
    user_index.business_email = user['business_email']
    user_index.business_phone_number = user['business_phone_number']
    user_index.business_category_name = user['business_category_name']
    user_index.overall_category_name = user['overall_category_name']
    user_index.category_enum = user['category_enum']
    user_index.category_name = user['category_name']
    user_index.is_private = user['is_private']
    user_index.is_verified = user['is_verified']
    user_index.should_show_category = user['should_show_category']
    user_index.should_show_public_contacts = user['should_show_public_contacts']
    user_index.connected_fb_page = user['connected_fb_page']
    user_index.pronouns = user['pronouns']
    user_index.deployment_stage = js_data['deployment_stage']
    user_index.mid_pct = js_data['mid_pct']
    user_index.seo_category_infos = str(js_data['entry_data']['ProfilePage'][0]['seo_category_infos'])

    db_name = "Instagram.db"

    # database.main_getindex(user_index, db_name)
    return user_index