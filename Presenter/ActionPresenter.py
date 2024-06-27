# presenter.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import json
import time
import csv
import json
import os
import unicodedata
import re

# driver.maximize_window()

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

    def process_text(self,text):
        text_without_accents = self.remove_vietnamese_accents(text)
        text_without_spaces = self.remove_spaces(text_without_accents)
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
    def ActionLogin(self):
       
        # Đường dẫn tới chromedriver
        chromedriver_path = "indexcraw/chromedriver.exe"  # Đảm bảo đường dẫn này là đúng
        # # Cấu hình tùy chọn cho Chrome
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Chạy ở chế độ headless
        # chrome_options.add_argument("--disable-gpu")  # Tùy chọn này dành cho Windows
        # chrome_options.add_argument("--no-sandbox")  # Tùy chọn này dành cho Linux

        # # Khởi tạo ChromeDriver
        # service = Service(chromedriver_path)
        # driver = webdriver.Chrome(service=service, options=chrome_options)

        # # Khởi tạo ChromeDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)

        # Mở trang web
        driver.get("http://192.168.0.65:8180/")  # Thay thế bằng URL trang đăng nhập của bạn
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
        listbody_divHeader = driver.find_element(By.ID,"lstMain-head")

        tableheader = listbody_divHeader.find_element(By.TAG_NAME,'table')

        tbodyheader = tableheader.find_elements(By.TAG_NAME,"tbody")

        rows2 = tbodyheader[0].find_elements(By.TAG_NAME,"tr")
        for row in rows2:
            cols3 = row.find_elements(By.TAG_NAME,"th")
            
            col4 = cols3[1:]
            data_header = []
            
            for col in col4:
                print(col.text)
                data_header.append(self.process_text(col.text))
        self.crawldata(data_header,driver)
   #hàm lấy data header
   
    def crawldata(data_header,driver):
                # Tìm thẻ div với id là 'listbody'
        listbody_div = driver.find_element(By.ID, 'lstMain-body')

        # Tìm thẻ table trong div 'listbody'
        table = listbody_div.find_element(By.TAG_NAME, 'table')

        object_array = []
        #chỉ định đường dẫn
        # Chỉ định đường dẫn nơi các tệp sẽ được tạo ra
        output_directory = "d:/USER DATA/Documents/nd2developer/DataText/DataNhapTest"
        csv_filename = "MaSanPhamISBT.csv"
        json_filename = "MaSanPhamISBT.json"

        # Tạo thư mục nếu nó chưa tồn tại
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Đường dẫn đầy đủ đến các tệp
        csv_file_path = os.path.join(output_directory, csv_filename)
        json_file_path = os.path.join(output_directory, json_filename)
        # Open the CSV file to write data
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Giả sử 'tbodys' là danh sách các phần tử tbody lấy từ trang web
            # Tìm tất cả các thẻ tbody trong table
            tbodys = table.find_elements(By.TAG_NAME, "tbody")
            # Khởi tạo 'rows' từ phần tử tbody đầu tiên
            rows = tbodys[1].find_elements(By.TAG_NAME,'tr')
            demstt = 0
            breakSTT = 1
            data_Array_all = []
            # for row in rows2:
            for row in rows:
                # Lấy tất cả các cột trong hàng hiện tại
                cols = row.find_elements(By.TAG_NAME,'td')
                # Loại bỏ cột đầu tiên
                cols2 = cols[1:]
                
                data_row = []
                #VÒNG    
                for col in cols2:
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(col).perform()

                        # Sử dụng WebDriverWait để đợi phần tử có thể truy cập
                        text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
                        data_row.append(text)
                        print(text + "\n")
                        demstt += 1
                        print("Lấy data của hàng"+demstt)
                    except Exception as e:
                        print(f"Error accessing column: {e}")
                        data_row.append("")
                
                # Ghi dữ liệu của hàng vào tệp CSV
                csvwriter.writerow(data_row)
                data_Array_all.append(data_row)
                # After processing all columns in the row
                demstt += 1
        

        object_array = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_Array_all]
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(object_array, json_file, ensure_ascii=False, indent=4)      

        time.sleep(10)

        # Close the browser
        driver.quit()
       