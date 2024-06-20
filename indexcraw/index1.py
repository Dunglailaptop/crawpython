# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# import requests

# # Set the path to the Chrome WebDriver executable
# chrome_driver_path = "chromedriver.exe"

# # Initialize the Chrome service with the correct path to Chrome executable
# service = Service(executable_path=chrome_driver_path)

# # Initialize the Chrome WebDriver with the service
# driver = webdriver.Chrome(service=service)

# # Open the desired URL
# driver.get("https://www.thegioididong.com")
# driver.maximize_window()

# # Find an element by class name
# input_element = driver.find_element(By.CLASS_NAME, "item-img")
# input_img = input_element.find_element(By.TAG_NAME,"img")
# linkimage = input_img.get_attribute("src")

# # Let's just print out the element's HTML to verify we've found the correct element
# print(linkimage)

# # Open a new tab
# driver.execute_script("window.open('about:blank', '_blank');")

# # Switch to the new tab
# driver.switch_to.window(driver.window_handles[1])

# # Open the image URL in the new tab
# driver.get(linkimage)

# # Download and save the image
# driver.save_screenshot("sreenshot.png")
# # Wait for 10 seconds (just for demonstration purposes)
# time.sleep(10)

# # Quit the WebDriver session
# driver.quit()

import json

# Mảng chứa các tên biến
keys = ["name", "age", "city"]

# Mảng chứa các giá trị tương ứng
values = ["Alice", 25, "New York"]

# Tạo một dictionary với các khóa từ mảng keys và giá trị từ mảng values
object_dict = {key: value for key, value in zip(keys, values)}

# Ghi JSON vào một tệp
with open('object_data.json', 'w') as json_file:
    json.dump(object_dict, json_file, indent=4)

print("Dữ liệu đã được ghi vào file object_data.json")


