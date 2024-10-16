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
from apt_manage import *
import subprocess
from piapps_manage import *
from flatpak_manage import flatpak_path
from flatpak_manage import Flat_remote_dict
from flatpak_manage import refresh_flatpak_installs
from flatpak_alias_list import *
from tabs.pop_ups import *
import re
import webbrowser
from subprocess import Popen, PIPE
from threading import Thread
from tool_tipps import CreateToolTip
from tabs.text_dict_lib import OneClicks, PiAppsOneClicks, FlatpakOneClicks
from tkinter import messagebox

def resize(img):
    basewidth = 500
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize))


def resize2(img):
    basewidth = 96
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize))


def get_app_summary(appstream_id):
    command = f"appstreamcli dump {appstream_id} | grep -m 1 -oP '<summary>\\K[^<]*'"
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e.stderr}")
        return ""


def extract_default_screenshot_url(application_id):
    output = subprocess.check_output(
        ["appstreamcli", "dump", application_id], text=True
    )

    start_index = output.find("<screenshots>")
    end_index = output.find("</screenshots>") + len("</screenshots>")

    xml_part = output[start_index:end_index]

    root = ET.fromstring(xml_part)

    for screenshot in root.findall(
        ".//screenshot[@type='default']/image[@type='source']"
    ):
        return screenshot.text

    return None


def build_screenshot_url():
    app_id = Flat_remote_dict[flatpak_entry.get()]

    screenshot_url = extract_default_screenshot_url(app_id)
    if screenshot_url:
        print("Standard-Screenshot-URL für {}:".format(app_id))
        print(screenshot_url)

    else:
        print("Kein Standard-Screenshot gefunden für {}.".format(app_id))


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


import tkinter as tk
from tkinter import ttk, PhotoImage, Label, Frame

class GameTabContent:

    @staticmethod
    def install_game_1(termf):
        def install_lutris():
            script_path = f"{application_path}/scripts/install_lutris"
            frame_width = termf.winfo_width()  # Use termf passed as an argument
            frame_height = termf.winfo_height()
            subprocess.run(
                f"xterm -into {wid} -bg Grey11 -geometry {frame_height}x{frame_width} -e \"{script_path} && read -p 'Press Enter to exit.' && exit ; exec bash\"",
                shell=True,
            )

        # Return details of the game, including the Icon path
        return {
            "Name": "Lutris",
            "Package": "Debian-Paket",
            "Description": "Bundle das Wine und Lutris installiert",
            "Icon": f"{application_path}/images/apps/lutris_logo_36.png",  # Add the Icon key here
            "Install": install_lutris,
        }

    @staticmethod
    def get_recommended_gaming(termf):
        return {
            "game_0": {
                "Name": "Steam",
                "Package": "DEB",
                "Description": "Ein Tool zum Zocken",
                "Icon": f"{application_path}/images/apps/steam_icon_36.png",
                "Install": lambda: print("Installing Steam...")
            },
            "game_1": GameTabContent.install_game_1(termf),  # Call with termf
            "game_2": {
                "Name": "Heroic",
                "Package": "DEB",
                "Description": "Ein Tool zum Zocken",
                "Icon": f"{application_path}/images/apps/heroic_icon_36.png",
                "Install": lambda: print("Installing Heroic...")
            },
        }


class GamingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Create the button frame first
        games_btn_frame = ttk.LabelFrame(self, text="Gaming Installer", padding=20)
        games_btn_frame.pack(pady=20, padx=20, fill="x")

        # Create the detail frame
        gams_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)
        gams_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.gaming_name = Label(gams_detail_frame, text="TEST")
        self.gaming_name.pack()

        self.gaming_pak = Label(gams_detail_frame, text="TEST")
        self.gaming_pak.pack()

        self.gaming_desc = Label(gams_detail_frame, text="TEST")
        self.gaming_desc.pack()

        self.gaming_inst_btn = ttk.Button(gams_detail_frame, text="Install")
        self.gaming_inst_btn.pack()

        # Initialize termf and pack it below the install button
        self.termf = Frame(gams_detail_frame, highlightthickness=0, borderwidth=0)
        self.termf.pack(fill=tk.BOTH, expand=True, pady=50, padx=30)

        global wid
        wid = self.termf.winfo_id()

        # Get recommended gaming list
        self.recommended_gaming = GameTabContent.get_recommended_gaming(self.termf)

        # Load game icons
        self.game0_icon = PhotoImage(file=self.recommended_gaming["game_0"]["Icon"])
        self.game1_icon = PhotoImage(file=self.recommended_gaming["game_1"]["Icon"])
        self.game2_icon = PhotoImage(file=self.recommended_gaming["game_2"]["Icon"])

        # Create game buttons
        self.create_game_button(games_btn_frame, "game_0", 0)
        self.create_game_button(games_btn_frame, "game_1", 1)
        self.create_game_button(games_btn_frame, "game_2", 2)

    def create_game_button(self, frame, game_key, column):
        game_data = self.recommended_gaming[game_key]
        game_button = ttk.Button(
            frame,
            text=game_data["Name"],
            image=self.get_game_icon(game_key),
            command=lambda: self.update_game_details(game_data),
            compound=tk.TOP,
            style="Custom.TButton"
        )
        game_button.grid(row=0, column=column, padx=5, pady=5, sticky="nesw")

    def get_game_icon(self, game_key):
        if game_key == "game_0":
            return self.game0_icon
        elif game_key == "game_1":
            return self.game1_icon
        elif game_key == "game_2":
            return self.game2_icon

    def update_game_details(self, game_data):
        self.gaming_name.configure(text=game_data["Name"])
        self.gaming_pak.configure(text=game_data["Package"])
        self.gaming_desc.configure(text=game_data["Description"])
        self.gaming_inst_btn.configure(command=game_data["Install"])







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
        process = Popen(task_script, stdout=PIPE, stderr=PIPE, text=True)

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

