#!/usr/bin/python3

# Removed unused imports
from tkinter import *
from tkinter import ttk
from resorcess import *
import webbrowser


class LinksTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)

    

        # Dictionary mit Links @dunkelklausner, Gonzo-3004
        linux_links = {
            "Holarse - Linuxspiele-News": "https://holarse.de/",
            "ProtonDB - Checke die Kompatibilitär deiner Games": "https://www.protondb.com/",
            "LinuxNews - Das Neueste aus der Linux Welt": "https://linuxnews.de/",
            "GNU/LINUX.ch - Tiefergehende Artikel zu Linux-Themen": "https://gnulinux.ch/",
            "Linux Command Library - Wissen, was ein Kommando tut": "https://linuxcommandlibrary.com/",
            "Open OS - Linux lernen": "http://www.openos.at/",
            "Distrowatch - Ausführliche Liste und Beschreibungen aller Distros": "https://distrowatch.com/",
            "Decocode - Wissens-Datenbank": "https://www.decocode.de/",
            "Linux-Bibel - Die freundliche Website rund um Debian und Linux": "https://linux-bibel.at/",
        }





        self.frame = ttk.Frame(self, padding="30")
        self.frame.grid(sticky="nsew")

        self.frame.columnconfigure(0, weight=1)
        # Für jeden Link einen Button erzeugen
        for idx, (label, url) in enumerate(linux_links.items()):
            btn = ttk.Button(self.frame, text=label,style="Accent.TButton", command=lambda url=url: self.open_link(url))
            btn.grid(row=idx, column=0, pady=5, sticky="ew")

    def open_link(self, url):
        webbrowser.open_new_tab(url)