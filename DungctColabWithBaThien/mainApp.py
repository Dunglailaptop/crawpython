import customtkinter
import os
import tkinter as tk
import sourceString as sour
from tkinter import Menu
from PIL import ImageTk, Image
from tkinter import ttk

def open_prescriptionDetail(new_tab):
    import mainPrescriptionDetail as prescriptiondetail
    prescriptiondetail.settupAppBeginStart(new_tab)

def open_invoiceoutpatientDetail(new_tab):
    import mainInvoiceoutpatientDetail as invoiceoutpatientDetail
    invoiceoutpatientDetail.settupAppBeginStart(new_tab)



def center_window(window,width=600,height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x=(screen_width / 2) - (width / 2)
    y=(screen_height / 2 ) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# Function to create and manage tabs, ensuring each button can only create one tab
# Function to create a tab with a close 'X' and embed a sub-application (frame)
def create_tab_with_content(tab_name, content_type):
    if tab_name not in created_tabs:
        # Create a new tab frame with fixed size
        new_tab = ttk.Frame(notebook, width=500, height=400)
        
        # Add the tab with a close button (X)
        notebook.add(new_tab, text=f"{tab_name} ✖")
        
        # Store the tab in the dictionary
        created_tabs[tab_name] = new_tab
        
        # Embed sub-application or content in the tab based on button clicked
        if content_type == "App1":
            open_prescriptionDetail(new_tab)
        elif content_type == "App2":
            open_invoiceoutpatientDetail(new_tab)
        elif content_type == "App3":
            # Another different layout or content
            app_label = tk.Label(master=new_tab, text="This is the content of App 3", font=("Arial", 16))
            app_label.pack(pady=20)
            listbox = tk.Listbox(new_tab)
            for item in ["Option 1", "Option 2", "Option 3"]:
                listbox.insert(tk.END, item)
            listbox.pack(pady=10)

        # Select the newly created tab
        notebook.select(new_tab)

# Function to detect which tab is clicked and close it if 'X' is clicked
def close_tab(event):
    # Get the index of the currently selected tab
    clicked_tab = notebook.index(notebook.select())
    tab_text = notebook.tab(clicked_tab, "text")
    
    # Check if the clicked part of the tab text is the 'X' (last character)
    if tab_text[-1] == '✖':
        notebook.forget(clicked_tab)  # Close the tab

        # Remove the tab from the created_tabs dictionary
        tab_name = tab_text[:-2]  # Extract the tab name without ' ✖'
        if tab_name in created_tabs:
            del created_tabs[tab_name]

app = customtkinter.CTk()
app.title("Lấy dữ liệu khám chưa bệnh")
center_window(app)
icon_path = sour.CONFIG_PATH_ICON_APP
app.iconbitmap(icon_path)

menu_bar = Menu(app)
app.config(menu=menu_bar)

prescription_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Lấy dữ liệu chi tiết đơn thuốc",menu=prescription_menu)
prescription_menu.add_command(label="Thực thi dữ liệu chi tiết đơn thuốc",command=lambda:  create_tab_with_content("Chi Tiết đơn thuốc", "App1"))
prescription_menu.add_command(label="Thực thi dữ liệu khám bệnh ngoại trú",command=lambda:  create_tab_with_content("Khám Ngoại trú", "App2"))
prescription_menu.add_command(label="Thực thi dữ liệu khám bệnh nội trú",command=lambda:  create_tab_with_content("Khám bệnh nội trú", "App3"))

# Create a Notebook widget (tab container)
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both")
created_tabs = {}

# Bind the event to detect tab clicks and close tabs
# notebook.bind("<Button-1>", close_tab)

def on_closing():
    app.quit()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

    
