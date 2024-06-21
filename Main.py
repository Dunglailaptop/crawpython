# main.py

import tkinter as tk
from Model.ModelTest import Model
from VIew.MainView import View
from Presenter.ActionPresenter import Presenter

def main():
    root = tk.Tk()
    model = Model()
    view = View(root)
   
    presenter = Presenter(model, view)
    presenter.ActionLogin()
    root.mainloop()
    

if __name__ == "__main__":
    main()
