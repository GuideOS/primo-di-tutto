import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from resorcess import *
from tabs.pop_ups import *
from tabs.system_dict_lib import SoftwareSys
from logger_config import setup_logger

logger = setup_logger(__name__)


class ExpertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        source_frame = ttk.Frame(self.inst_notebook)
        admin_frame = ttk.Frame(self.inst_notebook)

        source_frame.pack(fill="both", expand=True)
        admin_frame.pack(fill="both", expand=True)

        self.inst_notebook.add(source_frame, compound=LEFT, text="Quellen")
        self.inst_notebook.add(admin_frame, compound=LEFT, text="Admin")

        source_note_frame = SourcePanel(source_frame)
        source_note_frame.pack(fill=tk.BOTH, expand=True)

        admin_note_frame = AdminPanel(admin_frame)
        admin_note_frame.pack(fill=tk.BOTH, expand=True)


class AdminPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Frame für Canvas und Scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas-Container für sys_btn_frame
        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame in den Canvas einfügen
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
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

        max_columns = 4

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
                width=19,
            )
            sys_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_button.bind(
                "<Enter>", lambda event, key=sys_key: self.on_hover(event, key)
            )
            sys_button.bind("<Leave>", self.on_leave)

        sys_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        sys_info_frame.pack(pady=20, padx=20, fill="both")

        # Label für die Anzeige der Beschreibung
        self.sys_info_label = tk.Label(sys_info_frame, justify="left", wraplength=900)
        self.sys_info_label.pack(anchor="w")

    # Funktion für das Hover-Ereignis
    def on_hover(self, event, key):
        self.sys_info_label.configure(text=SoftwareSys.sys_dict[key]["Description"])

    # Funktion für das Verlassen des Buttons
    def on_leave(self, event):
        self.sys_info_label.configure(text="")


class SourcePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")

        self.added_repositories = ttk.LabelFrame(
            self, text="Eingebundene Repositories", padding=20
        )
        self.added_repositories.pack(fill="both", expand=True, padx=20, pady=20)

        self.added_tree_frame = tk.Frame(self.added_repositories)
        self.added_tree_frame.pack(fill="both", expand=True)

        self.added_treeview = ttk.Treeview(
            self.added_tree_frame, columns=("name"), show="headings"
        )
        self.added_treeview.heading("name", text="Name")
        self.added_treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.added_tree_frame, orient="vertical", command=self.added_treeview.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.added_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.add_sources_to_treeview()

        def open_source_f_d():
            popen(f"software-properties-gtk")

        self.open_source_folder = ttk.Button(
            self.added_repositories,
            text="Quellen bearbeiten",
            command=open_source_f_d,
            style="Custom.TButton",
        )
        self.open_source_folder.pack(pady=20, fill="x")

    def add_sources_to_treeview(self):
        sources_d1 = os.listdir("/etc/apt/sources.list.d")

        for file in sources_d1:
            self.added_treeview.insert("", "end", values=(file))
