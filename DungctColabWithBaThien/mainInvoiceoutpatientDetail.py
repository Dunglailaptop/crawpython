import psycopg2
import sourceString as sour
import tkinter as tk
import time
import threading
import os
import json
import logging
import requests
import customtkinter
from tkinter import messagebox
from psycopg2 import sql
from PIL import ImageTk, Image
from tkinter import Menu
from typing import List, Dict, Any

app = sour.Any
terminal_window = Any
terminal_text = Any
script_thread = Any
def log_terminal(message):
        global terminal_text
        terminal_text.insert(tk.END,message + "\n")
        terminal_text.see(tk.END)  # Scroll to the end
        terminal_text.update_idletasks()
#hàm chạy chính các sự kiện main
def run_script(terminaltext):
    global terminal_window, terminal_text
    sour.terminal_destroy = terminal_window
    terminal_text = terminaltext
    log_terminal("...........chay con server 80...............")
    log_terminal("...........khởi động chương trình...........")
    log_terminal("...........Khởi động chomre.................")
    bTry = False
    errorChrome = 1
    while bTry == False:
          bTry = sour._initSelenium_2()
          if bTry == False:
             if errorChrome >= 10:
                 log_terminal(".......khởi động chrome thất bại quá nhiều lần! tắt chương trình.......")
                 terminal_window.destroy()
                #  app.destroy()
             else:
                 errorChrome += 1
                 log_terminal("....khởi động chomre thất bại thử lại lần nữa.......")
    time.sleep(3)
    log_terminal("........Duyệt website thành công.........")
    sour._login_2("quyen.ngoq", "74777477")
     # ấn nút login
    time.sleep(0.5)
    log_terminal(".........................Sao chép userkey thành công.....................................")
    headers = {
                    "Appkey": sour.Appkey2,
                    "Userkey": sour.secretKey2,
                    "Authorization": sour.secretKey2,
                    "Content-Type": sour.contentType
                }
    log_terminal(".........................Đang tiến hành thu thập! Vui lòng chờ...........................")
    loading = True
    def loading_animation():
        chars = "/—\\|"
        i = 0
        while loading:
            log_terminal('\r' + 'Vui lòng đợi quá trình tải dữ liệu đang được diễn ra... ' + chars[i % len(chars)])
            time.sleep(0.1)
            i += 1
      # Thread cho animation
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
    # Bắt đầu animation
    loading_thread.start()
    # Biến global để kiểm soát animation
    try:
        get_list_data_prescription(headers) 
        if checkvalue:
           print("đóng kết nối chi tiết hóa đơn khám ngoại trú")
        else:
           messagebox.showinfo(title="Thành công!",message="Hoàn thành cào dữ liệu bệnh nhân! Kết nối PostgreSQL đã đóng!.....")
    finally:
        loading = False
        loading_thread.join()
    sour._destroySelenium_2()
    # terminal_window.destroy()
    # app.deiconify()

def load_config():
    if os.path.exists(sour.CONFIG_PATH_INVOICEOUTPATIENTDETAIL):
        with open(sour.CONFIG_PATH_INVOICEOUTPATIENTDETAIL,'r') as f:
            return json.load(f)
    return {"page_value":"1","record_value":"0"}

def save_config(config):
    with open(sour.CONFIG_PATH_INVOICEOUTPATIENTDETAIL, 'w') as f:
        json.dump(config, f)

def update_file_json(l4_value, l6_value):
    config = load_config()
    config['page_value'] = l4_value
    config['record_value'] = l6_value
    save_config(config)
   
def replace_nulls_with_string(data):
    if isinstance(data, dict):
        # Xử lý dictionary
        for key, value in data.items():
            if value is None:
                data[key] = "None"
    elif isinstance(data, list):
        # Xử lý list chứa dictionary hoặc tuple
        for i in range(len(data)):
            if isinstance(data[i], dict):
                # Nếu phần tử là dictionary, xử lý như dictionary
                data[i] = replace_nulls_with_string(data[i])
            elif isinstance(data[i], tuple):
                # Nếu phần tử là tuple, xử lý từng giá trị trong tuple
                data[i] = tuple("None" if v is None else v for v in data[i])
    elif isinstance(data, tuple):
        # Xử lý trực tiếp tuple
        return tuple("None" if v is None else v for v in data)
    return data


# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_detail_invoice(datalist: List[Dict[str, Any]]):
    conn_params = sour.ConnectStr
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        if len(datalist) > 0:
            for index, d in enumerate(datalist, start=1):
                try:
                    # Chuẩn bị dữ liệu cho invoice_outpatient_detail
                    invoice_detail_data = (
                        d["total"], d["pay_payment_item_id"], d["pay_receipt_id"],
                        d["patient_id"], d["created_time"], d["cashier_id"],
                        d["amount"], d["discount_amount"], d["discount_enum_unit"],
                        d["note"], d["invoice_code"], d["partner_invoice_code"],
                        d["cashier_name"], d["enum_payment_type"], d["pay_payment_account_id"],
                        d["enum_invoice_type"], d["total_price"], d["ins_paid_price"],
                        d["patient_price"], d["branch_id"], d["counter_id"],
                        d["enum_re_exam_type"], d["total_returned_amount"], d["returned"],
                        d["new_pay_receipt_id"], d["new_invoice_code"], d["refund_invoice_code"],
                        d["refund_pay_receipt_id"], d["refund_date"], d["bhbl_url"],
                        d["change_note"], d["deleted"], d["audi_last_modified_user_id"],
                        d["audi_last_modified_time"], d["refund_amount"], d["so_luu_tru"],
                        d["phai_thu"], d["phai_tra"], d["da_thu"], d["ngay_thu"],
                        d["nguoi_thu"], d["is_ngoai_quy_ds"], d["company_name"],
                        d["company_id"], d["so_hd"], d["hd_date"], d["transfer_date"],
                        d["bank_transaction_log_id"], d["icd10"], d["e_invoice_status"],
                        d["e_invoice_id"], d["ins_send_status"], d["ins_transaction_code"],
                        d["hd_info"], d["retail_patient_name"], d["retail_patient_address"],
                        d["tam_ung"], d["tochuc_quy"], d["total_dichvu"], 
                        d["total_nutrition"], d["percent_fee"], d["zone"], d["shift"],
                        d["is_inventory"], d["reason_decline"], d["user_id_decline"],
                        d["time_decline"], d["unit"], d["code"], d["unit_price"],
                        d["quantity"], d["insurance_name"], d["enum_item_type"],
                        d["service_name"], d["register_date"], d["doctor_name"],
                        d["item_type"], d["service_id"]
                    )

                    # Sử dụng sql.SQL để tránh SQL injection
                    insert_query = sql.SQL("""
                        INSERT INTO InvoicesoutpatientDetail (
                            total, pay_payment_item_id, pay_receipt_id, patient_id,
                            created_time, cashier_id, amount, discount_amount,
                            discount_enum_unit, note, invoice_code, partner_invoice_code,
                            cashier_name, enum_payment_type, pay_payment_account_id,
                            enum_invoice_type, total_price, ins_paid_price, patient_price,
                            branch_id, counter_id, enum_re_exam_type, total_returned_amount,
                            returned, new_pay_receipt_id, new_invoice_code, refund_invoice_code,
                            refund_pay_receipt_id, refund_date, bhbl_url, change_note,
                            deleted, audi_last_modified_user_id, audi_last_modified_time,
                            refund_amount, so_luu_tru, phai_thu, phai_tra, da_thu,
                            ngay_thu, nguoi_thu, is_ngoai_quy_ds, company_name, company_id,
                            so_hd, hd_date, transfer_date, bank_transaction_log_id, icd10,
                            e_invoice_status, e_invoice_id, ins_send_status, ins_transaction_code,
                            hd_info, retail_patient_name, retail_patient_address, tam_ung,
                            tochuc_quy, total_dichvu, total_nutrition, percent_fee, zone,
                            shift, is_inventory, reason_decline, user_id_decline, time_decline,
                            unit, code, unit_price, quantity, insurance_name, enum_item_type,
                            service_name, register_date, doctor_name, item_type, service_id
                        )
                        VALUES ({})
                    """).format(
                        sql.SQL(', ').join([sql.Placeholder()] * len(invoice_detail_data))
                    )

                    cur.execute(insert_query, invoice_detail_data)
                    conn.commit()
                    logging.info(f"Bản ghi thứ {index} đã được chèn thành công")
                    log_terminal(f"Bản ghi thứ {index} đã được chèn thành công")

                except Exception as e:
                    conn.rollback()
                    logging.error(f"Lỗi khi chèn bản ghi thứ {index}: {e}")

    except psycopg2.Error as e:
        logging.error(f"Lỗi kết nối database: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        logging.info("Kết nối database đã đóng")

#rx
checkvalue = False
def check_value_update(new_value):
    global checkvalue
    print(f"Giá trị checkvalue vừa được cập nhật: {new_value}")
    checkvalue = new_value
       

# Đăng ký (subscribe) vào stream để theo dõi thay đổi của checkvalue
sour.checkvalue_subject_invoicepatientdetail.subscribe(check_value_update)

#hàm lấy dự liệu lên từ database của bảng prescription
def get_list_data_prescription(header):
    config = load_config()
    page_value =config["page_value"]
    record_value = config["record_value"]
    while(True):
        if checkvalue:
            break
        try:
            conn_params = sour.ConnectStr
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            queryStr = f"SELECT * FROM invoiceoutpatient order by stt asc OFFSET {record_value} LIMIT 20;"
            cur.execute(queryStr)
            listdata = cur.fetchall()
            if len(listdata) > 0 :
                for item in listdata:
                    invoice_code = item[13]
                    pay_receipt_id = item[19]
                    patien_id = item[29]
                    payload = {
                         "invoice_code": invoice_code,
                         "pay_receipt_id": pay_receipt_id,
                         "patient_id": patien_id
                    }
                    responseChiTietToaThuoc = requests.get(sour.urlGetinvoiceoutdetail, headers=header,json=payload)
                    if responseChiTietToaThuoc.status_code == 200:
                        dataTT = responseChiTietToaThuoc.json()
                        try:
                            data = dataTT['data']
                            if len(data) > 0:
                                log_terminal("......BẮT ĐẦU GHI DATA VÔ NHA......")
                                add_detail_invoice(data)
                                #hamm them du lieu vao database postgresql
                        except Exception as e:
                            print(f"loi khi them du lieu vao database......")
                    else:
                        print(f"loi khi lay du lieu chi tiet toa thuoc" + str(e))
                p = int(page_value) + 1
                pSub = p - 1
                rc = pSub * 20 - 1
                update_file_json(l4_value=p, l6_value=rc)
                page_value = p
                record_value = rc
                log_terminal(f"tổng page vlaue/record value:{page_value}/{record_value}")
            else:
                break
        except Exception as e:
           print("Lỗi xảy ra trong quá trình truy cập CSDL... : "+ str(e))                  
        finally:
            if conn:
                 cur.close()
                 conn.close()




    
# Function to open a terminal window embedded in the tab
def open_terminal_window(new_tab):
       # Clear any existing widgets in the tab
    for widget in new_tab.winfo_children():
        widget.destroy()
    terminal_window = tk.Frame(new_tab)
    terminal_window.pack(expand=True, fill="both")

    terminal_text = tk.Text(terminal_window, bg="black", fg="green", insertbackground="green")
    terminal_text.pack(expand=True, fill="both")
    
    return terminal_window, terminal_text

# Function to start the script in a separate thread
def start_script_thread(new_tab):
    global script_thread
    terminal_window, terminal_text = open_terminal_window(new_tab)
    script_thread = threading.Thread(target=run_script, args=(terminal_text,))
    script_thread.start()

# Function to set up the main application in the tab
def settupAppBeginStart(new_tab):
    # Set up the application inside the tab
    imgBG = ImageTk.PhotoImage(Image.open(sour.CONFIG_PATH_IMAGE_BACKGROUND_APP_3))  # Replace with your image path
    l1 = customtkinter.CTkLabel(master=new_tab, image=imgBG)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=320, height=250, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    run_button = customtkinter.CTkButton(master=frame, command=lambda: start_script_thread(new_tab),
                                         text="Thực thi", font=('Tahoma', 13), fg_color="#005369", hover_color="#008097")
    run_button.place(x=160, y=200)

    new_tab.mainloop()

# Gọi hàm để chạy truy vấn

