import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_data(url, max_scrolls=30, scroll_delay=5):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    jobs_data = []
    scrolls = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_job_listings = soup.find_all('div', class_='job-list-job')  # Use the appropriate class here

        for job_listing in all_job_listings:
            title_element = job_listing.find('a', href=True)
            location_element = job_listing.find('span', class_='job-list-company-meta-item job-list-company-meta-locations')
            
            job_title = title_element.get_text(strip=True) if title_element else 'Title Not Found'
            job_url = title_element['href'] if title_element else 'URL Not Found'
            job_location = location_element.get_text(strip=True) if location_element else 'Location Not Found'

            job_data = {
                "title": job_title,
                "url": job_url,
                "location": job_location
            }
            jobs_data.append(job_data)

        scrolls += 1
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return jobs_data


if __name__ == "__main__":
    url = 'https://consider.com/boards/vc/consider/jobs?locations=United+States&skills=Machine+Learning'
    data = scrape_data(url)

    # CSV file saving
csv_file = "job_listings.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'url', 'location'])  # Include 'location'
    writer.writeheader()
    for job in data:
        writer.writerow(job)

print(f"Data saved to {csv_file}")