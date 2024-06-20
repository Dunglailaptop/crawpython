# view.py
from tkinter import messagebox
import tkinter as tk

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter MVP Example")

        # Đặt kích thước cho cửa sổ
        window_width = 400
        window_height = 300

        # Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Tính toán vị trí để cửa sổ nằm giữa màn hình
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Đặt kích thước và vị trí cho cửa sổ
        self.root.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')

        self.label = tk.Label(root, text="hello con ket")
        self.label.pack()
        # Tạo TextBox
        text_box = tk.Text(root, height=5, width=30)
        text_box.pack(pady=10)

        # Định nghĩa thuộc tính on_update_button_clicked trước khi sử dụng
        self.on_update_button_clicked = None

        self.update_button = tk.Button(root, text="Update")
        self.update_button.pack()

    def set_label_text(self, text):
        self.label.config(text=text)

    def bind_update_button(self, callback):
        self.get_textbox_data = callback

    def handle_update_button_clicked(self):
        if self.on_update_button_clicked:
           self.on_update_button_clicked()
     
    
    def get_textbox_data(self):
        messgae = self.text_box.get("1.0", tk.END).strip()
        messagebox.showinfo("Thông tin nhập", messgae)