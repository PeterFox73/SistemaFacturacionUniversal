import tkinter as tk
from tkinter import ttk
from gui import GUI
from database import Database

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Inventarios")
        self.db = Database("inventario.db")
        self.gui = GUI(self.root, self.db)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()