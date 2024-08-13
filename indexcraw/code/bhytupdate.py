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
import openpyxl

urlFolder = ""

def read_excel():
    global urlFolder
    # Mở workbook
    workbook = openpyxl.load_workbook(urlFolder)
    
    # Chọn sheet đầu tiên (hoặc bạn có thể chỉ định tên sheet)
    sheet = workbook.active
    
    # Lấy tên các cột
    columns = [cell.value for cell in sheet[1]]
    
    # Lấy dữ liệu từng dòng
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(row)
    for row in data:
        print(row)
    
      

def get_data_table(driver):
      # Đợi cho bảng xuất hiện
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "group-tb"))
    )

    # Tìm tất cả các hàng trong tbody
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

    # In số lượng quận/huyện
    print(f"Số lượng quận/huyện: {len(rows)}")
    print("===dô lấy dữ liệu nè===")
    # Lặp qua từng hàng và in thông tin
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) >= 3:  # Đảm bảo có đủ cột
           print("===đang kiểm tra tên quận/huyện")
           

        # Kiểm tra trạng thái khóa
        lock_button = row.find_elements(By.CSS_SELECTOR, "button.btn-success")
        unlock_button = row.find_elements(By.CSS_SELECTOR, "button.btn-danger")
        
        if lock_button:
            print("Trạng thái: Đang mở")
        elif unlock_button:
            print("Trạng thái: Đang khóa")
        else:
            print("Trạng thái: Không xác định")

        print("-" * 50)

def login():
    try:      
        print("===thực thi login===")
        login_url = "http://192.168.0.77/dist/#!/login"
        area_data_url = ""
        username = "quyen.ngoq"
        password = "74777477"
        area_data_url = "http://192.168.0.77/dist/#!/hanhchinh/district"  
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  
        options.add_argument("--window-size=1920x1080")  
        driver = webdriver.Chrome(options=options)
        driver.get(login_url)
        driver.maximize_window()
        time.sleep(1)
        usernames = driver.find_element(By.ID,"username")
        usernames.send_keys(username)
        
        passwords = driver.find_element(By.ID,"password")
        passwords.send_keys(password)
        
         # Find and click the login button
        findbuttonlogin = driver.find_element(By.CLASS_NAME,"col-6")
        login_button = findbuttonlogin.find_element(By.TAG_NAME, "button")
        login_button.click()
        time.sleep(3)
        driver.get(area_data_url)
        time.sleep(3)
              # Đợi cho phần tử select xuất hiện
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "district"))
        )

        # Lấy tất cả các option
        options = select_element.find_elements(By.TAG_NAME, "option")

        # In ra số lượng tỉnh thành
        print(f"Số lượng tỉnh thành: {len(options) - 1}")  # Trừ 1 vì có option mặc định

        # In ra danh sách tỉnh thành
        for option in options[1:]:  # Bỏ qua option đầu tiên (--Chọn tỉnh thành--)
            value = option.get_attribute("value")
            text = option.text
            print(f"Mã: {value}, Tên: {text}")
        options[4].click()
        time.sleep(4)
        get_data_table(driver)
        driver.quit()
        
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi chính: {e}")
        if driver:
           driver.quit()
    return driver

def select_Excel_File():
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )
    print(file_path)
    if file_path:
        urlFolder = file_path
        read_excel()
    else:
        print("No file selected.")

# login()

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
    # Create a label to display instructions
label = ttk.Label(root, text="SIÊU PHẦN MỀM CRAW DATA")
label.pack(pady=10)



  
button = ttk.Button(root, text="Get Data", command=select_Excel_File)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
