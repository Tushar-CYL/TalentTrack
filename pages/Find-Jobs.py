import time
import numpy as np
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings('ignore')


# --- Streamlit Config Setup ---
def streamlit_config():
    st.set_page_config(page_title='Resume Analyzer AI', layout="wide")
    st.markdown('<style>[data-testid="stHeader"] {background: rgba(0,0,0,0);}</style>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align: center;">Resume Analyzer AI</h1>', unsafe_allow_html=True)


# --- LinkedIn Scraper Class ---
class LinkedinScraper:

    def webdriver_setup():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    @staticmethod
    def get_user_input():
        with st.form(key='linkedin_scraper_form'):
            job_title_input = st.text_input('Job Title').split(',')
            job_location = st.text_input('Job Location', value='India')
            job_count = st.number_input('Job Count', min_value=1, value=1)
            skills_input = st.text_area('List Your Skills (comma-separated)').split(',')
            submit = st.form_submit_button('Submit')
        return job_title_input, job_location, job_count, skills_input, submit

    @staticmethod
    def build_url(job_title, job_location):
        job_title = '%2C%20'.join('%20'.join(i.split()) for i in job_title)
        link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location={job_location}&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"
        return link

    @staticmethod
    def open_link(driver, link):
        while True:
            try:
                driver.get(link)
                driver.implicitly_wait(5)
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value='span.switcher-tabs__placeholder-text.m-auto')
                return
            except NoSuchElementException:
                continue

    @staticmethod
    def link_open_scrolldown(driver, link, job_count):
        LinkedinScraper.open_link(driver, link)
        for _ in range(job_count):
            body = driver.find_element(by=By.TAG_NAME, value='body')
            body.send_keys(Keys.PAGE_UP)
            try:
                driver.find_element(by=By.CSS_SELECTOR, 
                    value="button[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']>icon>svg").click()
            except:
                pass
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(2)
            try:
                driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
                driver.implicitly_wait(5)
            except:
                pass

    @staticmethod
    def job_title_filter(scrap_job_title, user_job_title_input):
        user_input = [i.lower().strip() for i in user_job_title_input]
        scrap_title = [i.lower().strip() for i in [scrap_job_title]]
        confirmation_count = 0
        for i in user_input:
            if all(j in scrap_title[0] for j in i.split()):
                confirmation_count += 1
        return scrap_job_title if confirmation_count > 0 else np.nan

    @staticmethod
    def scrap_company_data(driver, job_title_input, job_location):
        company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
        company_name = [i.text for i in company]
        location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
        company_location = [i.text for i in location]
        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
        job_title = [i.text for i in title]
        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        website_url = [i.get_attribute('href') for i in url]
        
        df = pd.DataFrame(company_name, columns=['Company Name'])
        df['Job Title'] = pd.DataFrame(job_title)
        df['Location'] = pd.DataFrame(company_location)
        df['Website URL'] = pd.DataFrame(website_url)
        df['Job Title'] = df['Job Title'].apply(lambda x: LinkedinScraper.job_title_filter(x, job_title_input))
        df['Location'] = df['Location'].apply(lambda x: x if job_location.lower() in x.lower() else np.nan)
        df = df.dropna().reset_index(drop=True)
        return df 

    @staticmethod
    def scrap_job_description(driver, df, job_count):
        website_url = df['Website URL'].tolist()
        job_description = []
        description_count = 0
        for i in range(len(website_url)):
            try:
                LinkedinScraper.open_link(driver, website_url[i])
                driver.find_element(by=By.CSS_SELECTOR, 
                    value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
                driver.implicitly_wait(5)
                time.sleep(1)
                description = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="show-more-less-html__markup relative overflow-hidden"]')
                data = [i.text for i in description][0]
                if len(data.strip()) > 0 and data not in job_description:
                    job_description.append(data)
                    description_count += 1
                else:
                    job_description.append('Description Not Available')
            except:
                job_description.append('Description Not Available')
            if description_count == job_count:
                break

        df = df.iloc[:len(job_description), :]
        df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
        df['Job Description'] = df['Job Description'].apply(lambda x: np.nan if x == 'Description Not Available' else x)
        df = df.dropna().reset_index(drop=True)
        return df

    @staticmethod
    def calculate_skill_match(job_description, user_skills):
        job_skills = [skill.strip().lower() for skill in user_skills if skill.strip()]
        matched_skills = [skill for skill in job_skills if skill in job_description.lower()]
        match_percentage = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
        return match_percentage, matched_skills

    @staticmethod
    def display_data_userinterface(df_final, user_skills):
        if len(df_final) > 0:
            for i in range(len(df_final)):
                st.markdown(f'<h3 style="color: orange;">Job Posting Details : {i + 1}</h3>', unsafe_allow_html=True)
                st.write(f"Company Name : {df_final.iloc[i, 0]}")
                st.write(f"Job Title : {df_final.iloc[i, 1]}")
                st.write(f"Location : {df_final.iloc[i, 2]}")
                st.write(f"Website URL : {df_final.iloc[i, 3]}")
                
                with st.expander('Job Description'):
                    job_description = df_final.iloc[i, 4]
                    st.write(job_description)

                    match_percentage, matched_skills = LinkedinScraper.calculate_skill_match(job_description, user_skills)
                    st.write(f"Getting percent: {match_percentage:.2f}%")
                    st.write(f"Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}")
        else:
            st.markdown('<h5 style="text-align: center;color: orange;">No Matching Jobs Found</h5>', unsafe_allow_html=True)

    @staticmethod
    def main():
        driver = None
        try:
            job_title_input, job_location, job_count, skills_input, submit = LinkedinScraper.get_user_input()
            if submit:
                if job_title_input and job_location:
                    with st.spinner('Setting up Chrome Webdriver...'):
                        driver = LinkedinScraper.webdriver_setup()
                    with st.spinner('Loading job listings...'):
                        link = LinkedinScraper.build_url(job_title_input, job_location)
                        LinkedinScraper.link_open_scrolldown(driver, link, job_count)
                    with st.spinner('Scraping job details...'):
                        df = LinkedinScraper.scrap_company_data(driver, job_title_input, job_location)
                        df_final = LinkedinScraper.scrap_job_description(driver, df, job_count)
                    LinkedinScraper.display_data_userinterface(df_final, skills_input)
                else:
                    st.markdown('<h5 style="text-align: center;color: orange;">Job Title or Location is missing</h5>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<h5 style="text-align: center;color: orange;">Error: {e}</h5>', unsafe_allow_html=True)
        finally:
            if driver:
                driver.quit()


# --- Main Execution ---
streamlit_config()
LinkedinScraper.main()
