from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
from webdriver_manager.chrome import ChromeDriverManager

import time
import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime
import random

def log_with_time(message):
    """Log a message with a timestamp."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def initialize_mongo():
    """Initialize MongoDB connection and collections."""
    load_dotenv()
    mongo_client = pymongo.MongoClient(os.getenv('MONGO_CLIENT_LINK'))

    # Select database
    db_name = os.getenv('MONGO_CLIENT_DB')
    if db_name not in mongo_client.list_database_names():
        log_with_time("The database doesn't exist.")
        exit()

    db = mongo_client[db_name]
    log_with_time("The database exists.")

    # Select main collection
    collection_name = os.getenv('MONGO_CLIENT_COLLECTION')
    if collection_name not in db.list_collection_names():
        log_with_time("The collection doesn't exist.")
        exit()

    collection = db[collection_name]
    log_with_time("The collection exists.")

    # Check or create log collection
    log_collection_name = os.getenv('MONGO_CLIENT_LOG_COLLECTION')
    if log_collection_name not in db.list_collection_names():
        log_with_time("The log collection doesn't exist. Creating it now.")
        log_collection = db[log_collection_name]
        log_collection.insert_one({"message": "Initializing log collection"})
        log_with_time("Log collection created and initialized.")
    else:
        log_collection = db[log_collection_name]
        log_with_time("The log collection exists.")

    return collection, log_collection

def initialize_browser():
    """Initialize Selenium WebDriver with options."""
    chop = webdriver.ChromeOptions()
    if os.getenv('HEADLESS') == 'true':
        chop.add_argument("--headless")
    else:
        chop.add_argument("start-maximized")
    chop.add_argument("--no-sandbox")
    chop.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)

def add_cookies_to_browser(browser, cookies, target_domains):
    """Add cookies to the browser for specified target domains."""
    for cookie in cookies:
        if any(domain in cookie['domain'] for domain in target_domains):
            log_with_time(f"Adding cookie for domain: {cookie['domain']}")
            dynamic_cookie = {key: cookie[key] for key in cookie if key != 'domain'}
            dynamic_cookie['domain'] = cookie['domain']
            browser.add_cookie(dynamic_cookie)

def click_close_button_if_exists(browser, wait):
    """Click the close button if it exists."""
    try:
        close_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.components-home-assets-__sign-guide_---guide-close---2VvmzE"))
        )
        close_button.click()
        log_with_time("Close button clicked successfully.")
        return True
    except TE:
        log_with_time("Close button not found.")
        return False

def handle_cookie_consent(browser, wait):
    """Handle the cookie consent banner if it appears."""
    try:
        # Wait for the cookie banner to appear
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mihoyo-cookie-tips__button"))
        )
        cookie_button.click()
        log_with_time("Cookie consent banner dismissed successfully.")
    except TE:
        log_with_time("Cookie consent banner not found or already dismissed.")

def perform_check_in(browser, wait, username, log_collection):
    """Perform daily check-in and handle modal popups."""
    try:
        time.sleep(10)

        # Close guide modal if it exists
        click_close_button_if_exists(browser, wait)

        # Handle cookie consent banner
        handle_cookie_consent(browser, wait)

        # Click daily check-in button
        check_in_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='components-home-assets-__sign-content-test_---sign-wrapper---']"))
        )
        check_in_button.click()
        time.sleep(3)

        # Close the confirmation modal
        modal_close_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*=---dialog-close]'))
        )
        modal_close_button.click()

        # Log success
        log_collection.insert_one({"username": username, "timestamp": datetime.now()})
        log_with_time(f"{username} Check-in successful!")
        return True

    except TE:
        log_with_time(f"{username} Check-in unsuccessful! or Already Check-in!")
        return False

def main():
    """Main function to process accounts for daily check-in."""
    collection, log_collection = initialize_mongo()
    accounts = collection.find()

    # Random sleep before starting
    sleep_time = random.randint(int(os.getenv('MIN_SLEEP_TIME', '300')), int(os.getenv('MAX_SLEEP_TIME', '600')))
    log_with_time(f"Sleeping for {sleep_time // 60} minutes and {sleep_time % 60} seconds before starting...")
    time.sleep(sleep_time)

    for account in accounts:
        username = account['username']
        cookies = account['cookies']
        cookies.sort(key=lambda x: x["domain"], reverse=True)

        # Initialize browser
        browser = initialize_browser()
        wait = WebDriverWait(browser, 10)

        # Navigate to daily check-in page
        url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
        browser.get(url)

        # Add cookies
        target_domains = ['.hoyolab.com', '.hoyoverse.com']
        add_cookies_to_browser(browser, cookies, target_domains)
        browser.refresh()

        # Perform check-in
        perform_check_in(browser, wait, username, log_collection)

        # Clean up
        browser.delete_all_cookies()
        browser.quit()

        # Wait before next account
        log_with_time("Waiting for 10 seconds before switching to the next account...")
        time.sleep(10)

    log_with_time("All accounts processed.")

if __name__ == "__main__":
    main()
