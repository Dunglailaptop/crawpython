import os
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time
import csv
import json
import unicodedata
import re
from tkinter import ttk, filedialog, Tk
import datetime
from tkinter import *
from tkcalendar import DateEntry

def remove_vietnamese_accents(text):
    # Chuyển đổi chuỗi thành dạng chuẩn NFD (Normalization Form D)
    normalized_text = unicodedata.normalize('NFD', text)
    # Loại bỏ các ký tự dấu (accent)
    without_accents = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
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
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)

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
#ngay 
        
##lay ngay 2
# def set_date2(driver, element_id, date_value):
#     try:
#         # Chờ đến khi phần tử có ID xuất hiện
#         searchIdDateTime = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, element_id))
#         )

#         # Tìm thẻ <span> với class 'input-group-addon' bên trong phần tử
#         findspan = searchIdDateTime.find_element(By.CLASS_NAME, 'input-group-addon')

#         # Click vào thẻ <span> để mở lịch
#         findspan.click()
#         time.sleep(2)  # Thêm thời gian chờ để đảm bảo lịch được mở

#         # Tách date_value thành ngày, tháng và năm
#         day, month, year = date_value.split('/')
#         print(int(month) + 1)
#         # Gọi hàm select_date để chọn tháng và năm
#         select_date(driver, int(month) - 1, year)  # Chuyển đổi tháng về dạng số và trừ 1 vì tháng trong datepicker bắt đầu từ 0

#         # Chọn ngày
#         day_xpath = f"//td[@data-month='{month}' and @data-year='{year}']/a[text()='{day}']"
#         day_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, day_xpath))
#         )
#         time.sleep(1)  # Thêm thời gian chờ
#         day_element.click()

#     except Exception as e:
#         print(f"Lỗi trong quá trình xử lý: {e}")

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

def click_search_button(driver,csvfile,jsonfile):
    try:
        menu_crud = driver.find_element(By.ID,"menuCrud")
        
        # Tìm thẻ span với id "btnSearch" bên trong menuCrud
        btn_search = menu_crud.find_element(By.ID, "btnSearch")
        
        # Click vào thẻ span
        btn_search.click()
        
        time.sleep(5)
        Total = check_and_click_page(driver)
        # if Total is not None:
        #     numberpage = Total / 80
        #     numberpage_rounded = math.ceil(numberpage)
        #     print(f"Number of pages (rounded up): {numberpage_rounded}")
        # check_and_click_page_callback(driver)
        getdiv = driver.find_element(By.CLASS_NAME, 'j-bar-warp')
        getclick = getdiv.find_element(By.CLASS_NAME, "j-bar-first")
        print(getclick.get_attribute('outerHTML'))
        if getclick.get_attribute('disabled') == None:
           getclick.click()
        
         # Extract header data
        data_header = extract_header_data(driver)
        print(data_header)
        iterations = 3
        for i in range(iterations):
          csv_file = f"{i}_{csvfile}"
          json_file = f"{i}_{jsonfile}"
          if i > 0:
            click_next(driver)
            print(f"Iteration {i + 1}")
          extract_and_save_table_data(driver, data_header, csv_file, json_file,jsonfile)
       
    
           
        # Extract table data and save to CSV and JSON
        # extract_and_save_table_data(driver, data_header, csvfile, jsonfile)
        
    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")

def select_area_data(driver, url, date1, date2,csvfile,jsonfile):
    driver.get(url)
    time.sleep(2)
    set_date2(driver, "dbFrom","01/01/2023")
    set_date2(driver, "dbTo", "30/04/2023")
 
    click_search_button(driver,csvfile,jsonfile)
    # check_and_click_page(driver)

    # # # set_date(driver, "dbTo", date2)
    # try:
    #             # Add explicit wait to ensure the element is present
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "menuCrud"))
    #     )

    #     getdiv = driver.find_element(By.ID, "menuCrud")
    #     getdivs = getdiv.find_element(By.CSS_SELECTOR, ".j-bar.j-button-bar")
    #     getspan = getdivs.find_element(By.CSS_SELECTOR, ".j-bar-warp")
    #     getspans = getspan.find_element(By.CSS_SELECTOR, ".j-bar-info")
    #     print(getspans.text)
    # except Exception as e:
    #     print(f"Error: {e}")
    # finally:
    #     driver.switch_to.default_content()


# Function to extract header data
def extract_header_data(driver):
    listbody_div_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lstMain-head"))
    )
    table_header = listbody_div_header.find_element(By.TAG_NAME, 'table')
    tbody_header = table_header.find_elements(By.TAG_NAME, "tbody")
    rows = tbody_header[0].find_elements(By.TAG_NAME, "tr")
    data_header = [col.text for row in rows for col in row.find_elements(By.TAG_NAME, "th")[1:]]
    return data_header



    
