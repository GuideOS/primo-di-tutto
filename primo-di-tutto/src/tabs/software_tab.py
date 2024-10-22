import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from threading import Thread
from PIL import ImageTk, Image
from urllib.request import urlopen
import urllib.error
import requests
import xml.etree.ElementTree as ET
import apt
from bs4 import BeautifulSoup
from resorcess import *
import subprocess
from tabs.pop_ups import *
import re
import webbrowser
from subprocess import Popen, PIPE
from threading import Thread
from tool_tipps import CreateToolTip
from tkinter import messagebox
from tabs.text_dict_lib import SoftwareGame
from apt_manage import *
from flatpak_manage import flatpak_path
from flatpak_manage import Flat_remote_dict
from flatpak_manage import refresh_flatpak_installs

class SoftwareTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        office_frame = ttk.Frame(self.inst_notebook)
        edu_frame = ttk.Frame(self.inst_notebook)
        gaming_frame = ttk.Frame(self.inst_notebook)


        office_frame.pack(fill="both", expand=True)
        edu_frame.pack(fill="both", expand=True)
        gaming_frame.pack(fill="both", expand=True)


        # add frames to notebook
        self.inst_notebook.add(office_frame, compound=LEFT, text="Büro")

        self.inst_notebook.add(
            edu_frame, compound=LEFT, text="Bildbearbeitung"
        )

        self.inst_notebook.add(
            gaming_frame, compound=LEFT, text="Gaming"
        )



        office_note_frame = OfficePanel(office_frame)
        office_note_frame.pack(fill=tk.BOTH, expand=True)


        edu_note_frame = EduPanel(edu_frame)
        edu_note_frame.pack(fill=tk.BOTH, expand=True)

        gaming_note_frame = GamingPanel(gaming_frame)
        gaming_note_frame.pack(fill=tk.BOTH, expand=True)

class OfficePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        def error_message_0():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        def error_message_1():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

class EduPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self["background"] = maincolor
        self.no_img = PhotoImage(file=f"{application_path}/images/apps/no_image.png")

        def error_message_0():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        def error_message_1():
            e_mass = Error_Mass(self)
            e_mass.grab_set()




class GamingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000
        #refresh_flatpak_installs()

        self.games_btn0_icon = PhotoImage(
            file=SoftwareGame.game_dict["game_0"]["Icon"]
        )

        self.games_btn1_icon = PhotoImage(
            file=SoftwareGame.game_dict["game_1"]["Icon"]
        )

        self.games_btn2_icon = PhotoImage(
            file=SoftwareGame.game_dict["game_2"]["Icon"]
        )

        self.games_btn3_icon = PhotoImage(
            file=SoftwareGame.game_dict["game_3"]["Icon"]
        )

        self.games_btn4_icon = PhotoImage(
            file=SoftwareGame.game_dict["game_4"]["Icon"]
        )

        # Create the button frame first
        games_btn_frame = ttk.LabelFrame(self, text="Gaming Installer", padding=20)
        games_btn_frame.pack(pady=20, padx=20, fill="x")

        games_btn_frame.grid_columnconfigure(0, weight=1)
        games_btn_frame.grid_columnconfigure(1, weight=1)
        games_btn_frame.grid_columnconfigure(2, weight=1)
        games_btn_frame.grid_columnconfigure(3, weight=1)
        games_btn_frame.grid_columnconfigure(4, weight=1)
###########################################################################

        def run_installation(game_key):
            #hide_apt_frame()
            pigro_skript_task = "Installing ..."
            pigro_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            pigro_skript = SoftwareGame.game_dict[game_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )
            self.gaming_inst_btn.config(text="Deinstallieren")
            self.master.wait_window(custom_installer)
            refresh_status(game_key)

        def run_uninstall(game_key):
            #hide_apt_frame()
            pigro_skript_task = "Removing From System"
            pigro_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            pigro_skript = SoftwareGame.game_dict[game_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )
            self.gaming_inst_btn.config(text="Installieren")
            self.master.wait_window(custom_installer)
            refresh_status(game_key)
