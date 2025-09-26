#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from resorcess import application_path
from logger_config import setup_logger

logger = setup_logger(__name__)


class Done_(tk.Toplevel):
    """custom messagebox"""

    def __init__(self, parent):
        super().__init__(parent)
        # self["background"] = maincolor
        self.title("Erledigt!")
        self.icon = tk.PhotoImage(file=f"{application_path}/images/icons/logo.png")
        self.tk.call("wm", "iconphoto", self._w, self.icon)
        self.resizable(0, 0)
        app_width = 292
        app_height = 120
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

        cont_btn = ttk.Button(
            self, text="Ok", command=self.destroy, style="Accent.TButton"
        )
        cont_btn.pack(fill="x", expand=True, pady=20, padx=20)
