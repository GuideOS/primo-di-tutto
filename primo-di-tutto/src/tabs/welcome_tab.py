import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
import psutil
from time import strftime
import socket
from PIL import ImageTk, Image
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_manage import count_flatpaks
from flatpak_alias_list import *
from tabs.pop_ups import *
from tool_tipps import CreateToolTip
from pathlib import Path  # Sicherstellen, dass Path importiert ist


class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Icon für den Willkommensbildschirm laden
        self.welcome_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/pigro_icons/test.png")
        )

        # Label für das Icon erstellen und im Fenster platzieren
        self.icon_label = ttk.Label(self, image=self.welcome_icon)
        self.icon_label.pack(pady=20)

        # Willkommensnachricht definieren
        welcome_message = """Hier könnte dein Einleitungs-Text stehen!"""

        # Label für die Willkommensnachricht erstellen
        self.welcome_label = ttk.Label(self, text=welcome_message)
        self.welcome_label.pack(pady=10)

        # LabelFrame für Autostart-Optionen erstellen
        self.autostart_frame = ttk.Labelframe(self, text="Autostart")
        self.autostart_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

        # Konfigurieren der Spalten im LabelFrame
        self.autostart_frame.columnconfigure(0, weight=1)  # Spalte für den Text
        self.autostart_frame.columnconfigure(1, weight=0)  # Spalte für den Checkbutton

        # Beschreibung für Autostart hinzufügen (nimmt die erste Spalte ein)
        self.autostart_description = ttk.Label(
            self.autostart_frame, 
            text=("Hier kannst du den Autostart dieses Programms deaktivieren. "
                  "Nach dem nächsten Start wird der Willkommensbildschirm entfernt "
                  "und Piazza wird zu einem System-Tool."),
            wraplength=600
        )
        self.autostart_description.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # BooleanVar für den Autostart-Status
        self.autostart_enabled = tk.BooleanVar()

        # Checkbutton für das Umschalten des Autostarts (rechtsbündig in der zweiten Spalte)
        self.autostart_checkbutton = ttk.Checkbutton(
            self.autostart_frame, 
            variable=self.autostart_enabled, 
            command=self.toggle_autostart, 
            style='Switch.TCheckbutton'
        )
        self.autostart_checkbutton.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    def toggle_autostart(self):
        """Aktualisiert die Konfigurationsdatei, um den Autostart zu deaktivieren."""
        # Pfad zur Konfigurationsdatei
        config_file_path = Path(os.path.expanduser("~/.primo/primo.conf"))

        # Datei einlesen, falls sie existiert, oder eine leere Liste verwenden
        if config_file_path.exists():
            with open(config_file_path, 'r') as config_file:
                config_lines = config_file.readlines()
        else:
            config_lines = []

        # 'firstrun' Einstellung auf 'no' setzen
        with open(config_file_path, 'w') as config_file:
            firstrun_set = False
            for line in config_lines:
                if line.startswith("firstrun="):
                    config_file.write("firstrun=no\n")
                    firstrun_set = True
                else:
                    config_file.write(line)

            # Falls "firstrun=" nicht gefunden wurde, am Ende hinzufügen
            if not firstrun_set:
                config_file.write("firstrun=no\n")