# def extract_and_save_table_data(driver, data_header, csv_filename, json_filename):
#     listbody_div = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, 'lstMain-body'))
#     )
#     table = listbody_div.find_element(By.TAG_NAME, 'table')
#     tbodys = table.find_elements(By.TAG_NAME, "tbody")
#     rows = tbodys[1].find_elements(By.TAG_NAME, 'tr')

#     data_array_all = []
#     number = 1

#     # Kiểm tra xem tệp CSV có tồn tại hay không
#     csv_file_exists = os.path.exists(csv_filename)
#     json_file_exists = os.path.exists(json_filename)

#     # Mở tệp CSV ở chế độ ghi thêm ('a') nếu nó tồn tại và ở chế độ ghi ('w') nếu không
#     with open(csv_filename, 'a' if csv_file_exists else 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.writer(csvfile)

#         # Ghi tiêu đề vào CSV nếu tệp không tồn tại
#         if not csv_file_exists:
#             csvwriter.writerow(['Number'] + data_header)

#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, 'td')[1:]
#             data_row = []
#             data_row.append(number)
#             number += 1
#             for col in cols:
#                 try:
#                     actions = ActionChains(driver)
#                     actions.move_to_element(col).perform()
#                     text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
#                     data_row.append(text)
#                 except Exception as e:
#                     print(f"Error accessing column: {e}")
#                     data_row.append("")

#             csvwriter.writerow(data_row)
#             data_array_all.append(data_row)

#     # Cập nhật tệp JSON
#     try:
#         if json_file_exists:
#             with open(json_filename, 'r', encoding='utf-8') as json_file:
#                 object_array = json.load(json_file)
#         else:
#             object_array = []

#         object_array.extend([{key: value for key, value in zip(data_header, data_row)} for data_row in data_array_all])

#         with open(json_filename, 'w', encoding='utf-8') as json_file:
#             json.dump(object_array, json_file, ensure_ascii=False, indent=4)

#     except Exception as e:
#         print(f"Lỗi trong quá trình xử lý JSON: {e}")
# Function to extract table data and save to CSV and JSON
# def extract_and_save_table_data(driver, data_header, csv_filename, json_filename):
#     base_path = r'D:\tool\tooltestdatacanlamsan\ToolTestData\ToolTestData\View\CrawData\Json'
#     # full_path = os.path.join(base_path, folder)
#     # os.makedirs(full_path, exist_ok=True)  #
#     csv_filename = os.path.join(base_path, csv_filename)
#     json_filename = os.path.join(base_path, json_filename)
#     listbody_div = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, 'lstMain-body'))
#     )
#     table = listbody_div.find_element(By.TAG_NAME, 'table')
#     tbodys = table.find_elements(By.TAG_NAME, "tbody")
#     rows = tbodys[1].find_elements(By.TAG_NAME, 'tr')

#     data_array_all = []
#     number = 1
#     with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.writer(csvfile)
        
#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, 'td')[1:]
#             data_row = []
#             # data_row.append(number)
#             # number += 1
#             for col in cols:
#                 try:
#                     actions = ActionChains(driver)
#                     actions.move_to_element(col).perform()
#                     text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
#                     data_row.append(text)
#                 except Exception as e:
#                     print(f"Error accessing column: {e}")
#                     data_row.append("")

#             csvwriter.writerow(data_row)
#             data_array_all.append(data_row)

#     object_array = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_array_all]

