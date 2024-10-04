import tkinter as tk
from tkinter import ttk

class SimpleWindow:
    def __init__(self, title="First Run Wizard", size="900x600"):
        self.main = tk.Tk()
        self.main.title(title)
        self.main.geometry(size)
        self.style = ttk.Style()
        tk.call('source', r'/home/timo/Github/pguides_gui/Azure-ttk-theme-2.1.0/theme\dark.tcl')
        tk.call('source', r'/home/timo/Github/pguides_gui/Azure-ttk-theme-2.1.0\azure.tcl')
        self.theme_use('azure')

        #self.Styler = ttk.Style()
        #self.Styler.theme_use('')        

        self.sidebar = tk.Frame(self.main, background="cyan",padx=20)
        self.sidebar.pack(side="left", fill="y",expand="true",anchor="w")

        self.label = ttk.Label(self.sidebar, text="Willkommen auf\nProject Guide OS", background="cyan")
        self.label.pack(pady=20)

        self.content = ttk.Frame(self.main)
        self.content.pack(side="left", fill="y",expand="true")

        # Erstelle einen Label
        self.label = ttk.Label(self.content, text="Triff deine Software-Auswahl")
        self.label.pack(pady=20,fill="y")

        self.Buero = ttk.LabelFrame(self.content,text="Büro")
        self.Buero.pack(fill="both",expand="true")

        self.first_button = ttk.Button(self.Buero,text="LibreOffice")
        self.first_button.grid(row=0,column=0)







# Hauptprogramm
if __name__ == "__main__":
    window = SimpleWindow()
    window.run()
