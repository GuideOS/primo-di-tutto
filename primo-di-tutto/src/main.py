#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.welcome_tab import WelcomeTab
from tabs.dash_tab import DashTab
from tabs.update_tab import UpdateTab
from tabs.system_tab import SystemTab
from tabs.look_tab import LookTab
from tabs.software_tab import *
from tabs.contrib_tab import ContribTab
from tabs.expert_tools import ExpertTab
from tabs.links_tab import LinksTab
from tabs.large_folders_tab import LargeFoldersTab
from azure_ttk import *
from utils import scaling  # Import the scaling variable
from logger_config import setup_logger

logger = setup_logger(__name__)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__(className="Primo")
        self.title("Primo | GuideOS Einstellungen")
        self.resizable(False, False)
        self.tk.call("source", TCL_THEME_FILE_PATH)
        self.tk.call('tk', 'scaling', scaling)

        # self["background"] = maincolor
        app_width = 1200
        app_height = 750
        # Define Screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        #x = (screen_width / 2) - (app_width / 2)
        #y = (screen_height / 2) - (app_height / 2)

        # self.icon is still needed for some DEs
        self.icon = tk.PhotoImage(
            file=f"/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png"
        )
        self.tk.call("wm", "iconphoto", self._w, self.icon)
        self.geometry(f"{app_width}x{app_height}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Notebook Icons
        logger.info(theme_name)
        if "dark" in theme_name or "Dark" in theme_name:
            self.tk.call("set_theme", "dark")
        else:
            self.tk.call("set_theme", "light")


        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.willkommen_tab = WelcomeTab(self.notebook)
        self.dash_tab = DashTab(self.notebook)
        self.update_tab = UpdateTab(self.notebook)
        self.software_tab = SoftwareTab(self.notebook)
        self.system_tab = SystemTab(self.notebook)
        self.expert_tools_tab = ExpertTab(self.notebook)
        self.look_tab = LookTab(self.notebook)
        self.large_folders = LargeFoldersTab(self.notebook)
        self.links_tab = LinksTab(self.notebook)
        self.contrib_tab = ContribTab(self.notebook)

        if get_first_run() == "yes":
            self.notebook.add(self.willkommen_tab, compound=LEFT, text="Willkommen")

        self.notebook.add(self.dash_tab, compound=LEFT, text="Übersicht")
        self.notebook.add(self.update_tab, compound=LEFT, text="Aktualisierung")
        self.notebook.add(self.software_tab, compound=LEFT, text="Software-\nEmpfehlungen")
        self.notebook.add(self.system_tab, compound=LEFT, text="Werkzeuge")
        self.notebook.add(
            self.expert_tools_tab, compound=LEFT, text="Expertenwerkzeuge"
        )
        self.notebook.add(self.look_tab, compound=LEFT, text="Erscheinungsbild")
        self.notebook.add(self.large_folders, compound=LEFT, text="Speicherfresser")
        self.notebook.add(self.links_tab, compound=LEFT, text="Links")
        self.notebook.add(self.contrib_tab, compound=LEFT, text="Mitmachen")

        # Notebook Theming
        global noteStyler
        noteStyler = ttk.Style(self)
        noteStyler.configure(
            "TNotebook",
            borderwidth=0,
            tabposition="w",
            highlightthickness=0,
        )
        noteStyler.configure(
            "TNotebook.Tab",
            borderwidth=0,
            font=font_10,
            width=18,
            highlightthickness=0,
        )

        noteStyler.configure("TButton", justify="left", anchor="w")

        noteStyler.configure("Custom.TButton", justify="center", anchor="center")
        noteStyler.configure(
            "Accent2.TButton", justify="center", anchor="center", font=font_12
        )


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
