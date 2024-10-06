#!/usr/bin/python3

import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.pop_ups import *


class SourcesTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")


        self.rep_main_frame = ttk.Frame(
            self
        )
        self.rep_main_frame.pack(fill=BOTH, expand=True, pady=20, padx=20)



        self.added_repositories = ttk.LabelFrame(
            self.rep_main_frame,
            text="Added Repository",
            padding=20
        )
        self.added_repositories.pack(fill="both", expand=True)

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
            if pi_identify() == "pi_os":
                popen(f"sudo pcmanfm /etc/apt/sources.list.d")
                print("[Info] With great power comes great responsibility")
            else:
                popen(
                    f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY xdg-open /etc/apt/sources.list.d"
                )

        self.open_source_folder = ttk.Button(
            self.rep_main_frame,
            text="Open sources.list.d",
            command=open_source_f_d,
            style="Custom.TButton"

        )
        self.open_source_folder.pack(padx=20, expand=True, fill="x")

    def add_sources_to_treeview(self):
        sources_d1 = os.listdir("/etc/apt/sources.list.d")

        for file in sources_d1:
            self.added_treeview.insert("", "end", values=(file))
