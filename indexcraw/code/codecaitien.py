import os
import time
import csv
import json
import re
import unicodedata
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from unidecode import unidecode

# Helper functions
def call_api(datapost, url):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=datapost)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        return f"Request failed with status code: {response.status_code}"

def remove_vietnamese_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    without_accents = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
    without_accents = without_accents.replace('Đ', 'D').replace('đ', 'd')
    return without_accents

def remove_spaces(text):
    return re.sub(r'\s+', '', text)

def process_text(text):
    return remove_spaces(remove_vietnamese_accents(text))

# Selenium related functions
def init_driver(chromedriver_path):
    if not os.path.isfile(chromedriver_path):
        raise ValueError(f"Invalid file path: {chromedriver_path}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def login(driver, url, username, password):
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)
        
        driver.find_element(By.ID, "txtUsername").send_keys(username)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "btnLogin").click()
        time.sleep(5)
        
        driver.find_element(By.ID, "btnSave").click()
        time.sleep(3)
    except Exception as e:
        print(f"Error during login: {e}")

def select_date(driver, month, year):
    try:
        year_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-year'))
        )
        year_select.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//option[@value='{year}']"))
        ).click()

        month_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-month'))
        )
        month_select.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//option[@value='{month}']"))
        ).click()
    except Exception as e:
        print(f"Error selecting date: {e}")

def set_date(driver, element_id, date_value):
    try:
        day, month, year = date_value.split('/')
        day, month, year = int(day), int(month) - 1, int(year)
        
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        date_element.find_element(By.CLASS_NAME, 'input-group-addon').click()
        time.sleep(2)
        
        select_date(driver, month, year)
        
        day_xpath = f"//td[not(contains(@class, 'ui-datepicker-other-month')) and @data-month='{month}' and @data-year='{year}']/a[text()='{day}']"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, day_xpath))
        ).click()
    except Exception as e:
        print(f"Error setting date: {e}")

def check_and_click_page(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'j-bar-last'))
        )
        time.sleep(3)
        
        for button in driver.find_elements(By.CLASS_NAME, 'j-bar-last'):
            if not button.get_attribute('disabled'):
                driver.execute_script("arguments[0].click();", button)
                break
        time.sleep(3)
        
        span_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'j-bar-info'))
        ).text
        return span_text.split('/')[-1].strip().strip(']')
    except Exception as e:
        print(f"Error clicking page: {e}")
        return None

def check_and_click_page_callback(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'j-bar-first'))
        )
        time.sleep(3)
        
        for button in driver.find_elements(By.CLASS_NAME, 'j-bar-first'):
            if not button.get_attribute('disabled'):
                driver.execute_script("arguments[0].click();", button)
                break
        time.sleep(3)
    except Exception as e:
        print(f"Error clicking page callback: {e}")

def click_next(driver):
    try:
        driver.find_element(By.CLASS_NAME, 'j-bar-warp').find_element(By.CLASS_NAME, "j-bar-next").click()
    except Exception as e:
        print(f"Error clicking next: {e}")

def click_search_button(driver, csvfile, jsonfile):
    try:
        driver.find_element(By.ID, "menuCrud").find_element(By.ID, "btnSearch").click()
        time.sleep(5)
        
        total_pages = check_and_click_page(driver)
        check_and_click_page_callback(driver)
        
        data_header = extract_header_data(driver)
        print(data_header)
        
        iterations = 3
        for i in range(iterations):
            if i > 0:
                click_next(driver)
                print(f"Iteration {i + 1}")
            extract_and_save_table_data(driver, data_header, f"{i}_{csvfile}", f"{i}_{jsonfile}")
    except Exception as e:
        print(f"Error clicking search button: {e}")

def select_area_data(driver, url, date1, date2, csvfile, jsonfile):
    driver.get(url)
    time.sleep(2)
    
    set_date(driver, "dbFrom", date1)
    set_date(driver, "dbTo", date2)
    
    click_search_button(driver, csvfile, jsonfile)

# Data extraction functions
def extract_header_data(driver):
    try:
        header_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lstMain-head"))
        )
        table_header = header_div.find_element(By.TAG_NAME, 'table')
        rows = table_header.find_elements(By.TAG_NAME, "tr")
        return [process_text(col.text) for row in rows for col in row.find_elements(By.TAG_NAME, "th")[1:]]
    except Exception as e:
        print(f"Error extracting header data: {e}")
        return []

def extract_and_save_table_data(driver, data_header, csv_filename, json_filename):
    base_path = r'D:\tool\tooltestdatacanlamsan\ToolTestData\ToolTestData\View\CrawData\Json'
    csv_path = os.path.join(base_path, csv_filename)
    json_path = os.path.join(base_path, json_filename)
    
    try:
        body_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lstMain-body'))
        )
        table = body_div.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, "tbody")[1].find_elements(By.TAG_NAME, 'tr')
        
        data_all = []
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')[1:]
                data_row = []
                for col in cols:
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(col).perform()
                        text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
                        data_row.append(text)
                    except Exception as e:
                        print(f"Error accessing column: {e}")
                        data_row.append("")
                csvwriter.writerow(data_row)
                data_all.append(data_row)
        
        json_data = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_all]
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error extracting and saving table data: {e}")

# Main logic
if __name__ == "__main__":
    chromedriver_path = 'path/to/chromedriver'
    login_url = 'https://example.com/login'
    data_url = 'https://example.com/data'
    username = 'quyen.ngoq'
    password = '74777477'
    date1 = '01/01/2023'
    date2 = '31/01/2023'
    csvfile = 'output.csv'
    jsonfile = 'output.json'
    
    driver = init_driver(chromedriver_path)
    try:
        login(driver, login_url, username, password)
        select_area_data(driver, data_url, date1, date2, csvfile, jsonfile)
    finally:
        driver.quit()
