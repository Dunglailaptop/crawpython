# presenter.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import json


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.bind_update_button(self.on_button_clicked)

    def update_label(self):
        data = self.model.get_data()
    
    
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
    
     
    def on_button_clicked(self):
        # Lấy dữ liệu từ View
        user_input = self.view.get_textbox_data()
        # Cập nhật Model
        self.model.set_data(user_input)
        # Lấy dữ liệu từ Model và hiển thị trong View
        data = self.model.get_data()
        self.view.show_message(f"Bạn đã nhập: {data}")
    #Ham login
    def ActionLogin():
            # Đường dẫn tới chromedriver
        chromedriver_path = "indexcraw/chromedriver.exe"  # Đảm bảo đường dẫn này là đúng

        # Khởi tạo ChromeDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)

        # Mở trang web
        driver.get("http://192.168.0.65:8180/")  # Thay thế bằng URL trang đăng nhập của bạn
        driver.maximize_window()

        # Chờ trang tải
        time.sleep(1)

        # Tìm và nhập tên đăng nhập
        username_input = driver.find_element(By.ID, "txtUsername")  # Thay thế bằng id của trường username
        username_input.send_keys("quyen.ngoq")

        # Tìm và nhập mật khẩu
        password_input = driver.find_element(By.ID, "txtPassword")  # Thay thế bằng id của trường password
        password_input.send_keys("74777477")

        # Tìm và bấm nút đăng nhập
        login_button = driver.find_element(By.ID, "btnLogin")  # Thay thế bằng id của nút đăng nhập
        login_button.click()

        time.sleep(5)

        save = driver.find_element(By.ID,"btnSave")
        save.click()
        # Chờ một lúc để xem kết quả
        time.sleep(3)

        driver.get("http://192.168.0.65:8180/#menu=58&action=180")

        time.sleep(2)