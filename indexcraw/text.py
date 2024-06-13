import csv
from bs4 import BeautifulSoup

# Đọc nội dung từ tệp HTML
with open('D:/USER DATA/Documents/data_tailieudinhkiem/dataBenhNhan.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Phân tích cú pháp HTML bằng BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Mở tệp CSV để ghi dữ liệu
with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Giả sử 'tbodys' là danh sách các phần tử tbody lấy từ trang web
    tbodys = soup.find_all('tbody')

    # Khởi tạo 'rows' từ phần tử tbody đầu tiên
    rows = tbodys[0].find_all('tr')
    demstt = 1
    breakSTT = 1

    for row in rows:
        # Lấy tất cả các cột trong hàng hiện tại
        cols = row.find_all('td')
        # Loại bỏ cột đầu tiên
        cols2 = cols[1:]

        data_row = []
        for col in cols2:
            try:
                text = col.get_text(strip=True)
                data_row.append(text)
            except Exception as e:
                print(f"Error accessing column: {e}")
                data_row.append("")

        # Ghi dữ liệu của hàng vào tệp CSV
        csvwriter.writerow(data_row)
