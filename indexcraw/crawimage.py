# import os
# import math
# import requests
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# from PIL import Image
# from unidecode import unidecode 
# from tkinter import ttk, filedialog, Tk
# from datetime import datetime
# from tkinter import *
# from tkcalendar import DateEntry
# import time
# import csv
# import json
# import unicodedata
# import re
# import requests
# import io

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from concurrent.futures import ThreadPoolExecutor, as_completed
from unidecode import unidecode 
from tkinter import ttk, filedialog, Tk
from datetime import datetime
from tkinter import *
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import openpyxl
import pandas as pd
import math
import time
import csv
import json
import unicodedata
import re
import requests
import io
import os
from PIL import Image
import numpy as np


dateSelect = ''
page = 2

def call_api_import_size(json_file_path, url, chunk_size=100):
    with open(json_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)

    headers = {
        "Content-Type": "application/json"
    }

    def import_chunk(chunk):
        try:
            response = requests.post(url, json=chunk, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error importing chunk: {e}")
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            print(f"Sending chunk {i//chunk_size + 1} (size: {len(chunk)})")
            futures.append(executor.submit(import_chunk, chunk))

        for future in as_completed(futures):
            result = future.result()
            if result:
                print(json.dumps(result, indent=2))

    print("All data chunks have been processed.")

def call_api_import(datapost,urls):
    url = urls
    print(datapost)
    
    dataapitest = [{
        "ID": "56181185",
        "Ma": "KTC01",
        "Ten": "T\u00fai Ti\u1ec3u C\u1ea7u [40ml]",
        "Tenviettat": "T\u00fai Ti\u1ec3u C\u1ea7u [40ml]",
        "Loai": "M\u00e1u",
        "Thetich": "40 ml",
        "Gia": "449,167 \u20ab",
        "Ngaytao": "20/05/2022",
        "Uutien": "0"
    }]
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=datapost,headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Yêu cầu thất bại với mã lỗi: {response.status_code}")
        Message = f"Yêu cầu thất bại với mã lỗi: {response.status_code}"
        return Message

def remove_vietnamese_accents(text):
    # Chuyển đổi chuỗi thành dạng chuẩn NFD (Normalization Form D)
    normalized_text = unicodedata.normalize('NFD', text)
    # Loại bỏ các ký tự dấu (accent)
    without_accents = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
    # Thay thế chữ Đ và đ thành D và d
    without_accents = without_accents.replace('Đ', 'D').replace('đ', 'd')
    return without_accents


def remove_spaces(text):
    # Loại bỏ khoảng cách
    return re.sub(r'\s+', '', text)

def process_text(text):
    text_without_accents = remove_vietnamese_accents(text)
    text_without_spaces = remove_spaces(text_without_accents)
    return text_without_spaces

# Function to initialize and log into the system
def login(chromedriver_path, url, username, password):
    try:      
        if not os.path.isfile(chromedriver_path):
            raise ValueError(f"The path is not a valid file: {chromedriver_path}")
        
        print(f"Using chromedriver at: {chromedriver_path}")
        # # # Initialize ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        #     # Thêm các tùy chọn để giảm tải CPU và bộ nhớ
        # options.add_argument("--no-zygote")
        # options.add_argument("--single-process")
        # options.add_argument("--disable-setuid-sandbox")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--disable-accelerated-2d-canvas")
        # options.add_argument("--disable-gpu-sandbox")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service,options=options)

        # Open the website
        driver.get(url)
        driver.maximize_window()

        # Wait for the page to load
        time.sleep(1)

        # Find and enter username
        username_input = driver.find_element(By.ID, "txtUsername")
        username_input.send_keys(username)

        # Find and enter password
        password_input = driver.find_element(By.ID, "txtPassword")
        password_input.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()

        # Wait for login to complete
        time.sleep(5)

        # Click save button
        save = driver.find_element(By.ID, "btnSave")
        save.click()
        time.sleep(3)
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi chính: {e}")

    return driver

def select_date(driver, month_value, year_value):
    try:
           # Chờ đợi thẻ <select> của năm xuất hiện
        year_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-year'))
        )
        # Tạo đối tượng Select và chọn giá trị năm
        year_select = Select(year_select_element)
        year_select.select_by_value(str(year_value))
        time.sleep(1)  # Thêm thời gian chờ
        # Chờ đợi thẻ <select> của tháng xuất hiện
        month_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-month'))
        )
        # Tạo đối tượng Select và chọn giá trị tháng
        month_select = Select(month_select_element)
        print("tháng đã chọn vào hệ thống:" + str(month_value))
        month_select.select_by_value(str(month_value))
        time.sleep(5)  # Thêm thời gian chờ

     

        print(f"Đã chọn tháng {month_value + 1} và năm {year_value}")

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")

