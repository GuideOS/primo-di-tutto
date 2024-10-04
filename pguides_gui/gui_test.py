from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# Klasse für die Hauptanwendung
class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test")
        self.create_widgets()




    def create_widgets(self):
        # Erstellt ein Notebook (Tab-Widget)
        self.notebook = ttk.Notebook(self.root)
        
        # Frame für den ersten Tab
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Willkommen")
        self.create_tab1_widgets()

        # Frame für den ersten Tab
        self.tab11 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab11, text="Einführung")
        self.create_tab11_widgets()

        # Frame für den ersten Tab
        self.tab12 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab12, text="Gaming")
        self.create_tab12_widgets()

        # Frame für den zweiten Tab
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Software")
        self.create_tab2_widgets()

        # Frame für den zweiten Tab
        self.tab22 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab22, text="Mitmachen")
        self.create_tab22_widgets()

        # Notebook packen
        self.notebook.pack(expand=True, fill="both")

    def create_tab1_widgets(self):
        # Widgets für den ersten Tab


        self.proton_icon = PhotoImage(
            file=f"/home/timo/Github/pguides_gui/proton_icon_36.png")
        self.system_icon = PhotoImage(
            file=f"/home/timo/Github/pguides_gui/test.png"
        )
        self.heroic_icon = PhotoImage(
            file=f"/home/timo/Github/pguides_gui/heroic_icon_36.png")
        self.steam_icon = PhotoImage(
            file=f"/home/timo/Github/pguides_gui/steam_icon_36.png")
        self.lutris_icon = PhotoImage(
            file=f"/home/timo/Github/pguides_gui/lutris_logo_36.png")

        label1 = ttk.Label(self.tab1, image=self.system_icon)
        label1.pack(pady=20)

        willko = """Schön das du dich für Project Guide OS entschieden hast. 
Wir wollen mit dieser Distribution .... ???? Bratwurst braten!"""

        button1 = ttk.Label(self.tab1, text=willko)
        button1.pack(pady=10)

    def create_tab11_widgets(self):
        # Widgets für den zweiten Tab
        label2 = ttk.Label(self.tab11, text="Das ist Tab 2")
        label2.pack()

        button2 = ttk.Button(self.tab11, text="Klick mich in Tab 2", command=lambda: self.on_button_click(2))
        button2.pack(pady=10)

    def create_tab12_widgets(self):
        # Widgets für den zweiten Tab
        game_lf = ttk.LabelFrame(self.tab12, text="Gaming Installer",padding=20)
        game_lf.pack(pady=20,padx=20,fill="x")

        label2 = ttk.Button(game_lf, text="Steam",compound=TOP, image=self.steam_icon)
        label2.grid(row=0,column=0)

        label2 = ttk.Button(game_lf, text="Lutris",image=self.lutris_icon,compound=TOP,)
        label2.grid(row=0,column=1,padx=5)

        label2 = ttk.Button(game_lf, text="Heroic",image=self.heroic_icon,compound=TOP,)
        label2.grid(row=0,column=2)

        label2 = ttk.Button(game_lf, text="ProtonUp-Qt",image=self.proton_icon,compound=TOP,)
        label2.grid(row=0,column=3,padx=5)

        game_tool_lf = ttk.LabelFrame(self.tab12, text="Gaming Installer",padding=20)
        game_tool_lf.pack(pady=20,padx=20,fill="both",expand=True)

        tool_name = ttk.Label(game_tool_lf, text="Name: Lutris",)
        tool_name.pack(pady=5,padx=10,fill="x")

        tool_format = ttk.Label(game_tool_lf, text="Paket: DEB",)
        tool_format.pack(pady=5,padx=10,fill="x")

        tool_descr = ttk.Label(game_tool_lf, text="Beschreinung:\n Dieser Installer stellt das Programm Lutris bereit und\ninstalliert alle nötigen Abhängikeiten z.B. Wine",)
        tool_descr.pack(pady=5,padx=10,fill="x")

        tool_descr = ttk.Button(game_tool_lf, text="Installieren",)
        tool_descr.pack(pady=5,padx=10,fill="x")

    def create_tab2_widgets(self):
        # Widgets für den zweiten Tab
        label2 = ttk.Label(self.tab2, text="Das ist Tab 2")
        label2.pack()

        button2 = ttk.Button(self.tab2, text="Klick mich in Tab 2", command=lambda: self.on_button_click(2))
        button2.pack(pady=10)

    def create_tab22_widgets(self):
        # Widgets für den zweiten Tab
        label2 = ttk.Label(self.tab22, text="Das ist Tab 2")
        label2.pack()

        button2 = ttk.Button(self.tab2, text="Klick mich in Tab 2", command=lambda: self.on_button_click(2))
        button2.pack(pady=10)

    def on_button_click(self, tab_number):
        # Reaktion auf den Button-Klick
        print(f"Button in Tab {tab_number} wurde gedrückt!")

# Startet die Anwendung
def main():
    root = tk.Tk()
    root.geometry("900x600")
    root.tk.call("source", "/home/timo/Github/pguides_gui/Azure-ttk-theme-2.1.0/azure.tcl")
    root.tk.call("set_theme", "dark")
    noteStyler = ttk.Style()
    noteStyler.configure(
    "TNotebook",
    borderwidth=0,
    tabposition="w",
    highlightthickness=0,)

    noteStyler.configure(
        "TNotebook.Tab",
        borderwidth=0,
        background="#ffffff",
        #foreground=main_font,
        font=("Sans",12),
        width=15,
        highlightthickness=0,
    )
    noteStyler.configure("TFrame")
    noteStyler.map(
        "TNotebook.Tab",
        background=[("selected", "#ffffff")],
        foreground=[("selected", "#ffffff")],
    )


    app = MyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

