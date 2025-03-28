import time
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import driver_utilities as du

# Configuration, in order to make the script more stable and safe from being blocked by LinkedIn
USE_DELAYS = True  # Set to False to disable all timing delays
MIN_KEYSTROKE_DELAY = 0.1  # Minimum delay between keystrokes
MAX_KEYSTROKE_DELAY = 0.3

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    return webdriver.Chrome( options=chrome_options)

def login(driver, email, password):
    try:
        driver.get('https://www.linkedin.com/login')
        du.random_sleep(3, 5) 
        
        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        for char in email:
            email_field.send_keys(char)
            if USE_DELAYS:
                time.sleep(random.uniform(MIN_KEYSTROKE_DELAY, MAX_KEYSTROKE_DELAY))
        
        du.random_sleep(1, 2)
        
        # Enter password
        password_field = driver.find_element(By.ID, 'password')
        for char in password:
            password_field.send_keys(char)
            if USE_DELAYS:
                time.sleep(random.uniform(MIN_KEYSTROKE_DELAY, MAX_KEYSTROKE_DELAY))
        
        du.random_sleep(1, 2) 
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Wait for login to complete with a longer random delay
        du.random_sleep(15, 15)
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False
