import tkinter as tk
from tkinter import ttk

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
            # Simulate embedding an application window with widgets (e.g., a small app layout)
            app_label = tk.Label(new_tab, text="This is the content of App 1", font=("Arial", 16))
            app_label.pack(pady=20)
            entry = tk.Entry(new_tab)
            entry.pack(pady=10)
        elif content_type == "App2":
            # Another example of embedding different content in the tab
            app_label = tk.Label(new_tab, text="This is the content of App 2", font=("Arial", 16))
            app_label.pack(pady=20)
            button = tk.Button(new_tab, text="Click me")
            button.pack(pady=10)
        elif content_type == "App3":
            # Another different layout or content
            app_label = tk.Label(new_tab, text="This is the content of App 3", font=("Arial", 16))
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

# Initialize the main application window
app = tk.Tk()
app.title("Tab with Embedded Window Example")
app.geometry("600x500")  # Set fixed size for the main app window

# Create a Notebook widget (tab container)
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both")

# Dictionary to track created tabs
created_tabs = {}

# Create a frame to hold the buttons at the top
button_frame = tk.Frame(app)
button_frame.pack(side="top", pady=10)

# Create buttons for adding tabs and embedding app windows
buttons = {
    "Tab 1": tk.Button(button_frame, text="Open Tab 1 with App1", command=lambda: create_tab_with_content("Tab 1", "App1")),
    "Tab 2": tk.Button(button_frame, text="Open Tab 2 with App2", command=lambda: create_tab_with_content("Tab 2", "App2")),
    "Tab 3": tk.Button(button_frame, text="Open Tab 3 with App3", command=lambda: create_tab_with_content("Tab 3", "App3"))
}

# Pack the buttons at the top
for button in buttons.values():
    button.pack(side="left", padx=5)

# Bind the event to detect tab clicks and close tabs
notebook.bind("<Button-1>", close_tab)

# Start the application
app.mainloop()
