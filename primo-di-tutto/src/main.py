#!/usr/bin/python3

import os
import sys
import fcntl
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from resorcess import *
from apt_manage import *
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
from logger_config import setup_logger

logger = setup_logger(__name__)



def check_single_instance():
    """Check if another instance of the application is already running"""
    lock_file = "/tmp/primo-di-tutto.lock"
    
    try:
        # Try to open the lock file
        lock_fd = open(lock_file, 'w')
        
        # Try to acquire an exclusive lock
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        # Write the current PID to the lock file
        lock_fd.write(str(os.getpid()))
        lock_fd.flush()
        
        # Return the file descriptor to keep it open
        return lock_fd
        
    except (IOError, OSError):
        # Another instance is already running
        print("Another instance of Primo is already running.")
        sys.exit(1)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__(className="Primo")
        self.title("Primo | GuideOS Einstellungen")
        self.resizable(False, False)
        dpi = self.winfo_fpixels('1i')
        print("DPI:", dpi)
        self.tk.call('tk', 'scaling',1.0)

        self.tk.call("source", TCL_THEME_FILE_PATH)
        app_width = 1200
        app_height = 750
        # Define Screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        # self.icon is still needed for some DEs
        self.icon = tk.PhotoImage(
            file=f"/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png"
        )
        self.tk.call("wm", "iconphoto", self._w, self.icon)
        self.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

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
        self.notebook.add(self.update_tab, compound=LEFT, text="Aktualisierungen")
        self.notebook.add(
            self.software_tab, compound=LEFT, text="Software-\nEmpfehlungen"
        )
        self.notebook.add(self.system_tab, compound=LEFT, text="Werkzeuge")
        self.notebook.add(
            self.expert_tools_tab, compound=LEFT, text="Admin"
        )
        self.notebook.add(self.look_tab, compound=LEFT, text="Erscheinungsbild")
        self.notebook.add(self.large_folders, compound=LEFT, text="Speicherfresser")
        self.notebook.add(self.links_tab, compound=LEFT, text="Links")
        self.notebook.add(self.contrib_tab, compound=LEFT, text="Mitmachen")

        def notebook_styler():
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
                width=18,
                highlightthickness=0,
            )

            noteStyler.configure("TButton", justify="left", anchor="w")

            noteStyler.configure("Custom.TButton", justify="center", anchor="center")
            noteStyler.configure("Accent2.TButton", justify="center", anchor="center")

        notebook_styler()


if __name__ == "__main__":
    # Check for single instance before creating the application
    lock_fd = check_single_instance()
    
    try:
        app = MainApplication()
        app.mainloop()
    finally:
        # Clean up the lock file when the application exits
        if lock_fd:
            lock_fd.close()
            try:
                os.remove("/tmp/primo-di-tutto.lock")
            except OSError:
                pass
