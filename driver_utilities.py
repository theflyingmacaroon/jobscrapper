import time
import random

# Configuration, in order to make the script more stable and safe from being blocked by LinkedIn
USE_DELAYS = True  # Set to False to disable all timing delays
MIN_DELAY = 2  # Minimum delay in seconds
MAX_DELAY = 5  # Maximum delay in seconds
MIN_KEYSTROKE_DELAY = 0.1  # Minimum delay between keystrokes
MAX_KEYSTROKE_DELAY = 0.3  # Maximum delay between keystrokes


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

def random_sleep(min_seconds=MIN_DELAY, max_seconds=MAX_DELAY):
    if USE_DELAYS:
        time.sleep(random.uniform(min_seconds, max_seconds))