from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import io
import os
from PIL import Image
import numpy as np



# Function to initialize and log into the system
def login(chromedriver_path, url, username, password):
    try:      
        if not os.path.isfile(chromedriver_path):
            raise ValueError(f"The path is not a valid file: {chromedriver_path}")
        
        print(f"Using chromedriver at: {chromedriver_path}")
        # # # Initialize ChromeDriver
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--disable-plugins")
        # options.add_argument("--disable-software-rasterizer")
        # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

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



def capture_image(driver, download_path, file_name):
    try:
        # Chụp ảnh màn hình tại vị trí cụ thể
        png = driver.get_screenshot_as_png()
        
        # Sử dụng PIL để mở ảnh từ dữ liệu PNG
        im = Image.open(io.BytesIO(png))

        # Cắt ảnh tại vị trí cụ thể
        left = 935
        top = 17
        right = left + 682  # Giả sử kích thước ảnh là 682x376
        bottom = top + 376
        im = im.crop((left, top, right, bottom))

        # Tạo đường dẫn đầy đủ cho file
        full_path = os.path.join(download_path, file_name)
        folder_path = os.path.dirname(full_path)

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(folder_path, exist_ok=True)

        # Lưu ảnh đã cắt
        im.save(full_path)

        print(f"Đã lưu ảnh: {full_path}")
        print("success")
    except Exception as e:
        print("failed -", str(e))



chromedriver_path = "chromedriver.exe"  # Ensure this path is correct
login_url = "http://192.168.0.65:8180/"
area_data_url = ""
username = "quyen.ngoq"
password = "74777477"

driver = login(chromedriver_path, login_url, username, password)

url = "http://192.168.0.65:8180/web/wado/jpeg/5/1.2.840.113543.6.6.4.0.79408240273981.20240718.8211437/1.2.840.113543.6.6.4.0.79408240273981.8211437.20240718/1.2.840.113543.6.6.4.0.79408240273981.8211437.1855754.1721270528989?rows=1024"



driver.get(url)

time.sleep(1)



capture_image(driver, "d:\\USER DATA\\Documents\\crawpython\\indexcraw\\ImageBenhNhan\\","saved_image.png")



driver.quit()
