import pandas as pd
import os

def save_to_excel(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_excel(filename, index=False)
    print(f"Jobs saved to {filename}")


def create_env_file():
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('LINKEDIN_EMAIL=your_email@example.com\n')
            f.write('LINKEDIN_PASSWORD=your_password\n')
        print("Please update the .env file with your LinkedIn credentials")
        return True
    return False
