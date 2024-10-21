import customtkinter
import os
import tkinter as tk
import sourceString as sour
from tkinter import Menu
from PIL import ImageTk, Image

def open_prescriptionDetail():
    app.withdraw()
    import mainPrescriptionDetail as prescriptiondetail
    prescriptiondetail.settupAppBeginStart(app)




def center_window(window,width=600,height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x=(screen_width / 2) - (width / 2)
    y=(screen_height / 2 ) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


app = customtkinter.CTk()
app.title("Lấy dữ liệu khám chưa bệnh")
center_window(app)
icon_path = sour.CONFIG_PATH_ICON_APP
app.iconbitmap(icon_path)

menu_bar = Menu(app)
app.config(menu=menu_bar)

prescription_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Lấy dữ liệu chi tiết đơn thuốc",menu=prescription_menu)
prescription_menu.add_command(label="Thực thi dữ liệu chi tiết đơn thuốc",command=open_prescriptionDetail)

imgBG = ImageTk.PhotoImage(Image.open(sour.CONFIG_PATH_IMAGE_BACKGROUND_APP))
l1 = customtkinter.CTkLabel(master=app, image=imgBG)
l1.pack()

frame = customtkinter.CTkFrame(master=l1, width=320, height=300, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Select configuration", font=('Century Gothic', 20))
l2.place(x=70, y=45)

def on_closing():
    app.quit()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

    
