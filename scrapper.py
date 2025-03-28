from selenium.webdriver.common.by import By
import os
import utilities as u
import driver_utilities as du
from dotenv import load_dotenv
import driver_services as ds

u.create_env_file()

def search_jobs(driver, keyword, location, num_pages):
    jobs = []
    try:
        # Navigate to jobs page
        driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}')
        du.random_sleep(4, 6) 
        du.driver_scroll(driver)

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
                    du.random_sleep(1, 2)
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
                    du.random_sleep(2, 3)  
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button.jobs-search-pagination__button--next')
                    next_button.click()
                    du.random_sleep(3, 4)  
                except Exception as e:
                    print(f"Warning: Error navigating to next page: {str(e)}")
                    break  

        return jobs
    except Exception as e:
        print(f"Warning: Error in main search function: {str(e)}")
        return jobs  


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
    driver = ds.setup_driver()
    
    try:
        if ds.login(driver, email, password):
            jobs = search_jobs(driver, keyword, location, num_pages)
            
            if jobs:
                u.save_to_excel(jobs, 'jobs.xlsx')
                print(f"Found {len(jobs)} jobs")
            else:
                print("No jobs found")
        else:
            print("Failed to login to LinkedIn")
    finally:
        driver.quit()

