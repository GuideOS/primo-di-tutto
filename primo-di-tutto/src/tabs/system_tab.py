#!/usr/bin/python3

import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.pop_ups import *
from tabs.system_tab_check import *
from tabs.system_dict_lib import SoftwareSys
from tool_tipps import CreateToolTip


class SystemTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.update_interval = 1000

        
        # Frame für Canvas und Scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True,padx=10, pady=20)

        # Canvas-Container für sys_btn_frame
        canvas = tk.Canvas(canvas_frame,borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y,padx=5)

        # Frame in den Canvas einfügen
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # sys_btn_frame in das scrollbare Frame einfügen
        sys_btn_frame = ttk.LabelFrame(scrollable_frame, text="Werkzeuge", padding=20)
        sys_btn_frame.pack(fill="both", expand=tk.TRUE)

        sys_btn_frame.grid_columnconfigure(0, weight=2)
        sys_btn_frame.grid_columnconfigure(1, weight=2)
        sys_btn_frame.grid_columnconfigure(2, weight=2)
        sys_btn_frame.grid_columnconfigure(3, weight=1)
        sys_btn_frame.grid_columnconfigure(4, weight=2)
 
        def sys_btn_action(sys_key):
            # SoftwareSys.sys_dict[sys_key]["Action"]
            command = SoftwareSys.sys_dict[sys_key]["Action"]
            print(command)
            os.popen(command)

        self.sys_btn_icons = []

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            icon = tk.PhotoImage(file=sys_info["Icon"])
            self.sys_btn_icons.append(icon)

        max_columns = 5

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            row = i // max_columns
            column = i % max_columns

            sys_button = ttk.Button(
                sys_btn_frame,
                text=sys_info["Name"],
                image=self.sys_btn_icons[i],
                command=lambda key=sys_key: sys_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19
            )
            sys_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_button.bind("<Enter>", lambda event, key=sys_key: self.on_hover(event, key))
            sys_button.bind("<Leave>", self.on_leave)

##############################





        sys_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        sys_info_frame.pack(pady=20, padx=20, fill="both")

        # Label für die Anzeige der Beschreibung
        self.sys_info_label = tk.Label(sys_info_frame, justify="left",wraplength=900)
        self.sys_info_label.pack(anchor="w")

    # Funktion für das Hover-Ereignis
    def on_hover(self, event, key):
        self.sys_info_label.configure(text=SoftwareSys.sys_dict[key]["Description"])

    # Funktion für das Verlassen des Buttons
    def on_leave(self, event):
        self.sys_info_label.configure(text="")
