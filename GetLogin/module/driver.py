import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def inject_timer(browser, duration):
    # JavaScript to create and start the timer overlay
    js_script = f"""
    // Create overlay div
    var overlay = document.createElement('div');
    overlay.id = 'timer-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '10px';
    overlay.style.right = '10px';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    overlay.style.color = 'white';
    overlay.style.padding = '10px';
    overlay.style.borderRadius = '5px';
    overlay.style.fontSize = '16px';
    overlay.style.zIndex = '9999';
    document.body.appendChild(overlay);

    // Update timer every second
    var timer = {duration};
    var interval = setInterval(function() {{
        overlay.innerHTML = 'Time remaining: ' + timer + ' seconds';
        timer--;
        if (timer < 0) {{
            clearInterval(interval);
            overlay.innerHTML = 'Time is up!';
        }}
    }}, 1000);
    """
    browser.execute_script(js_script)

def driver(username, password, fill_password):
    # Create a new Chrome browser instance with options
    chop = webdriver.ChromeOptions()
    chop.add_argument("start-maximized")
    # Uncomment the next line if you want to run in headless mode
    # chop.add_argument("--headless")
    chop.add_argument("--no-sandbox")
    chop.add_argument("--disable-dev-shm-usage")

    # Use WebDriver Manager to automatically handle ChromeDriver
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chop)

    # Navigate to the given URL
    url = 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481'
    browser.get(url)

    wait = WebDriverWait(browser, 10)

    # Wait for any modal to appear and close it if it has a close button with class "---guide-close"
    try:
        modal_close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*=---guide-close]')))
        modal_close_button.click()
    except:
        pass

    # Wait for the "Sign In" button to be clickable
    signin_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
    signin_button.click()

    # Switch to iframe using its ID
    iframe = wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "hyv-account-frame"))
    )

    # Locate and interact with the username input
    username_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
    )
    username_input.send_keys(username)

    if fill_password.lower() == 'y':
        # Locate and interact with the password field
        password_field = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        password_field.send_keys(password)

        # Locate and click the login button
        login_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        login_button.click()

    browser.switch_to.default_content()

    # Inject overlay timer
    inject_timer(browser, 60)  # 60 seconds timer

    # Wait for user to login for a manual timer
    manual_timer = 60
    print(f"Waiting for {manual_timer} seconds for user login captcha...")
    for i in range(manual_timer, 0, -1):
        print(f"\r{i} seconds remaining...", end="")
        time.sleep(1)
    print("\n")

    # Check if the user has logged in
    checklogin = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mhy-hoyolab-account-block')))
    checklogin.click()
    time.sleep(5)

    # Saving state on select menu
    select_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mhy-hoyolab-account-block div.mhy-hoyolab-select-menu')))
    time.sleep(5)

    # Check if the style display is not "none"
    style_attribute = select_menu.get_attribute('style')
    if style_attribute and 'none' in style_attribute:
        print('Please Retry Login!')
        exit()

    # Get all cookies from hoyolab.com
    cookies = browser.get_cookies()
    # Filter cookies for domains 'hoyolab.com' or '.hoyoverse.com'
    hoyolab_cookies = [
        cookie for cookie in cookies if 'hoyolab.com' in cookie['domain'] or '.hoyoverse.com' in cookie['domain']
    ]

    # Print the extracted cookies
    print(hoyolab_cookies)

    # Close the browser instance
    browser.quit()

    return hoyolab_cookies