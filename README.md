# **GenshinDailyLoginV3**

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

## **Requirements**
- **MongoDB**: Used for saving and retrieving login cookies.
- **Python**: Ensure Python is installed and aliased as `py` on your system.

---

## **Setup Instructions**

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd GenshinDailyLoginV3
```

### **Step 2: Set Up Virtual Environments**

#### For **AutoDaily**:
1. Navigate to the `AutoDaily` directory:
   ```bash
   cd AutoDaily
   ```
2. Create a virtual environment:
   ```bash
   py -m venv env
   ```
3. Activate the virtual environment:
   - **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **Linux**:
     ```bash
     source env/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### For **GetLogin**:
1. Navigate to the `GetLogin` directory:
   ```bash
   cd ../GetLogin
   ```
2. Repeat steps 2–4 as above.

---

## **Environment Variables**

1. Copy the `.env.example` file to `.env` in both `AutoDaily` and `GetLogin` directories.
2. Update the `.env` files with your MongoDB connection details and other required configurations.

---

## **Usage**

### **1. Running GetLogin**
To retrieve cookies and manage login credentials:
```bash
cd GetLogin
py main.py
```

### **2. Running AutoDaily**
To automate the daily check-in:
```bash
cd AutoDaily
py main.py
```

---

## **Tested Operating Systems**
- **Linux**: Ubuntu 20.04
- **Windows**: Windows 10, Windows 11

---
