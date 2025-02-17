﻿# **GenshinDailyLoginV3**

A Python-based automation script for daily login activities in Genshin Impact using Selenium and MongoDB. This project is organized into two modules:

1. **AutoDaily**: Handles daily login automation using cookies.
2. **GetLogin**: Manages login credentials and cookies retrieval.

---

## **Directory Structure**
```
GenshinDailyLoginV3/
│
├── AutoDaily/
│   ├── env/                 # Virtual environment for AutoDaily
│   ├── main.py              # Main script for daily login automation
│   ├── requirements.txt     # Dependencies for AutoDaily
│   ├── .env.example         # Environment variable template for AutoDaily
│
├── GetLogin/
│   ├── env/                 # Virtual environment for GetLogin
│   ├── module/              # Helper modules for login handling
│   │   ├── authy.py         # Authentication-related functions
│   │   ├── driver.py        # Selenium WebDriver setup and usage
│   ├── main.py              # Main script for login and cookie management
│   ├── requirements.txt     # Dependencies for GetLogin
│   ├── .env.example         # Environment variable template for GetLogin
│
├── .gitignore               # Git ignore file
└── README.md                # Project documentation
```

---

## **Dependencies**

This project relies on the following key dependencies:

### **1. Python Libraries**
Make sure the following Python packages are installed:

- **`selenium`**: Used for automating browser interactions.
  ```bash
  pip install selenium
  ```
- **`webdriver_manager`**: Automatically downloads and manages the appropriate WebDriver for Selenium.
  ```bash
  pip install webdriver_manager
  ```
- **`pymongo`**: Provides a Python interface to MongoDB for saving and retrieving login cookies.
  ```bash
  pip install pymongo
  ```
- **`python-dotenv`**: Enables the use of `.env` files to manage environment variables.
  ```bash
  pip install python-dotenv
  ```

### **2. Additional Requirements**
- **MongoDB**: A NoSQL database used to store user cookies and account data.
  - Install MongoDB Community Edition:
    - [MongoDB Installation Guide](https://www.mongodb.com/docs/manual/installation/)
  - Start the MongoDB server before running the scripts.

- **Google Chrome**: Required for browser automation with Selenium.
  - Install Chrome: [Google Chrome Download](https://www.google.com/chrome/)
  - Make sure the Chrome version matches the WebDriver version managed by `webdriver_manager`.

---

## **Installing Dependencies**

### **Method 1: Using `requirements.txt`**
Each module has its own `requirements.txt` file. Install the dependencies by running:

#### For AutoDaily:
```bash
cd AutoDaily
pip install -r requirements.txt
```

#### For GetLogin:
```bash
cd ../GetLogin
pip install -r requirements.txt
```

### **Method 2: Manual Installation**
If you encounter issues with the `requirements.txt` file, install the dependencies manually:

```bash
pip install selenium
pip install webdriver_manager
pip install pymongo
pip install python-dotenv
```

---

## **Setting Up Environment Variables**

1. Copy the `.env.example` file to `.env` in both `AutoDaily` and `GetLogin` directories:
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and configure the following variables:
   - `MONGO_CLIENT_LINK`: Your MongoDB connection string.
   - `MONGO_CLIENT_DB`: The name of the database.
   - `MONGO_CLIENT_COLLECTION`: The name of the collection for user cookies.
   - `MONGO_CLIENT_LOG_COLLECTION`: The name of the collection for logging.
   - `HEADLESS`: Set to `false` to run the browser in headful mode (visible) during automation.
   - `MIN_SLEEP_TIME`: The minimum sleep time (in seconds) between login attempts.
   - `MAX_SLEEP_TIME`: The maximum sleep time (in seconds) between login attempts.
---

## **Quick Test for Dependencies**

Run the following command to verify if all dependencies are installed:
```bash
python -m pip freeze | grep -E "selenium|webdriver_manager|pymongo|python-dotenv"
```

If any dependency is missing, install it as shown in the **Dependencies** section above.

---

## **How It Works**

### **1. GetLogin Module**
Please note that this module currently cannot bypass the captcha. You will need to manually solve the captcha. Once completed, you can press the timer button to expedite the process.
The `GetLogin` module handles the retrieval and management of login credentials and cookies. Here's how it works:

1. **Manual Login**: The user manually logs into their Genshin Impact account through the automated browser.
2. **Retrieve Cookies**: After a successful login, the script retrieves the cookies from the browser.
3. **Save Cookies**: The retrieved cookies are saved to MongoDB for future use by the `AutoDaily` module.

### **2. AutoDaily Module**
This module was last tested on January 7, 2025. If there are any changes to the website, the module may not work as expected. Updates will be provided as necessary.
To ensure the script runs daily without manual intervention, it is recommended to set up a cron job (Linux) or Task Scheduler (Windows). This allows the `AutoDaily` module to execute at a specified time each day, maintaining consistent login activity.

The `AutoDaily` module is responsible for automating the daily login process. Here's a step-by-step overview of how it works:

1. **Login Automation**: The script navigates to the Genshin Impact login page and performs the login using stored cookies.
2. **Daily Sign-In Actions**: Selenium will automatically navigate through the necessary steps, including clicking on the guide, accepting cookies, performing the daily sign-in, and confirming the action.
3. **Logging**: Logs the login activity and any errors encountered during the process.

---