def set_date(driver, element_id, date_value):
    try:
        # Chờ đến khi phần tử có ID xuất hiện
        searchIdDateTime = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )

        # Tìm thẻ <span> với class 'input-group-addon' bên trong phần tử
        findspan = searchIdDateTime.find_element(By.CLASS_NAME, 'input-group-addon')

        # Click vào thẻ <span> để mở lịch
        findspan.click()
        time.sleep(2)  # Thêm thời gian chờ để đảm bảo lịch được mở

        # Tách date_value thành ngày, tháng và năm
        day, month, year = date_value.split('/')
        print(month)
        # Gọi hàm select_date để chọn tháng và năm
        select_date(driver, int(month) - 1, year)  # Chuyển đổi tháng về dạng số và trừ 1 vì tháng trong datepicker bắt đầu từ 0

        # Chọn ngày
        day_xpath = f"//td[not(contains(@class, 'ui-datepicker-other-month')) and @data-month='{month}' and @data-year='{year}']/a[text()='{day}']"
        day_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, day_xpath))
        )
        time.sleep(1)  # Thêm thời gian chờ
        day_element.click()

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")

        


#check disabled và lấy tổng số phần tử
def check_and_click_page(driver):
    try:
        # Chờ đến khi phần tử có class 'j-bar-last' xuất hiện
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'j-bar-last'))
        )
        time.sleep(3)
        
        # Tìm phần tử với thuộc tính 'disabled="disabled"' và click vào nó
        for button in buttons:
            if button.get_attribute('disabled') == None:
                driver.execute_script("arguments[0].click();", button)  # Sử dụng JavaScript để click
                print("Clicked on the disabled 'j-bar-last' button")
                break

        time.sleep(3)

        # Lấy giá trị sau dấu '/'
        span_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'j-bar-info'))
        ).text
        total_value = span_text.split('/')[-1].strip().strip(']')
        print(f"Total value after '/': {total_value}")
        
        return total_value

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")
        return None
#call back
def check_and_click_page_callback(driver):
    try:
        # Chờ đến khi phần tử có class 'j-bar-last' xuất hiện
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'j-bar-first'))
        )
        time.sleep(3)
        
        # Tìm phần tử với thuộc tính 'disabled="disabled"' và click vào nó
        for button in buttons:
            if button.get_attribute('disabled') == None:
                driver.execute_script("arguments[0].click();", button)  # Sử dụng JavaScript để click
                print("Clicked on the disabled 'j-bar-last' button")
                break

        time.sleep(3)
    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")
        return None
 #ngay 2
def set_date2(driver, element_id, date_value):
    try:
        # Chờ đến khi phần tử có ID xuất hiện
        searchIdDateTime = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )

        # Tìm thẻ <span> với class 'input-group-addon' bên trong phần tử
        findspan = searchIdDateTime.find_element(By.CLASS_NAME, 'input-group-addon')

        # Click vào thẻ <span> để mở lịch
        findspan.click()
        time.sleep(2)  # Thêm thời gian chờ để đảm bảo lịch được mở

        # Tách date_value thành ngày, tháng và năm
        day, month, year = date_value.split('/')
        day = int(day)
        month = int(month) - 1  # Chuyển đổi tháng về dạng số và trừ 1 vì tháng trong datepicker bắt đầu từ 0
        year = int(year)

        # Gọi hàm select_date để chọn tháng và năm
        select_date(driver, month, year)

        # Chọn ngày
        day_xpath = f"//td[not(contains(@class, 'ui-datepicker-other-month')) and @data-month='{month}' and @data-year='{year}']/a[text()='{day}']"
        day_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, day_xpath))
        )
        time.sleep(1)  # Thêm thời gian chờ
        day_element.click()

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")

