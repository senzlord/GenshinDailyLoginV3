from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime 
from getpass import getpass

import time
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
mongo_client_link = os.getenv('MONGO_CLIENT_LINK')
mongo_client_db = os.getenv('MONGO_CLIENT_DB')
mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
mongo_client = pymongo.MongoClient(mongo_client_link)
# print(mongo_client.server_info())

manual_timer = 80

# prompt user for their username
username = input("Please enter your username: ")
# Ask user if they want to fill in the password field
fill_password = input("Do you want to fill in the password field? (y/n): ")
if fill_password.lower() == 'y':
    show_password = input("Do you want to hide the password while type? (y/n): ")
    if show_password.lower() == 'y':
        password = getpass(prompt="Enter your password: ")
    else:
        password = input("Enter your password: ")
    

# create a new Chrome browser instance
chop = webdriver.ChromeOptions()
chop.add_argument("start-maximized")
# chop.add_argument("headless")
s = Service(r"./chromedriver/chromedriver.exe")
browser = webdriver.Chrome(options=chop, service=s)

# navigate to the given URL
url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
browser.get(url)

wait = WebDriverWait(browser, 10)
# wait for any modal to appear and close it if it has a close button with class "---guide-close"
try:
    modal_close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*=---guide-close]')))
    modal_close_button.click()
except:
    pass

# wait for the "Sign In" button to be clickable
signin_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
# click on the "Sign In" button to open the login page
signin_button.click()

# fill the input field with the username
username_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-account-flow-form-input.input-item:nth-of-type(1) input')))
username_input.send_keys(username)
if fill_password.lower() == 'y':
    password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-account-flow-form-input.input-item:nth-of-type(2) input')))
    password_field.send_keys(password)
    
    # wait 3 seconds before click login
    time.sleep(3)
    login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mhy-login-button button.login-btn')))
    login_button.click()
    
    manual_timer = 60


# wait for user to login for some seconds
print(f"Waiting for \r{manual_timer} seconds for user login captcha...")
for i in range(manual_timer, 0, -1):
    print(f"\r{i} seconds remaining...", end="")
    time.sleep(1)
print("\n")

# check login or not
checklogin = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
checklogin.click()
time.sleep(5)
# saving state on select menu
select_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mhy-hoyolab-account-block div.mhy-hoyolab-select-menu')))
time.sleep(5)
# Check if the style display is not none
# if select_menu.value_of_css_property('display') == 'none':
#     print('Please Retry Login!')
#     exit()

style_attribute = select_menu.get_attribute('style')
if style_attribute:
    print('Please Retry Login!')
    exit()

# get all cookies from hoyolab.com
cookies = browser.get_cookies()
hoyolab_cookies = [cookie for cookie in cookies if 'hoyolab.com' in cookie['domain']]

# print the extracted cookies
print(hoyolab_cookies)

# close the browser instance
browser.quit()

# Access GenshinTest database
hoyolab_db = mongo_client[mongo_client_db]
users_collection = hoyolab_db[mongo_client_collection]

# check if user with entered username already exists in the database
existing_user = users_collection.find_one({"username": username})
timestamp = datetime.now()
if existing_user:
    # update the existing user's cookies
    users_collection.update_one({"_id": existing_user["_id"]}, {"$set": {"cookies": hoyolab_cookies, 'timestamp': timestamp}})
    print(f"User {username}'s cookies updated in MongoDB")
else:
    # insert a new user with the entered username and extracted cookies
    user_data = {"username": username, "cookies": hoyolab_cookies, 'timestamp': timestamp}
    users_collection.insert_one(user_data)
    print(f"New user {username} and cookies saved to MongoDB")


