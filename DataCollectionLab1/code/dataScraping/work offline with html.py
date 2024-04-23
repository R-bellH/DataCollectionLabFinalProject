from bs4 import BeautifulSoup
import requests
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
def extract_job_titles(soup):
    # Find all 'a' tags with the specified class
    a_tags = soup.find_all('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')

    # For each 'a' tag, find the 'span' tag with class 'sr-only' and get its text
    job_titles = [a.find('span', class_='sr-only').get_text(strip=True) for a in a_tags]

    return job_titles
def check_if_anon(soup):
    # Check if the class 'header__content__heading' exists
    header_exists = soup.find(class_='header__content__heading') is not None

    # Check if the class 'modal__overlay flex items-center bg-color-background-scrim justify-center fixed bottom-0 left-0 right-0 top-0 opacity-0 invisible pointer-events-none z-[1000] transition-[opacity] ease-[cubic-bezier(0.25,0.1,0.25,1.0)] duration-[0.17s] py-4 modal__overlay--visible' exists
    modal_exists = soup.find(class_='modal__overlay flex items-center bg-color-background-scrim justify-center fixed bottom-0 left-0 right-0 top-0 opacity-0 invisible pointer-events-none z-[1000] transition-[opacity] ease-[cubic-bezier(0.25,0.1,0.25,1.0)] duration-[0.17s] py-4 modal__overlay--visible') is not None

    # Return True if either class exists, False otherwise
    return header_exists or modal_exists
def extract_job_titles_and_companies(soup):
    # Find all 'a' tags with the specified class
    a_tags = soup.find_all('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')

    # Initialize lists to store job titles and companies
    job_titles = []
    companies = []

    # For each 'a' tag, find the 'span' tag with class 'sr-only' and get its text
    # Also find the 'a' tag with class 'hidden-nested-link' and get its text
    for a in a_tags:
        job_title = a.find('span', class_='sr-only').get_text(strip=True)
        company = a.find('a', class_='hidden-nested-link').get_text(strip=True)
        companies.append(company)
        job_titles.append(job_title)

    return companies, job_titles
# company='taboola'
# company='spaceX'
company='Red bull'

# with open(f'linkedin_positions_at_{company}.html', 'r', encoding='utf-8') as f:
with open(f'htmls\linkedin_positions_at_{company}.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, 'html.parser')
if check_if_anon(soup):
    print('Anon')
print(extract_job_titles(soup))