def select_date(driver, month, year):
    try:
        # Chọn năm
        year_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-year'))
        )
        year_select.click()
        year_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//option[@value='{year}']"))
        )
        year_option.click()

        # Chọn tháng
        month_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-datepicker-month'))
        )
        month_select.click()
        month_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//option[@value='{month}']"))
        )
        month_option.click()

    except Exception as e:
        print(f"Lỗi khi chọn tháng và năm: {e}")
##       
def click_next(driver):
    getdiv = driver.find_element(By.CLASS_NAME, 'j-bar-warp')
    getclick = getdiv.find_element(By.CLASS_NAME, "j-bar-next")
    print(getclick.get_attribute('outerHTML'))
    if getclick.get_attribute('disabled') == None:
       getclick.click()

def click_search_button(driver,urlFolder):
    global page
    try:    
        Total = check_and_click_page(driver)
        if Total is not None:
            numberpage = int(Total) / 80
            numberpage_rounded = math.ceil(numberpage)
            print(f"Number of pages (rounded up): {numberpage_rounded}")
        else:
            print("Total is None, unable to calculate the number of pages.")
        
        getdiv = driver.find_element(By.CLASS_NAME, 'j-bar-warp')
        getclick = getdiv.find_element(By.CLASS_NAME, "j-bar-first")
        print(getclick.get_attribute('outerHTML'))
        if getclick.get_attribute('disabled') is None:
           getclick.click()
        
        data_header = extract_header_data(driver)
        
        print(data_header)
        iterations = numberpage_rounded
        #doc file csv 
        
        
        #
        for i in range(iterations):
            click_next(driver)
            print(f"Iteration {i + 1}")
            if i == page:
               extract_and_save_table_data_loads_cachup(driver, page,data_header, urlFolder) 
               time.sleep(3)
               break
            # if i == page:
            #     extract_and_save_table_data_loads_cachup(driver, data_header, urlFloderSave ,urlsCsvFile)
        
    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")



   



# Function to extract header data
def extract_header_data(driver):
    listbody_div_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lstMain-head"))
    )
    table_header = listbody_div_header.find_element(By.TAG_NAME, 'table')
    tbody_header = table_header.find_elements(By.TAG_NAME, "tbody")
    rows = tbody_header[0].find_elements(By.TAG_NAME, "tr")
    data_header = [process_text(col.text) for row in rows for col in row.find_elements(By.TAG_NAME, "th")[1:]]
    return data_header


# Function to extract table data and save to CSV and JSON
def clean_price(price_str):
    return float(re.sub(r'[^\d.]', '', price_str))

def parse_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y").isoformat()


#new function
def capture_image(driver, download_path, file_name, numberId):
    try:
        # Chụp ảnh toàn màn hình
        png = driver.get_screenshot_as_png()
        
        # Sử dụng PIL để mở ảnh từ dữ liệu PNG
        im = Image.open(io.BytesIO(png))

        # Tạo đường dẫn đầy đủ cho file
        folder_path = os.path.join(download_path, str(numberId))
        full_path = os.path.join(folder_path, file_name)

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(folder_path, exist_ok=True)

        # Lưu ảnh
        im.save(full_path)

        print(f"Đã lưu ảnh: {full_path}")
        print("success")
    except Exception as e:
        print("failed -", str(e))

