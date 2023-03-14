from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE

import time
import json
import pymongo
import os
from dotenv import load_dotenv

# Get Data From MongoDB
load_dotenv()
mongo_client_link = os.getenv('MONGO_CLIENT_LINK')
mongo_client_db = os.getenv('MONGO_CLIENT_DB')
mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
mongo_client_log_collection = os.getenv('MONGO_CLIENT_LOG_COLLECTION')
mongo_client = pymongo.MongoClient(mongo_client_link)

# Select the database and collection
if mongo_client_db in mongo_client.list_database_names():
    db = mongo_client[mongo_client_db]
    print("The database exists.")
else:
    print("The database doesn't exists.")
    exit()
    
if mongo_client_collection in db.list_collection_names():
    collection = db[mongo_client_collection]
    print("The collection exists.")
else:
    print("The collection doesn't exists.")
    exit()
    
if mongo_client_log_collection in db.list_collection_names():
    log_collection = db[mongo_client_log_collection]
    print("The log collection exists.")
else:
    print("The log collection doesn't exists.")
    exit()

# Find all documents in the collection
LoginDocuments = collection.find()

# Print the documents
for Login in LoginDocuments:
    cookies = Login['cookies']
    cookies.sort(key=lambda x: x["domain"], reverse=True)

    chop = webdriver.ChromeOptions()
    chop.add_argument("start-maximized")
    # chop.add_argument("headless")
    s=Service(r"./chromedriver/chromedriver.exe")
    browser = webdriver.Chrome(options=chop, service=s)

    ## Login 1
    url = "https://hoyolab.com/"
    browser.get(url)
    for cookie in cookies:
        if cookie['domain'][1:] == 'hoyolab.com':
            browser.add_cookie({'domain': cookie['domain'][1:], 'expiry': cookie['expiry'], 'httpOnly': cookie['httpOnly'], 'name': cookie['name'], 'path': cookie['path'], 'secure': cookie['secure'], 'value': cookie['value']})
    browser.refresh()
    time.sleep(3)

    ## Login 2 + Daily Page
    url = "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481"
    browser.get(url)
    for cookie in cookies:
        if cookie['domain'][1:] == 'act.hoyolab.com':
            browser.add_cookie({'domain': cookie['domain'][1:], 'expiry': cookie['expiry'], 'httpOnly': cookie['httpOnly'], 'name': cookie['name'], 'path': cookie['path'], 'secure': cookie['secure'], 'value': cookie['value']})
    browser.refresh()
    
    print(f"Waiting for 10 seconds before clicking daily check-in content ...")
    for i in range(10, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")

    ## Do Click for Daily
    wait = WebDriverWait(browser, 10)
    
    modal_close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*=---guide-close]')))
    modal_close_button.click()
    
    click_daily_sign_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.start.components-home-assets-__sign-content_---sign-wrapper")))
    click_daily_sign_button.click()
    
    time.sleep(3)
    # Access GenshinTest database
    hoyolab_db = mongo_client[mongo_client_db]
    users_collection = hoyolab_db[mongo_client_collection]
    try:
        checker_modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*=---dialog-close]')))
        checker_modal_close_button.click()
        print("Click successful!")
    except TE:
        print("Click unsuccessful.")
            
    browser.deleteAllCookies()
    browser.quit()
    
    print(f"Waiting for 10 seconds before clicking going to next account ...")
    for i in range(10, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")
    
print("All Account Clear")