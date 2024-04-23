import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
username = 'please-add-your-username-here'
password = 'please-add-your-password-here'
auth = f'{username}:{password}'
host = 'please-add-your-host-here'
browser_url = f'wss://{auth}@{host}'

def link_from_text(company, location=None, ):
    """
    :param search_term: a string
    :return: the search term as a string for the Linkedin search api
    """
    company = company.replace(' ', '%20').replace('&', '%26').replace(',', '%2C')
    search_term = f'https://www.linkedin.com/jobs/search?keywords={company}'
    if location:
        location = location.replace(' ', '%20').replace('&', '%26').replace(',', '%2C')
        search_term += f'&{location}'
    return search_term
def is_locked(soup):
    """
    This function checks if the page is locked behind a login screen
    :param soup: linkedin page soup
    :return: True if the page is locked, False otherwise
    """
    header_exists = soup.find(class_='header__content__heading') is not None
    modal_exists = soup.find(class_='modal__overlay flex items-center bg-color-background-scrim justify-center fixed bottom-0 left-0 right-0 top-0 opacity-0 invisible pointer-events-none z-[1000] transition-[opacity] ease-[cubic-bezier(0.25,0.1,0.25,1.0)] duration-[0.17s] py-4 modal__overlay--visible') is not None
    return header_exists or modal_exists

def extract_job_titles_and_companies(soup):
    job_titles = []
    companies = []
    jobs = soup.find_all('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
    infos = soup.find_all('div', class_='base-search-card__info')
    for job, info in zip(jobs, infos):
        try:
            job_title = job.find('span', class_='sr-only').get_text(strip=True)
        except:
            job_title = 'not found'
        try:
            company = info.find('a', class_='hidden-nested-link').get_text(strip=True)
        except:
            company = 'not found'
        companies.append(company)
        job_titles.append(job_title)
    return companies, job_titles

def get_from_file(name):
    safe_name=name.replace('/','0').replace('|', '1')
    with open(f'../../data/htmls/linkedin_positions_at_{safe_name}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    try:
        search_term = soup.find('input', id="job-search-bar-keywords")['value']
        jobs_header = soup.find('div', class_='results-context-header')
        if jobs_header is None:
            return [search_term], [None], [search_term], [0]
        jobs_count = jobs_header.find('span', class_='results-context-header__job-count').get_text(strip=True)
    except:
        print("failed to get html for ", name)
        search_term = 'not found'
        jobs_count = 0
        return [name], [None],[name], [jobs_count]

    companies, job_titles= extract_job_titles_and_companies(soup)
    return companies, job_titles , [search_term]*len(companies), [jobs_count]*len(companies)

async def main(search_terms):
    async with async_playwright() as pw:
        print('connecting')
        browser = await pw.chromium.connect_over_cdp(browser_url)
        print('connected')
        page = await browser.new_page()
        print('goto')
        all_companies_=[]
        all_job_titles_=[]
        all_search_terms_=[]
        all_jobs_counts_=[]
        failed_terms=[]
        for i, search_term in enumerate(search_terms):
            print("searching for jobs at ", search_term)
            await page.goto(link_from_text(search_term), timeout=120000)
            try:
                html_content = await page.evaluate('()=>document.documentElement.outerHTML')
            except:
                print("failed to get html content for ", search_term)
                failed_terms.append(search_term)
                continue
            soup = BeautifulSoup(html_content, 'html.parser')
            if not is_locked(soup):
                safe_search_term = search_term.replace('/', '0').replace('|', '1')
                with open(f'../../data/htmls/linkedin_positions_at_{safe_search_term}.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                companies, job_titles = extract_job_titles_and_companies(soup)
                all_companies_+= companies
                all_job_titles_ += job_titles
                all_search_terms_ += [search_term]*len(companies)
            print("found ", len(companies), " jobs at ", search_term)
        await browser.close()

        # recursively get the failed terms until all are done
        if len(failed_terms)>0:
            companies_, job_titles_, search_terms_, jobs_counts_ = await main(failed_terms)
            all_companies_ += companies_
            all_job_titles_ += job_titles_
            all_search_terms_ += search_terms_
            all_jobs_counts_ += jobs_counts_
        return all_companies_, all_job_titles_, all_search_terms_, all_jobs_counts_


with open("../../data/companies_names_linkedin.txt",'r',encoding='utf-8') as f:
    companies = f.readlines()
companies = companies[:500]
companies = [company.strip() for company in companies]

files = os.listdir('../../data/htmls')
companies_with_file = [file[22:-5].replace('0','/').replace('1','|') for file in files]


companies_to_scrap = [company for company in companies if company not in companies_with_file]
companies_to_scrap.remove("Hemant Sharma 2.0 | Job & Career")
companies_to_scrap.remove("Viacom18 Media Private Limited")
print("companies: ", len(companies))
print("companies with file: ", len(companies_with_file))
print("companies to scrap: ", len(companies_to_scrap))

data = pd.DataFrame(columns=['company', 'job_title', 'search_term','jobs count'])
all_companies, all_job_titles, all_search_terms, all_jobs_counts = [], [], [], []
if len(companies_to_scrap)>0:
    all_companies, all_job_titles, all_search_terms, all_jobs_counts = asyncio.run(main(companies_to_scrap))


for company in companies_with_file:
    data = pd.DataFrame(columns=['company', 'job_title', 'search_term','jobs count'])
    print("reading ", company)
    companies_, job_titles_, search_terms_, jobs_counts_ = get_from_file(company)
    all_companies += companies_
    all_job_titles += job_titles_
    all_search_terms += search_terms_
    all_jobs_counts += jobs_counts_
data['company'] = all_companies
data['job_title'] = all_job_titles
data['search_term'] = all_search_terms
data['jobs count'] = all_jobs_counts
data.to_csv('../../data/open_positions_data.csv', index=False)