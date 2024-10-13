import psycopg2
import sourceString as sour
import tkinter as tk
import time
import threading
import os
import json
import requests

app = sour.Any
#hàm chạy chính các sự kiện main
def run_script():
    global app
    print("...........khởi động chương trình...........")
    print("...........Khởi động chomre.................")
    bTry = False
    errorChrome = 1
    while bTry == False:
          bTry = sour._initSelenium_()
          if bTry == False:
             if errorChrome >= 10:
                 print(".......khởi động chrome thất bại quá nhiều lần! tắt chương trình.......")
                 app.destroy()
             else:
                 errorChrome += 1
                 print("....khởi động chomre thất bại thử lại lần nữa.......")
    time.sleep(3)
    print("........Duyệt website thành công.........")
    sour._login_("quyen.ngoq", "74777477")
     # ấn nút login
    time.sleep(0.5)
    print(".........................Sao chép userkey thành công.....................................")
    headers = {
                    "Appkey": sour.Appkey,
                    "Userkey": sour.secretKey,
                    "Authorization": sour.secretKey,
                    "Content-Type": sour.contentType
                }
    print(".........................Đang tiến hành thu thập! Vui lòng chờ...........................")
    loading = True
    def loading_animation():
        chars = "/—\\|"
        i = 0
        while loading:
            print('\r' + 'Vui lòng đợi quá trình tải dữ liệu đang được diễn ra... ' + chars[i % len(chars)])
            time.sleep(0.1)
            i += 1
      # Thread cho animation
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
    # Bắt đầu animation
    loading_thread.start()
    # Biến global để kiểm soát animation
    try:
        get_list_data_prescription()
    finally:
        loading = False
        loading_thread.join()
    sour._destroySelenium_()
    app.deiconify()

def load_config():
    if os.path.exists('prescriptionDetail.json'):
        with open('prescriptionDetail.json','r') as f:
            return json.load(f)
    return {"page_value":"1","record_value":"0"}

def save_config(config):
    with open('prescriptionDetail.json', 'w') as f:
        json.dump(config, f)

def update_file_json(l4_value, l6_value):
    config = load_config()
    config['page_value'] = l4_value
    config['record_value'] = l6_value
    save_config(config)

#hàm lấy dự liệu lên từ database của bảng prescription
def get_list_data_prescription(header):
    config = load_config()
    page_value =config["page_value"]
    record_value = config["record_value"]
    while(True):
        try:
            conn_params = sour.ConnectStr
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            queryStr = f"SELECT * FROM prescription order by stt asc OFFSET {record_value} LIMIT 20;"
            cur.execute(queryStr)
            listdata = cur.fetchall()
            if len(listdata) > 0 :
                for item in listdata:
                    prescription_id = item[54]
                    payload = {
                         "prescription_id": prescription_id
                    }
                    responseChiTietToaThuoc = requests.get(sour.urlGetPrescriptiondetail, headers=header,json=payload)
                    if responseChiTietToaThuoc.status_code == 200:
                        dataTT = responseChiTietToaThuoc.json()
                        try:
                            data = dataTT['data']
                            if len(data) > 0:
                                print("vo ne")
                                #hamm them du lieu vao database postgresql
                        except Exception as e:
                            print(f"loi khi them du lieu vao database......")
                    else:
                        print(f"loi khi lay du lieu chi tiet toa thuoc" + str(e))
                p = page_value + 1
                pSub = p - 1
                rc = pSub * 20 - 1
                update_file_json(l4_value=p, l6_value=rc)
                page_value = p
                record_value = rc
        except Exception as e:
           print("Lỗi xảy ra trong quá trình truy cập CSDL... : "+ str(e))                  
        finally:
            if conn:
                 cur.close()
                 conn.close()

            
# Gọi hàm để chạy truy vấn

