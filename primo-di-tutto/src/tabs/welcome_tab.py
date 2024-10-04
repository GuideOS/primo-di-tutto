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


class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.system_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/pigro_icons/test.png")
        )

        label1 = ttk.Label(self, image=self.system_icon)
        label1.pack(pady=20)

        willko = """Schön das du dich für Project Guide OS entschieden hast. 
Wir wollen mit dieser Distribution .... ???? Bratwurst braten!"""

        button1 = ttk.Label(self, text=willko)
        button1.pack(pady=10)


 
