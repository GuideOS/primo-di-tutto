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

        def apt_install():
            hide_apt_frame()
            pigro_skript_task = "Installing ..."
            pigro_skript_task_app = f"{apt_entry.get()}"
            pigro_skript = [f"{permit}", "apt", "install", "-y", f"{apt_entry.get()}"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )




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

        def hide_flatpak_frame():
            flatpak_info_frame.pack_forget()
            flatpak_search_frame.pack(anchor="w", side=LEFT, pady=20, padx=10)
            flatpak_info_throber_frame.pack(fill=BOTH, expand=True, pady=20, padx=10)

        def flatpak_install():
            hide_flatpak_frame()

            pigro_skript_task = "Installing ..."
            pigro_skript_task_app = f"{flatpak_entry.get()}"
            pigro_skript = [
                f"flatpak",
                "install",
                "-y",
                "flathub",
                f"{Flat_remote_dict[flatpak_entry.get()]}",
            ]

            custom_installer = Custom_Installer(master)

            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )

            update_flatpak(Flat_remote_dict.keys())


class GamingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.proton_icon = PhotoImage(
            file=f"{application_path}/images/apps/proton_icon_36.png")
        self.system_icon = PhotoImage(
            file=f"{application_path}/images/apps/test.png"
        )
        self.heroic_icon = PhotoImage(
            file=f"{application_path}/images/apps/heroic_icon_36.png")
        self.steam_icon = PhotoImage(
            file=f"{application_path}/images/apps/steam_icon_36.png")
        self.lutris_icon = PhotoImage(
            file=f"{application_path}/images/apps/lutris_logo_36.png")



        game_lf = ttk.LabelFrame(self, text="Gaming Installer",padding=20)
        game_lf.pack(pady=20,padx=20,fill="x")

        label2 = ttk.Button(game_lf, text="Steam",compound=TOP, image=self.steam_icon)
        label2.grid(row=0,column=0)

        label2 = ttk.Button(game_lf, text="Lutris",image=self.lutris_icon,compound=TOP,)
        label2.grid(row=0,column=1,padx=5)

        label2 = ttk.Button(game_lf, text="Heroic",image=self.heroic_icon,compound=TOP,)
        label2.grid(row=0,column=2)

        label2 = ttk.Button(game_lf, text="ProtonUp-Qt",image=self.proton_icon,compound=TOP,)
        label2.grid(row=0,column=3,padx=5)

        game_tool_lf = ttk.LabelFrame(self, text="Gaming Installer",padding=20)
        game_tool_lf.pack(pady=20,padx=20,fill="both",expand=True)

        tool_name = ttk.Label(game_tool_lf, text="Name: Lutris",)
        tool_name.pack(pady=5,padx=10,fill="x")

        tool_format = ttk.Label(game_tool_lf, text="Paket: DEB",)
        tool_format.pack(pady=5,padx=10,fill="x")

        tool_descr = ttk.Label(game_tool_lf, text="Beschreinung:\n Dieser Installer stellt das Programm Lutris bereit und\ninstalliert alle nötigen Abhängikeiten z.B. Wine",)
        tool_descr.pack(pady=5,padx=10,fill="x")

        tool_descr = ttk.Button(game_tool_lf, text="Installieren",)
        tool_descr.pack(pady=5,padx=10,fill="x")




 


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
