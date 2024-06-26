from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
    # Initialize ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
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

    return driver


# Function to select area data
def select_area_data(driver, url):
    driver.get(url)
    time.sleep(2)


# Function to extract header data
def extract_header_data(driver):
    listbody_div_header = driver.find_element(By.ID, "lstMain-head")
    table_header = listbody_div_header.find_element(By.TAG_NAME, 'table')
    tbody_header = table_header.find_elements(By.TAG_NAME, "tbody")
    rows = tbody_header[0].find_elements(By.TAG_NAME, "tr")
    data_header = [col.text for row in rows for col in row.find_elements(By.TAG_NAME, "th")[1:]]
    return data_header


# Function to extract table data and save to CSV and JSON
def extract_and_save_table_data(driver, data_header, csv_filename, json_filename):
    listbody_div = driver.find_element(By.ID, 'lstMain-body')
    table = listbody_div.find_element(By.TAG_NAME, 'table')
    tbodys = table.find_elements(By.TAG_NAME, "tbody")
    rows = tbodys[1].find_elements(By.TAG_NAME, 'tr')

    data_array_all = []

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
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
            data_array_all.append(data_row)

    object_array = [{key: value for key, value in zip(data_header, data_row)} for data_row in data_array_all]

    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(object_array, json_file, ensure_ascii=False, indent=4)


# Main function to run the script
def main():
    chromedriver_path = "chromedriver.exe"  # Ensure this path is correct
    login_url = "http://192.168.0.65:8180/"
    area_data_url = "http://192.168.0.65:8180/#menu=58&action=180"
    username = "quyen.ngoq"
    password = "74777477"
    csv_filename = 'dataLuotSuIn.csv'
    json_filename = 'dataJsonLuotSuIn.json'

    # Initialize and log into the system
    driver = login(chromedriver_path, login_url, username, password)

    # Select area data
    select_area_data(driver, area_data_url)

    # Extract header data
    data_header = extract_header_data(driver)
    print(data_header)

    # Extract table data and save to CSV and JSON
    extract_and_save_table_data(driver, data_header, csv_filename, json_filename)

    # Wait for a while before closing the browser
    time.sleep(10)

    # Close the browser
    driver.quit()

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




def khoitaoapp():
    root = Tk()
    root.title("Tkinter ComboBox Example")
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
    # Function to handle selection event
    def on_select(event):
         selected_item = combo.get()
         selected_number = item_to_number.get(selected_item, None)
         if selected_number is not None:
          print(f"Selected number: {selected_number}")
          main()
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

    # Start the Tkinter event loop
    root.mainloop()



# Run the main function
if __name__ == "__main__":
    khoitaoapp()
