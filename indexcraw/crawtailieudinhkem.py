from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import csv

# Đường dẫn tới chromedriver
chromedriver_path = "chromedriver.exe"  # Đảm bảo đường dẫn này là đúng

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

driver.get("http://192.168.0.65:8180/#menu=207&action=375")
original_tab = driver.current_window_handle

time.sleep(2)

# Tìm thẻ div với id là 'listbody'
listbody_div = driver.find_element(By.ID, 'lstMain-body')

# Tìm thẻ table trong div 'listbody'
table = listbody_div.find_element(By.TAG_NAME, 'table')



# Open the CSV file to write data
with open('datatailieudinhkem.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Giả sử 'tbodys' là danh sách các phần tử tbody lấy từ trang web
    # Tìm tất cả các thẻ tbody trong table
    tbodys = table.find_elements(By.TAG_NAME, "tbody")

    # Khởi tạo 'rows' từ phần tử tbody đầu tiên
    rows = tbodys[1].find_elements(By.TAG_NAME,'tr')
    demstt = 0
    breakSTT = 1
    
    rows2 = tbodys[0].find_elements(By.TAG_NAME,"tr")
    
    for row in rows2:
        
    

    for row in rows:
        # Lấy tất cả các cột trong hàng hiện tại
        cols = row.find_elements(By.TAG_NAME,'td')
        # Loại bỏ cột đầu tiên
        cols2 = cols[1:]
        
        data_row = []
        
        # linkimage = f"http://192.168.0.65:8180/web/media/{cols[1].text}/0/{cols[3].text}"
        # name = cols[3].text
        # print(linkimage)

        # # Mở tab mới
        # driver.execute_script("window.open('about:blank', '_blank');")

        # # Chuyển sang tab mới
        # driver.switch_to.window(driver.window_handles[1])

        # # Mở URL ảnh trong tab mới
        # driver.get(linkimage)

        # # Đợi trang tải xong
        # time.sleep(2)

        # # Chụp ảnh màn hình và lưu với tên duy nhất
        # # screenshot_filename = f"screenshot_{cols[1].text}_{cols[3].text}.png"
        # driver.save_screenshot(f"{name}.png")
        # data_row.append(linkimage)

        # # Đóng tab hiện tại (tab mới)
        # driver.close()

        # # Chuyển về tab ban đầu
        # driver.switch_to.window(original_tab)
        
        for col in cols2:
            if demstt == 20:
            #    time.sleep(3)
               print(str(demstt)+"||"+col.text)
               demstt = 0
            try:
                
                
                actions = ActionChains(driver)
                actions.move_to_element(col).perform()

                # Sử dụng WebDriverWait để đợi phần tử có thể truy cập
                text = WebDriverWait(driver, 10).until(EC.visibility_of(col)).text
                data_row[f'col_{i+1}'] = text
                data_row.append(text)
            except Exception as e:
                print(f"Error accessing column: {e}")
                data_row.append("")
        
        # Ghi dữ liệu của hàng vào tệp CSV
        csvwriter.writerow(data_row)

        # After processing all columns in the row
        demstt += 1
       

time.sleep(30)

# Close the browser
driver.quit()