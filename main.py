from scrapper import scrape_linkedin_jobs, create_env_file

def main():
    if create_env_file():
        return
    
    scrape_linkedin_jobs(
        keyword='job',
        location='country',
        num_pages=14
    )

if __name__ == "__main__":
    main() 