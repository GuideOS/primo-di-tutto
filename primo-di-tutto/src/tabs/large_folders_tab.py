#!/usr/bin/python3

import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import subprocess


class LargeFoldersTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        my_home = os.path.expanduser("~")

        path_nodes = {}  # Pfad: Treeview-ID
        node_paths = {}  # Treeview-ID: Pfad

        def get_du_output():
            result = subprocess.run(
                ["du", "-h", "--max-depth=10", f"{my_home}/"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split("\n")
            output = []
            for line in lines:
                try:
                    size, path = line.strip().split(None, 1)
                    output.append((path, size))
                except ValueError:
                    continue
            return output

        def insert_path(tree, path, size):
            rel_path = os.path.relpath(path, my_home)
            parts = rel_path.split(os.sep)
            current_parent = ""
            full_path = ""
            for part in parts:
                if not part:
                    continue
                full_path = os.path.join(full_path, part)
                if full_path not in path_nodes:
                    node_id = tree.insert(current_parent, "end", text=part, values=("",))
                    path_nodes[full_path] = node_id
                    node_paths[node_id] = os.path.join(my_home, full_path)  # <-- hier absolut speichern
                    current_parent = node_id
                else:
                    current_parent = path_nodes[full_path]
            tree.item(path_nodes[full_path], values=(size,))


        def on_double_click(event, tree):
            item_id = tree.identify_row(event.y)
            if item_id:
                path = node_paths.get(item_id)
                if path:
                    abs_path = os.path.abspath(path)
                    try:
                        subprocess.Popen(["nemo", abs_path])
                    except FileNotFoundError:
                        print("Nemo nicht gefunden. Stelle sicher, dass Nemo installiert ist.")



        tree = ttk.Treeview(self, columns=("size",), show="tree headings")
        tree.heading("#0", text="Pfad", anchor="w")
        tree.heading("size", text="Größe", anchor="center")
        tree.column("#0", anchor="w", width=600)
        tree.column("size", anchor="center", width=100)
        tree.pack(fill="both", expand=True, padx=30, pady=30)

        du_data = get_du_output()
        for path, size in du_data:
            insert_path(tree, path, size)

        # Doppelklick-Event binden
        tree.bind("<Double-1>", lambda event: on_double_click(event, tree))