# craw ca chụp
def extract_and_save_table_data_loads_cachup(driver,page, data_header,urlCsvFile):
    global dateSelect
    data_header.insert(0,"STT")
    data_header.insert(1,"PAGE")
    date = datetime.strptime(dateSelect,"%d/%m/%Y")
    formatted_date = date.strftime("%d-%m-%Y")
    csv_filenames = os.path.join(urlCsvFile, f"Cachup_data_{formatted_date}.csv")
    # Đọc số lượng bản ghi hiện có trong file CSV
    
    existing_records = 0
    if os.path.exists(csv_filenames):
        with open(csv_filenames, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_records = sum(1 for row in reader) - 1  # Trừ 1 để bỏ qua header
    else: 
        print("===không tồn tại file CSV===")
        with open(csv_filenames, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data_header)
            print(f"Đã tạo thành công csv tai: {csv_filenames}")
    print(f"Số bản ghi hiện có: {existing_records}")

    print("=======lay du lieu ca chup========")
    time.sleep(1)

    def locate_table():
        listbody_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lstMain-body'))
        )
        table = listbody_div.find_element(By.TAG_NAME, 'table')
        tbodys = table.find_elements(By.TAG_NAME, "tbody")
        return tbodys[1].find_elements(By.TAG_NAME, 'tr')
    
    def get_series_data(number, numberId):
        series_data = []
        checkButton = False
        # Tìm tất cả các phần tử có class 'series-item'
        series_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.series-item'))
        )
        numberSeries_item = 0
        for series_item in series_items:
            numberSeries_item += 1
            series_item.click()
            time.sleep(0.5)
            
            # Lấy giá trị của thẻ 'ins-length'
           
            image_count = int(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ins-length'))
            ).text)
            print("in số lượng ảnh:" + str(image_count))

            # Chụp ảnh và lưu vào thư mục
            if image_count > 1:
                for i in range(image_count):
                    capture_image(driver, "d:\\USER DATA\\Documents\\crawpython\\indexcraw\\ImageBenhNhan\\",
                                f"saved_image_{number}_{i}_{numberSeries_item}.png", numberId)
                    time.sleep(0.5)
                    # Nhấn nút chuyển sang ảnh tiếp theo
                    next_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.paging .fa-chevron-right'))
                    )
                    next_button.click()
                    time.sleep(0.5)
            else:
                capture_image(driver, "d:\\USER DATA\\Documents\\crawpython\\indexcraw\\ImageBenhNhan\\",
                            f"saved_image_{number}_0_{numberSeries_item}.png", numberId)
            
            series_data.append({
                "image_count": image_count
            })

        return series_data

    def getData_Image(cols, number, numberId):
        # Get the first column data (assuming it's the ID or unique identifier)
        cols[0].click()
        time.sleep(0.5)  # Đợi để trang load

        div_Menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'menuCrud'))
        )
        Button_showImage = div_Menu.find_element(By.ID, 'btnWebViewer')
        Button_showImage.click()
        time.sleep(0.5)
        div_Zoom = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".layout-menu-right button[title='Toàn màn hình']"))
        )
        div_Zoom.click()
        time.sleep(0.5)

        series_data = get_series_data(number, numberId)
        # print("tong so luong anh lay dc:"+series_data)

        time.sleep(0.5)
        div_ViewImage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".layout-menu-right button[title='Thu nhỏ (ALT-M)']"))
        )
        time.sleep(0.5)
        div_ViewImage.click()
        time.sleep(0.5)
        cols[0].click()
        time.sleep(0.5)
        
    
    def get_row_data():
        rows = locate_table()
        data_array = []
        process_edit_data = []
        number = existing_records + 1
        
        # csv_filenames = os.path.join(urlCsvFile,csv_filenames)
        
        for row in rows[existing_records:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            data_row = [number,page]
            print(f"===đối tượng đầu tiên {number}===")
            number += 1
            numberIDBenhNhan = ""
            if number == 20:
               return data_array, process_edit_data
            for col in cols[1:]:
                retry_count = 1
                while retry_count > 0:
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(col).perform()
                        text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
                        try:
                            icon_element = col.find_element(By.TAG_NAME, "i")
                            icon_html = icon_element.get_attribute('outerHTML')
                            text = "True"
                        except:
                            pass
                        print(f"nhánh {len(data_row)}: {text}")
                        if len(data_row) == 0:   
                           numberIDBenhNhan = text
                        data_row.append(text)
                        
                        
                        break
                    except StaleElementReferenceException:
                        retry_count -= 1
                        if retry_count == 0:
                            print(f"Lỗi khi truy cập cột sau {3 - retry_count} lần thử")
                            data_row.append("")
                        else:
                            print("Vào rồi nè")
                            time.sleep(0.5)
                            rows = locate_table()
                            time.sleep(0.5)
            print("===============================")
            # # Ghi dữ liệu tạm thời vào file CSV
            print(f"Có quyền ghi vào thư mục: {os.access(os.path.dirname(csv_filenames), os.W_OK)}")
            with open(csv_filenames, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data_header)
                if file.tell() == 0:  # Nếu file rỗng, ghi header
                    writer.writeheader()
                writer.writerows([{data_header[i]: data_row[i] for i in range(len(data_header))}])
            data_array.append(data_row)
            # if number <= 10:   
            #    getData_Image(cols,number,numberIDBenhNhan)
        return data_array, process_edit_data
    
    data_array_all, process_edit_data = get_row_data()

    # # Ghi CSV
    # with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(data_header)
    #     csvwriter.writerows(data_array_all)

    # Tạo object array
    object_array = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_array_all]

    # Ghi JSON
   
    print("\n===== Hoàn tất hủy diệt dữ liệu =====")
   