#     with open(json_filename, 'w', encoding='utf-8') as json_file:
#         json.dump(object_array, json_file, ensure_ascii=False, indent=4)
# new code funtction
def extract_and_save_table_data(driver, data_header, csv_filename, json_filename, folder):
    base_path = r'D:\tool\tooltestdatacanlamsan\ToolTestData\ToolTestData\View\CrawData\Json'
    full_path = os.path.join(base_path, folder)
    os.makedirs(full_path, exist_ok=True)  # Tạo thư mục nếu nó không tồn tại

    csv_filename = os.path.join(base_path, csv_filename)
    json_filename = os.path.join(base_path, json_filename)
    time.sleep(4)
    def locate_table():
        listbody_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'lstMain-body'))
        )
        table = listbody_div.find_element(By.TAG_NAME, 'table')
        tbodys = table.find_elements(By.TAG_NAME, "tbody")
        return tbodys[1].find_elements(By.TAG_NAME, 'tr')

    data_array_all = []
    number = 1
    def get_row_data():
        rows = locate_table()
        data_array = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')[1:]
            data_row = []
            print(f"==doi tuong dau tien{number}===")
            for col in cols:
                retry_count = 3
                numberofcol = 1
                while retry_count > 0:
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(col).perform()
                        text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
                        # Đợi và lấy thẻ <i> nếu tồn tại bên trong col
                        try:
                            icon_element = WebDriverWait(col, 2).until(
                                EC.presence_of_element_located((By.TAG_NAME, "i"))
                            )
                            icon_html = icon_element.get_attribute('outerHTML')
                            print(f"Icon HTML in column {numberofcol}: {icon_html}")
                        except:
                            print(f"No <i> element found in column {numberofcol}")
                        print(f"thuoc {numberofcol}:{text}")
                        numberofcol += 1
                        data_row.append(text)
                        break
                    except StaleElementReferenceException:
                        retry_count -= 1
                        if retry_count == 0:
                            print(f"Lỗi khi truy cập cột sau {3 - retry_count} lần thử")
                            data_row.append("")
                        else:
                            print("vo roi ne")
                            time.sleep(3)
                            rows = locate_table()  # Định vị lại các hàng trong bảng
                            # col = rows[rows.index(row)].find_elements(By.TAG_NAME, 'td')[1:][cols.index(col)]
                            time.sleep(3)
            print("===============================")
            data_array.append(data_row)
        return data_array

    data_array_all = get_row_data()

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for data_row in data_array_all:
            csvwriter.writerow(data_row)

    object_array = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_array_all]

    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(object_array, json_file, ensure_ascii=False, indent=4)
     # Di chuyển về đầu bảng
    try:
        first_row = locate_table()[0]
        actions = ActionChains(driver)
        actions.move_to_element(first_row).perform()
    except Exception as e:
        print(f"Lỗi khi di chuyển về đầu bảng: {e}")
        
# Main function to run the script
def main(type,date1,date2):
    try:     
        chromedriver_path = "chromedriver.exe"  # Ensure this path is correct
        login_url = "http://192.168.0.65:8180/"
        area_data_url = ""
        username = "quyen.ngoq"
        password = "74777477"
        csv_filename = ''
        json_filename = ''
        if type == 1:
            area_data_url = "http://192.168.0.65:8180/#menu=291&action=557"
            csv_filename = 'LoMau.csv'
            json_filename = 'LoMau.json'
        elif type == 2:
            area_data_url = "http://192.168.0.65:8180/#menu=292&action=547"
            csv_filename = 'TuiMau.csv'
            json_filename = 'TuiMau.json'


        print(f"Chromedriver path: {chromedriver_path}")
        # Initialize and log into the system
        driver = login(chromedriver_path, login_url, username, password)
        if not driver:
            print("Failed to initialize the web driver.")
            return
        # Select area data
        select_area_data(driver, area_data_url,date1,date2,csv_filename,json_filename)
        # Wait for a while before closing the browser
        time.sleep(10)
        # Close the browser
        driver.quit()
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi chính: {e}")

def on_button_click():
    print("Button clicked!")
    

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            print(data)  # Print or process the JSON data as needed


def get_dates(cal,cal2,number):
    date1 = cal.get_date().strftime('%d/%m/%Y')
    date2 = cal2.get_date().strftime('%d/%m/%Y')
    print(f"Selected Date 1: {date1}")
    print(f"Selected Date 2: {date2}")
    main(number,date1,date2)
    return [date1,date2]

def khoitaoapp():
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

    # Mapping of combo box items to corresponding numbers
    item_to_number = {
        "Lô Máu": 1,
        "Túi Máu": 2,
        "Cấu Hình": 3
    }
    date1 = ''
    date2 = ''
    # Function to handle selection event
    def on_select(event):
         selected_item = combo.get()
         selected_number = item_to_number.get(selected_item, None)
         if selected_number is not None:
          print(f"Selected number: {selected_number}")
          numberget[0] = selected_number
         
         else:
          print(f"Selected item is not valid: {selected_item}")
        # Create a label to display instructions
    label = ttk.Label(root, text="SIÊU PHẦN MỀM CRAW DATA")
    label.pack(pady=10)
    # Create a label to display instructions
    label = ttk.Label(root, text="Choose an option:")
    label.pack(pady=10)

    # Create a ComboBox widget
    combo = ttk.Combobox(root, values=list(item_to_number.keys()),width=30)
    combo.pack(pady=10)
   

    # Set the default value (optional)
    combo.set("Lô Máu")

    # Bind the selection event
    combo.bind("<<ComboboxSelected>>", on_select)
  

    file_button = ttk.Button(root, text="Select File", command=select_file, width=30)  # Corrected here
    file_button.pack(pady=10)
   #datetime picker
    
    cal = DateEntry(root,selectmode='day')
    cal.pack(pady=10)

    cal2 = DateEntry(root,selectmode='day')
    cal2.pack(pady=10)
     
    button = ttk.Button(root, text="Get Dates", command=lambda: get_dates(cal, cal2,numberget[0]))
    button.pack(pady=10)
    
    # Start the Tkinter event loop
    root.mainloop()



# Run the main function
if __name__ == "__main__":
    khoitaoapp()
