from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
import webbrowser
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.pop_ups import *


class ContribTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.take_part_frame = ttk.LabelFrame(self,text="Mach mit!",padding=20)
        self.take_part_frame.pack(padx=20,pady=20,fill="both",expand=True)

        take_part_message = ttk.Label(self.take_part_frame,text="Hier steht ein super kluger Text!")
        take_part_message.grid(row=0,column=0,columnspan=3)

        go_board = ttk.Button(self.take_part_frame,text="Werder Teil der Community")
        go_board.grid(row=1,column=0,columnspan=2)

        go_board = ttk.Button(self.take_part_frame,text="pgOS aufGithub")
        go_board.grid(row=1,column=3)

        self.thx_frame = ttk.LabelFrame(self,text="Ewiger Dank geht raus an die Community-Mitglieder ...",padding=20)
        self.thx_frame.pack(padx=20,pady=20,fill="both",expand=True)

        # Textbox erstellen und die Hintergrundfarbe setzen
        text_box = tk.Text(self.thx_frame, wrap='word')  # Hier wird die Hintergrundfarbe geändert
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar erstellen
        scrollbar = ttk.Scrollbar(self.thx_frame, orient=tk.VERTICAL, command=text_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar mit der Textbox verbinden
        text_box.config(yscrollcommand=scrollbar.set)

        # Text in die Textbox einfügen
        text_box.insert(tk.END, "Adelheid\nWolfgang\nGertrud\nAlbrecht\nDorothea\nOtto\nUlrich\nMargarethe\nErwin\nBrunhilde\nEberhard\nElfriede\nGunther\nRoswitha\nHartmut\nWalburga\nRudolf\nGisela\nAdalbert\nKunigunde\nHermann\nEdith\nHeinrich\nHildegard\nDietrich\nWilhelmine\nSigmund\nBertha\nLudwig\nIrmgard\nErika\nTheodora\nBaldwin\nFriedrich\nGudrun\nBertram\nHedwig\nGiselher\nBrunhilde\nAlmut\nEckhardt"
)

        # Textbox für Eingaben sperren (read-only)
        text_box.config(state=tk.DISABLED)