# Main function to run the script
def main(urlFolder):
    global dateSelect
    try:
        #khai báo thông số     
        chromedriver_path = "chromedriver.exe"  # Ensure this path is correct
        login_url = "http://192.168.0.65:8180/"
        area_data_url = ""
        username = "quyen.ngoq"
        password = "74777477"
        area_data_url = "http://192.168.0.65:8180/#menu=131&action=111"
    
      
        
        driver = login(chromedriver_path, login_url, username, password)
        # chọn phân trang tính toán tổng số page
        driver.get(area_data_url)
        time.sleep(2)
        set_date2(driver, "dbFrom",dateSelect)
        set_date2(driver, "dbTo", dateSelect)
    
        click_search_button(driver,urlFolder)
        time.sleep(3)
        driver.quit()
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi chính: {e}")

def on_button_click():
    print("Button clicked!")
    

def select_folder():
    folder_path = filedialog.askdirectory(
        title="Select a folder"
    )
    if folder_path:
        print(folder_path)
        main(folder_path)
    else:
        print("No folder selected.")
        

def select_Excel_File():
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )
    print(file_path)
    if file_path:
        Export_Excel_File_And_GetData(file_path)
    else:
        print("No file selected.")
   



#đọc file excel 
def Export_Excel_File_And_GetData(file_path):
    global dateSelect
    if not file_path:
        print("Không có file nào được chọn.")
        return None
    # tìm tên file 
    file_name = os.path.basename(file_path)
    name_part, extension = os.path.splitext(file_name)
    try:
        date = datetime.strptime(name_part,"%d-%m-%Y")
        formatted_date = date.strftime("%d/%m/%Y")
        dateSelect = formatted_date
        
        # Đọc workbook
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        print(formatted_date)
    except ValueError:
        print(name_part)


root = Tk()
root.title("Tkinter ComboBox Example")

#so 
numberget = [0]
# Đặt kích thước cho cửa sổ
window_width = 400
window_height = 300

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tính toán vị trí để cửa sổ nằm giữa màn hình
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)

# Đặt kích thước và vị trí cho cửa sổ
root.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')


date1 = ''
date2 = ''
    # Create a label to display instructions
label = ttk.Label(root, text="SIÊU PHẦN MỀM CRAW ĐÁ DỮ LIỆU ẢNH")
label.pack(pady=10)
# Create a label to display instructions
label = ttk.Label(root, text="Choose an option:")
label.pack(pady=10)


#get data json
file_button = ttk.Button(root, text="Select csv Excel", command=select_Excel_File, width=30)  # Corrected here
file_button.pack(pady=10)

cal = DateEntry(root,selectmode='day')
cal.pack(pady=10)

cal2 = DateEntry(root,selectmode='day')
cal2.pack(pady=10)

button = ttk.Button(root, text="Get Data", command=select_folder, width=10)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()



# # Run the main function
# if __name__ == "__main__":
#     khoitaoapp()