###########################################################################
        def open_website(game_key):
            path = SoftwareGame.game_dict[game_key]["Path"]
            # Quotes added around the path
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(game_key):
            game_name = SoftwareGame.game_dict[game_key]["Name"]
            game_pakage = SoftwareGame.game_dict[game_key]["Package"]
            game_disc = SoftwareGame.game_dict[game_key]["Description"]
            game_path = SoftwareGame.game_dict[game_key]["Path"]
            # APT-Pakete und Flatpak-Installationen überprüfen
            installed_apt = game_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `game_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = game_path in flatpak_installs.values()

            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if installed_apt or installed_flatpak:
                print(f"{game_name} is installed")
                self.gaming_inst_btn.config(text="Deinstallieren", command=lambda: run_uninstall(game_key))
            else:
                print(f"{game_name} is not installed")
                self.gaming_inst_btn.config(text="Installieren", command=lambda: run_installation(game_key))


        def game_btn_action(game_key):
            # Den Namen des Spiels aus der SoftwareGame-Klasse holen
            game_name = SoftwareGame.game_dict[game_key]["Name"]
            game_pakage = SoftwareGame.game_dict[game_key]["Package"]
            game_disc = SoftwareGame.game_dict[game_key]["Description"]
            game_path = SoftwareGame.game_dict[game_key]["Path"]
            game_thumb = SoftwareGame.game_dict[game_key]["Thumbnail"]

            self.games_thumb = PhotoImage(file=game_thumb)

            self.gaming_name.config(text=f"Name: {game_name}")
            self.gaming_pak.config(text=f"Paket: {game_pakage}")
            self.gaming_desc.config(text=f"Beschreibung: {game_disc}")
            
            self.gaming_inst_btn.grid(column=1,row=0,rowspan=2,sticky="e")
            self.termf.grid(column=0,columnspan=2,row=3)
            self.thumb_lbl.configure(image=self.games_thumb)
            self.thumb_lbl.pack()

            #print(get_installed_apt_pkgs())
            refresh_status(game_key)



        game0_button = ttk.Button(
            games_btn_frame,
            text=SoftwareGame.game_dict["game_0"]["Name"],
            image=self.games_btn0_icon,
            command=lambda: game_btn_action("game_0"),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        game1_button = ttk.Button(
            games_btn_frame,
            text=SoftwareGame.game_dict["game_1"]["Name"],
            image=self.games_btn1_icon,
            command=lambda: game_btn_action("game_1"),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game1_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        game2_button = ttk.Button(
            games_btn_frame,
            text=SoftwareGame.game_dict["game_2"]["Name"],
            image=self.games_btn2_icon,
            command=lambda: game_btn_action("game_2"),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game2_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        game3_button = ttk.Button(
            games_btn_frame,
            text=SoftwareGame.game_dict["game_3"]["Name"],
            image=self.games_btn3_icon,
            command=lambda: game_btn_action("game_3"),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game3_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        game4_button = ttk.Button(
            games_btn_frame,
            text=SoftwareGame.game_dict["game_4"]["Name"],
            image=self.games_btn4_icon,
            command=lambda: open_website("game_4"),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game4_button.grid(row=0, column=4, padx=5, pady=5, sticky="nesw")
        #print(SoftwareGame.game_dict)

        # Create the detail frame
        gams_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)
        gams_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

        gams_detail_frame.grid_columnconfigure(0, weight=1)
        gams_detail_frame.grid_columnconfigure(1, weight=1)
        gams_detail_frame.grid_rowconfigure(3, weight=1)

        self.gaming_name = Label(gams_detail_frame, text="",justify="left",anchor="w")
        self.gaming_name.grid(column=0,row=0,sticky="ew")

        self.gaming_pak = Label(gams_detail_frame, text="",justify="left",anchor="w")
        self.gaming_pak.grid(column=0,row=1,sticky="ew")
        self.gaming_desc = Label(gams_detail_frame, text="",justify="left",anchor="w",wraplength=600)
        self.gaming_desc.grid(column=0,row=2,sticky="ew")

        self.gaming_inst_btn = ttk.Button(gams_detail_frame, text="Install", style="Custom.TButton")
        

        # Initialize termf and pack it below the install button
        self.termf = Frame(gams_detail_frame,)
        self.thumb_lbl = Label(self.termf)
        
        global game_wid
        game_wid = self.termf.winfo_id()











class Custom_Installer(tk.Toplevel):
    """child window that makes the the install process graphicle"""

    def __init__(self, parent):
        super().__init__(parent)
        self["background"] = maincolor
        self.icon = tk.PhotoImage(file=f"{application_path}/images/icons/logo.png")
        self.tk.call("wm", "iconphoto", self._w, self.icon)
        self.resizable(0, 0)
        cust_app_width = 700
        cust_app_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (cust_app_width / 2)
        y = (screen_height / 2) - (cust_app_height / 2)
        self.geometry(f"{cust_app_width}x{cust_app_height}+{int(x)}+{int(y)}")
        self.title("Software Manager")
        self.configure(bg=maincolor)

        self.installer_main_frame = Frame(self, background=maincolor)
        self.installer_main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.installer_main_frame.columnconfigure(1, weight=1)
        self.installer_main_frame.rowconfigure(0, weight=0)

        self.boot_log_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/unpack.png"
        )
        self.install_ok_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/unpack_ok.png"
        )
        self.install_error_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/unpack_error.png"
        )

        self.icon_label = tk.Label(
            self.installer_main_frame, image=self.boot_log_icon, bg=maincolor
        )

        self.icon_label.grid(row=0, rowspan=3, column=0, sticky="w", padx=10, pady=10)
        self.done_label = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            bg=maincolor,
            fg=label_frame_color,
            justify="left",
            anchor="w",
        )
        self.done_label.grid(row=0, column=1, sticky="nw")
        self.done_label2 = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            bg=maincolor,
            fg=main_font,
            justify="left",
            anchor="w",
        )
        self.done_label2.grid(row=1, column=1, sticky="nw")
        self.text = tk.Text(
            self.installer_main_frame,
            bg=maincolor,
            fg=main_font,
            height=1,
            borderwidth=0,
            highlightthickness=0,
            highlightcolor=main_font,
        )

        self.text.grid(row=2, column=1, columnspan=3, sticky="ew")

        self.install_button = tk.Button(
            self.installer_main_frame,
            text="Close",
            command=self.close_btn_command,
            borderwidth=0,
            highlightthickness=0,
            background=ext_btn,
            foreground=ext_btn_font,
            state=DISABLED,
        )
        self.install_button.grid(row=3, column=2, sticky="e", pady=10)
        self.grab_set()
        self.thread = None

    def do_task(self, task_label, task_app_label, task_script):
        self.done_label.config(text=task_label)
        self.done_label2.config(text=task_app_label)
        process = Popen(task_script.split(), stdout=PIPE, stderr=PIPE, text=True)
        self.thread = Thread(target=self.run_update_output, args=(process, task_label))
        self.thread.start()

    def run_update_output(self, process, task_label):
        self.update_output(process, task_label)

    def update_output(self, process, task_label):
        while process.poll() is None:
            line = process.stdout.readline().strip()
            if line:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, line)
                self.text.see(tk.END)

        self.text.delete(1.0, tk.END)
        exit_code = process.returncode
        if exit_code == 0:
            self.done_label.config(text=f"{task_label} Done!")
            self.icon_label.config(image=self.install_ok_icon)
        else:
            self.done_label.config(text=f"Error! (Exit-Code: {exit_code})")
            self.icon_label.config(image=self.install_error_icon)
        self.install_button.config(state=NORMAL)

    def close_btn_command(self):
        Custom_Installer.destroy(self)



    def on_thread_finished(self):
        print("Thread beendet")

