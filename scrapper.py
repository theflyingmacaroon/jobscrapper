from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import random
from dotenv import load_dotenv

# Configuration, in order to make the script more stable and safe from being blocked by LinkedIn
USE_DELAYS = True  # Set to False to disable all timing delays
MIN_DELAY = 2  # Minimum delay in seconds
MAX_DELAY = 5  # Maximum delay in seconds
MIN_KEYSTROKE_DELAY = 0.1  # Minimum delay between keystrokes
MAX_KEYSTROKE_DELAY = 0.3  # Maximum delay between keystrokes


def random_sleep(min_seconds=MIN_DELAY, max_seconds=MAX_DELAY):
    """Sleep for a random amount of time between min and max seconds if delays are enabled."""
    if USE_DELAYS:
        time.sleep(random.uniform(min_seconds, max_seconds))

def setup_driver():
    """Initialize and return a configured Chrome WebDriver."""
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment to run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    return webdriver.Chrome( options=chrome_options)

def login(driver, email, password):
    """Log in to LinkedIn using provided credentials."""
    try:
        driver.get('https://www.linkedin.com/login')
        random_sleep(3, 5) 
        
        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        for char in email:
            email_field.send_keys(char)
            if USE_DELAYS:
                time.sleep(random.uniform(MIN_KEYSTROKE_DELAY, MAX_KEYSTROKE_DELAY))
        
        random_sleep(1, 2)
        
        # Enter password
        password_field = driver.find_element(By.ID, 'password')
        for char in password:
            password_field.send_keys(char)
            if USE_DELAYS:
                time.sleep(random.uniform(MIN_KEYSTROKE_DELAY, MAX_KEYSTROKE_DELAY))
        
        random_sleep(1, 2) 
        
        # Click login button
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Wait for login to complete with a longer random delay
        random_sleep(15, 15)
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

def driver_scroll(driver):
            # Scroll the jobs container slowly to detect all the jobs
            time.sleep(3)
            driver.execute_script("""
                const jobsContainer = document.querySelector(".mIELPyQEFIFgeLLNERTXgOZnKCPOmvto");
                if (jobsContainer) {
                    const scrollHeight = jobsContainer.scrollHeight;
                    let currentPosition = 0;
                    const scrollStep = 100; // Scroll 100px at a time
                    const scrollInterval = 100; // Wait 100ms between scrolls
                    
                    function scroll() {
                        if (currentPosition < scrollHeight) {
                            jobsContainer.scrollTo(0, currentPosition);
                            currentPosition += scrollStep;
                            setTimeout(scroll, scrollInterval);
                        }
                    }
                    
                    scroll();
                }
            """)
            random_sleep(3, 4)

def search_jobs(driver, keyword, location, num_pages):
    jobs = []
    try:
        # Navigate to jobs page
        driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}')
        random_sleep(4, 6) 
        
        driver_scroll(driver)

        for page in range(num_pages):
            print(f"Processing page {page + 1} of {num_pages}")
            
            # Get job cards
            job_cards = driver.find_elements(By.CLASS_NAME, 'flex-grow-1')
            print(f"Found {len(job_cards)} jobs on page {page + 1}")
             
            for card in job_cards:
                try:
                    # Extract job details
                    title = card.find_element(By.CSS_SELECTOR, '.job-card-job-posting-card-wrapper__title strong').text
                    company = card.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle div[dir="ltr"]').text
                    location = card.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__caption div[dir="ltr"]').text

                    # Extract description and job type
                    card.click()
                    random_sleep(1, 2)
                    description = driver.find_element(By.CSS_SELECTOR, '.jobs-box__html-content .mt4 p').text
                    job_type = driver.find_element(By.CSS_SELECTOR, '.ui-label--accent-3 span[aria-hidden="true"]').text
                    job_level = driver.find_element(By.CSS_SELECTOR, '.job-details-jobs-unified-top-card__job-insight-view-model-secondary').text

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'description': description,
                        'job_type': job_type,
                        'job_level': job_level,
                    })
                except Exception as e:
                    print(f"Warning: Error extracting job details from card: {str(e)}")
                    continue
            
            # Click next page if not on last page
            if page < num_pages - 1:
                try:
                    random_sleep(2, 3)  
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button.jobs-search-pagination__button--next')
                    next_button.click()
                    random_sleep(3, 4)  
                except Exception as e:
                    print(f"Warning: Error navigating to next page: {str(e)}")
                    break  

        return jobs
    except Exception as e:
        print(f"Warning: Error in main search function: {str(e)}")
        return jobs  

def save_to_csv(jobs, filename='linkedin_jobs.csv'):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Jobs saved to {filename}")

    # Main function to scrape LinkedIn jobs.
    # Args:
    #     keyword (str): The job title or keywords to search for
    #     location (str): The location to search jobs in
    #     num_pages (int): Number of pages to scrape
    # 
    # Load environment variables
def scrape_linkedin_jobs(keyword: str, location: str, num_pages: int) -> None:
    load_dotenv()
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return
    
    # Setup and initialize driver
    driver = setup_driver()
    
    try:
        if login(driver, email, password):
            jobs = search_jobs(driver, keyword, location, num_pages)
            
            if jobs:
                save_to_csv(jobs)
                print(f"Found {len(jobs)} jobs")
            else:
                print("No jobs found")
        else:
            print("Failed to login to LinkedIn")
    finally:
        driver.quit()

def create_env_file():
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('LINKEDIN_EMAIL=your_email@example.com\n')
            f.write('LINKEDIN_PASSWORD=your_password\n')
        print("Please update the .env file with your LinkedIn credentials")
        return True
    return False
