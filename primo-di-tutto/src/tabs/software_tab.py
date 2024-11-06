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
from tabs.software_dict_lib import (
    SoftwareGame,
    SoftwareOffice,
    SoftwareStore,
    SoftwareCommunication,
)
from apt_manage import *
from snap_manage import *
from flatpak_manage import flatpak_path
from flatpak_manage import Flat_remote_dict
from flatpak_manage import refresh_flatpak_installs


def resize700(img):
    basewidth = 700
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize))


def resize46(img):
    basewidth = 46
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize))

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

        com_frame = ttk.Frame(self.inst_notebook)
        office_frame = ttk.Frame(self.inst_notebook)
        edu_frame = ttk.Frame(self.inst_notebook)
        gaming_frame = ttk.Frame(self.inst_notebook)
        #store_frame = ttk.Frame(self.inst_notebook)
        apt_frame = ttk.Frame(self.inst_notebook)


        com_frame.pack(fill="both", expand=True)
        office_frame.pack(fill="both", expand=True)
        edu_frame.pack(fill="both", expand=True)
        gaming_frame.pack(fill="both", expand=True)
        #store_frame.pack(fill="both", expand=True)
        apt_frame.pack(fill="both", expand=True)


        # add frames to notebook
        self.inst_notebook.add(com_frame, compound=LEFT, text="Kommunikation")
        self.inst_notebook.add(office_frame, compound=LEFT, text="Textverarbeitung")
        self.inst_notebook.add(edu_frame, compound=LEFT, text="Bildbearbeitung")
        self.inst_notebook.add(gaming_frame, compound=LEFT, text="Gaming")
        #self.inst_notebook.add(store_frame, compound=LEFT, text="Verwaltung")
        self.inst_notebook.add(apt_frame, compound=LEFT, text="APT-Verwaltung")



        com_note_frame = ComPanel(com_frame)
        com_note_frame.pack(fill=tk.BOTH, expand=True)

        office_note_frame = OfficePanel(office_frame)
        office_note_frame.pack(fill=tk.BOTH, expand=True)

        edu_note_frame = EduPanel(edu_frame)
        edu_note_frame.pack(fill=tk.BOTH, expand=True)

        gaming_note_frame = GamingPanel(gaming_frame)
        gaming_note_frame.pack(fill=tk.BOTH, expand=True)

        #store_note_frame = StorePanel(store_frame)
        #store_note_frame.pack(fill=tk.BOTH, expand=True)

        apt_search_panel = AptSearchPanel(apt_frame)
        apt_search_panel.pack(fill=tk.BOTH, expand=True)


class StorePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.store_btn0_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_0"]["Icon"]
        )

        self.store_btn1_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_1"]["Icon"]
        )

        def open_store(store_key):
            popen(f"""{SoftwareStore.store_dict[store_key]["Open"]}""")

        # Create the button frame first
        store_btn_frame = ttk.LabelFrame(self, text="Softwareverwaltung", padding=20)
        store_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        store_btn_frame.grid_columnconfigure(0, weight=1)
        store_btn_frame.grid_columnconfigure(1, weight=1)

        store0_button = ttk.Button(
            store_btn_frame,
            text=SoftwareStore.store_dict["store_0"]["Name"],
            image=self.store_btn0_icon,
            command=lambda: open_store("store_0"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        store0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        store1_button = ttk.Button(
            store_btn_frame,
            text=SoftwareStore.store_dict["store_1"]["Name"],
            image=self.store_btn1_icon,
            command=lambda: open_store("store_1"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        store1_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        self.store_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        self.store_info_frame.pack(pady=20, padx=20, fill=BOTH)

        self.store_info_frame.columnconfigure(0, weight=1)
        self.store_info_frame.rowconfigure(0, weight=1)

        info_text = """Gnome Software ist eine moderne Softwareverwaltung, die vor allem dafür genutzt werden kann, grafische Desktop-Programme zu installieren. In GuideOS wird das volle Potenzial ausgenutzt: Es können sowohl Debian-Pakete, Flatpaks als auch Snaps installiert werden. Das stellt sicher, dass die größtmögliche Softwareauswahl verfügbar ist.


Synaptic ist eine grafische Oberfläche zur Verwaltung von Debian-Systempaketen. Im Gegensatz zu Gnome Software findet man hier alle Systempakete des Repositorys, unter anderem auch Treiber und einzelne Bibliotheken. Vor allem für fortgeschrittene Nutzer bietet Synaptic eine Vielzahl von Informationen über einzelne Pakete.


In den weiteren Kategorien befindet sich eine Softwareauswahl der Community, die darauf abgestimmt ist, den PC disziplinübergreifend zu nutzen.
"""

        self.store_info_discription = ttk.Label(
            self.store_info_frame,
            text=info_text,
            justify="left",
            wraplength=750,
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="nesw")


class OfficePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            office_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            back_button.pack_forget()
            office_detail_frame.pack_forget()

        def hide_button_frame():
            office_btn_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        back_button = ttk.Button(self, text="Zurück", command=show_button_frame)

        office_btn_frame = ttk.LabelFrame(self, text="Gaming Empfehlungen", padding=20)
        office_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        office_btn_frame.grid_columnconfigure(0, weight=1)
        office_btn_frame.grid_columnconfigure(1, weight=1)
        office_btn_frame.grid_columnconfigure(2, weight=1)
        office_btn_frame.grid_columnconfigure(3, weight=1)
        office_btn_frame.grid_columnconfigure(4, weight=1)

        def run_installation(office_key):
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareOffice.office_dict[office_key]["Name"]
            primo_skript = SoftwareOffice.office_dict[office_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.office_detail_inst.config(text="Deinstallieren")

            refresh_status(office_key)

        def run_uninstall(office_key):
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareOffice.office_dict[office_key]["Name"]
            primo_skript = SoftwareOffice.office_dict[office_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.office_detail_inst.config(text="Installieren")

            refresh_status(office_key)

        def open_website(office_key):
            path = SoftwareOffice.office_dict[office_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(office_key):
            office_name = SoftwareOffice.office_dict[office_key]["Name"]
            office_pakage = SoftwareOffice.office_dict[office_key]["Package"]
            office_disc = SoftwareOffice.office_dict[office_key]["Description"]
            office_path = SoftwareOffice.office_dict[office_key]["Path"]

            installed_apt = office_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `com_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = office_path in flatpak_installs.values()
            installed_snap = office_path in get_installed_snaps()
            print()
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if installed_snap or installed_apt or installed_flatpak:
                print(f"{office_name} is installed")
                self.office_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(office_key),
                    style="Red.TButton",
                )
            else:
                print(f"{office_name} is not installed")
                self.office_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(office_key),
                    style="Green.TButton",
                )

        def office_btn_action(office_key):
            office_icon_img = SoftwareOffice.office_dict[office_key]["Icon"]
            office_name = SoftwareOffice.office_dict[office_key]["Name"]
            office_pakage = SoftwareOffice.office_dict[office_key]["Package"]
            office_disc = SoftwareOffice.office_dict[office_key]["Description"]
            office_path = SoftwareOffice.office_dict[office_key]["Path"]
            office_thumb = SoftwareOffice.office_dict[office_key]["Thumbnail"]

            # self.office_thumb = PhotoImage(file=office_thumb)
            # self.office_icon = PhotoImage(file=office_icon_img)

            # Öffnen und skalieren des Thumbnails
            thumb_img = Image.open(office_thumb)
            resized_thumb_img = resize700(thumb_img)
            self.office_thumb = ImageTk.PhotoImage(resized_thumb_img)

            # Öffnen und skalieren des Icons
            icon_img = Image.open(office_icon_img)
            resized_icon_img = resize46(icon_img)
            self.office_icon = ImageTk.PhotoImage(resized_icon_img)

            self.office_detail_icon.configure(image=self.office_icon)
            self.office_detail_name.config(text=f"{office_name}")
            self.office_detail_pak.config(text=f"{office_pakage}")
            self.office_detail_desc.config(text=f"\n{office_disc}")

            self.office_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.office_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            office_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # print(get_installed_apt_pkgs())
            refresh_status(office_key)

        self.office_btn_icons = []

        for i, (office_key, office_info) in enumerate(
            SoftwareOffice.office_dict.items()
        ):
            img = Image.open(office_info["Icon"])
            resized_img = resize46(img)
            icon = ImageTk.PhotoImage(resized_img)
            self.office_btn_icons.append(icon)

        max_columns = 5

        for i, (office_key, office_info) in enumerate(
            SoftwareOffice.office_dict.items()
        ):
            row = i // max_columns
            column = i % max_columns

            office_button = ttk.Button(
                office_btn_frame,
                text=office_info["Name"],
                image=self.office_btn_icons[i],
                command=lambda key=office_key: office_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
            )
            office_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")

        office_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        office_detail_frame.grid_columnconfigure(1, weight=1)
        office_detail_frame.grid_rowconfigure(3, weight=1)

        self.office_detail_icon = Label(
            office_detail_frame,
        )
        self.office_detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.office_detail_name = Label(
            office_detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.office_detail_name.grid(column=1, row=0, sticky="w")

        self.office_detail_pak = Label(
            office_detail_frame, text="", justify="left", anchor="w"
        )
        self.office_detail_pak.grid(column=1, row=1, sticky="we")

        self.office_detail_desc = Label(
            office_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.office_detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.office_detail_inst = ttk.Button(
            office_detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            office_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global office_wid
        office_wid = self.termf.winfo_id()


class EduPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


class GamingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            game_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            back_button.pack_forget()
            game_detail_frame.pack_forget()

        def hide_button_frame():
            game_btn_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        back_button = ttk.Button(self, text="Zurück", command=show_button_frame)

        game_btn_frame = ttk.LabelFrame(self, text="Gaming Empfehlungen", padding=20)
        game_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        game_btn_frame.grid_columnconfigure(0, weight=1)
        game_btn_frame.grid_columnconfigure(1, weight=1)
        game_btn_frame.grid_columnconfigure(2, weight=1)
        game_btn_frame.grid_columnconfigure(3, weight=1)
        game_btn_frame.grid_columnconfigure(4, weight=1)

        def run_installation(game_key):
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            primo_skript = SoftwareGame.game_dict[game_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.game_detail_inst.config(text="Deinstallieren")

            refresh_status(game_key)

        def run_uninstall(game_key):
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            primo_skript = SoftwareGame.game_dict[game_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.game_detail_inst.config(text="Installieren")

            refresh_status(game_key)

        def open_website(game_key):
            path = SoftwareGame.game_dict[game_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(game_key):
            game_name = SoftwareGame.game_dict[game_key]["Name"]
            game_pakage = SoftwareGame.game_dict[game_key]["Package"]
            game_disc = SoftwareGame.game_dict[game_key]["Description"]
            game_path = SoftwareGame.game_dict[game_key]["Path"]

            installed_apt = game_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `com_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = game_path in flatpak_installs.values()
            installed_snap = game_path in get_installed_snaps()
            print()
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if installed_snap or installed_apt or installed_flatpak:
                print(f"{game_name} is installed")
                self.game_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(game_key),
                    style="Red.TButton",
                )
            else:
                print(f"{game_name} is not installed")
                self.game_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(game_key),
                    style="Green.TButton",
                )

        def game_btn_action(game_key):
            game_icon_img = SoftwareGame.game_dict[game_key]["Icon"]
            game_name = SoftwareGame.game_dict[game_key]["Name"]
            game_pakage = SoftwareGame.game_dict[game_key]["Package"]
            game_disc = SoftwareGame.game_dict[game_key]["Description"]
            game_path = SoftwareGame.game_dict[game_key]["Path"]
            game_thumb = SoftwareGame.game_dict[game_key]["Thumbnail"]

            # self.game_thumb = PhotoImage(file=game_thumb)
            # self.game_icon = PhotoImage(file=game_icon_img)

            # Öffnen und skalieren des Thumbnails
            thumb_img = Image.open(game_thumb)
            resized_thumb_img = resize700(thumb_img)
            self.game_thumb = ImageTk.PhotoImage(resized_thumb_img)

            # Öffnen und skalieren des Icons
            icon_img = Image.open(game_icon_img)
            resized_icon_img = resize46(icon_img)
            self.game_icon = ImageTk.PhotoImage(resized_icon_img)

            self.game_detail_icon.configure(image=self.game_icon)
            self.game_detail_name.config(text=f"{game_name}")
            self.game_detail_pak.config(text=f"{game_pakage}")
            self.game_detail_desc.config(text=f"\n{game_disc}")

            self.game_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.game_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            game_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # print(get_installed_apt_pkgs())
            refresh_status(game_key)

        self.game_btn_icons = []

        for i, (game_key, game_info) in enumerate(SoftwareGame.game_dict.items()):
            img = Image.open(game_info["Icon"])
            resized_img = resize46(img)
            icon = ImageTk.PhotoImage(resized_img)
            self.game_btn_icons.append(icon)

        max_columns = 5

        for i, (game_key, game_info) in enumerate(SoftwareGame.game_dict.items()):
            row = i // max_columns
            column = i % max_columns

            game_button = ttk.Button(
                game_btn_frame,
                text=game_info["Name"],
                image=self.game_btn_icons[i],
                command=lambda key=game_key: game_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=20,
            )
            game_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")

        game_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        game_detail_frame.grid_columnconfigure(1, weight=1)
        game_detail_frame.grid_rowconfigure(3, weight=1)

        self.game_detail_icon = Label(
            game_detail_frame,
        )
        self.game_detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.game_detail_name = Label(
            game_detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.game_detail_name.grid(column=1, row=0, sticky="w")

        self.game_detail_pak = Label(
            game_detail_frame, text="", justify="left", anchor="w"
        )
        self.game_detail_pak.grid(column=1, row=1, sticky="we")

        self.game_detail_desc = Label(
            game_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.game_detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.game_detail_inst = ttk.Button(
            game_detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            game_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global game_wid
        game_wid = self.termf.winfo_id()


class ComPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            com_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            back_button.pack_forget()
            com_detail_frame.pack_forget()

        def hide_button_frame():
            com_btn_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        back_button = ttk.Button(self, text="Zurück", command=show_button_frame)

        com_btn_frame = ttk.LabelFrame(
            self, text="Communication Empfehlungen", padding=20
        )
        com_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        com_btn_frame.grid_columnconfigure(0, weight=1)
        com_btn_frame.grid_columnconfigure(1, weight=1)
        com_btn_frame.grid_columnconfigure(2, weight=1)
        com_btn_frame.grid_columnconfigure(3, weight=1)
        com_btn_frame.grid_columnconfigure(4, weight=1)

        def run_installation(com_key):
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareCommunication.com_dict[com_key]["Name"]
            primo_skript = SoftwareCommunication.com_dict[com_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.com_detail_inst.config(text="Deinstallieren")

            refresh_status(com_key)

        def run_uninstall(com_key):
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareCommunication.com_dict[com_key]["Name"]
            primo_skript = SoftwareCommunication.com_dict[com_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.com_detail_inst.config(text="Installieren")

            refresh_status(com_key)

        def open_website(com_key):
            path = SoftwareCommunication.com_dict[com_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(com_key):
            com_name = SoftwareCommunication.com_dict[com_key]["Name"]
            com_pakage = SoftwareCommunication.com_dict[com_key]["Package"]
            com_disc = SoftwareCommunication.com_dict[com_key]["Description"]
            com_path = SoftwareCommunication.com_dict[com_key]["Path"]

            installed_apt = com_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `com_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = com_path in flatpak_installs.values()
            installed_snap = com_path in get_installed_snaps()
            print()
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if installed_snap or installed_apt or installed_flatpak:
                print(f"{com_name} is installed")
                self.com_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(com_key),
                    style="Red.TButton",
                )
            else:
                print(f"{com_name} is not installed")
                self.com_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(com_key),
                    style="Green.TButton",
                )

        def com_btn_action(com_key):
            com_icon_img = SoftwareCommunication.com_dict[com_key]["Icon"]
            com_name = SoftwareCommunication.com_dict[com_key]["Name"]
            com_pakage = SoftwareCommunication.com_dict[com_key]["Package"]
            com_disc = SoftwareCommunication.com_dict[com_key]["Description"]
            com_path = SoftwareCommunication.com_dict[com_key]["Path"]
            com_thumb = SoftwareCommunication.com_dict[com_key]["Thumbnail"]

            # Öffnen und skalieren des Thumbnails
            thumb_img = Image.open(com_thumb)
            resized_thumb_img = resize700(thumb_img)
            self.com_thumb = ImageTk.PhotoImage(resized_thumb_img)

            # Öffnen und skalieren des Icons
            icon_img = Image.open(com_icon_img)
            resized_icon_img = resize46(icon_img)
            self.com_icon = ImageTk.PhotoImage(resized_icon_img)

            self.com_detail_icon.configure(image=self.com_icon)
            self.com_detail_name.config(text=f"{com_name}")
            self.com_detail_pak.config(text=f"{com_pakage}")
            self.com_detail_desc.config(text=f"\n{com_disc}")

            self.com_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.com_thumb)
            self.thumb_lbl.pack(fill="x")

            hide_button_frame()
            com_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # print(get_installed_apt_pkgs())
            refresh_status(com_key)

        self.com_btn_icons = []

        for i, (com_key, com_info) in enumerate(SoftwareCommunication.com_dict.items()):
            img = Image.open(com_info["Icon"])
            resized_img = resize46(img)
            icon = ImageTk.PhotoImage(resized_img)
            self.com_btn_icons.append(icon)

        max_columns = 5

        for i, (com_key, com_info) in enumerate(SoftwareCommunication.com_dict.items()):
            row = i // max_columns
            column = i % max_columns

            com_button = ttk.Button(
                com_btn_frame,
                text=com_info["Name"],
                image=self.com_btn_icons[i],
                command=lambda key=com_key: com_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=20,
            )
            com_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")

        com_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        com_detail_frame.grid_columnconfigure(1, weight=1)
        com_detail_frame.grid_rowconfigure(3, weight=1)

        self.com_detail_icon = Label(
            com_detail_frame,
        )
        self.com_detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.com_detail_name = Label(
            com_detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.com_detail_name.grid(column=1, row=0, sticky="w")

        self.com_detail_pak = Label(
            com_detail_frame, text="", justify="left", anchor="w"
        )
        self.com_detail_pak.grid(column=1, row=1, sticky="we")

        self.com_detail_desc = Label(
            com_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.com_detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.com_detail_inst = ttk.Button(
            com_detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            com_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global com_wid
        com_wid = self.termf.winfo_id()


class AptSearchPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        def error_message_0():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        def error_message_1():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        if "dark" in theme or "noir" in theme:
            self.deb_butt = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/debian_dark_24x24.png"
            )
        else:
            self.deb_butt = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/debian_light_24x24.png"
            )
        self.debinstall_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/debian-logo.png"
        )
        self.no_img = PhotoImage(file=f"{application_path}/images/apps/no_image.png")
        self.deb_pack_l = PhotoImage(
            file=f"{application_path}/images/icons/deb_pack_l.png"
        )

        self.deb_nav = PhotoImage(
            file=f"{application_path}/images/icons/nav_bar/debian_light_24x24.png"
        )
        self.search_btn = PhotoImage(
            file=f"{application_path}/images/icons/nav_bar/glass_icon.png"
        )
        self.exit_btn = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/exit_btn.png"
        )

        def apt_install():
            hide_apt_frame()
            pigro_skript_task = "Installing ..."
            pigro_skript_task_app = f"{apt_entry.get()}"
            pigro_skript = f"{permit} apt install -y {apt_entry.get()}"
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )
            self.master.wait_window(custom_installer)

        def apt_uninstall():
            hide_apt_frame()
            pigro_skript_task = "Removing From System"
            pigro_skript_task_app = f"{apt_entry.get()}"
            pigro_skript = f"{permit} apt remove -y {apt_entry.get()}"

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )
            self.master.wait_window(custom_installer)
            apt_search_container.pack(anchor="w", pady=20, padx=10)

        def update_apt_list(apt_data):
            apt_data = sorted(apt_data)
            apt_list_box.delete(0, END)
            for item in apt_data:
                apt_list_box.insert(END, item)

        def apt_list_fillout(e):
            apt_entry.delete(0, END)
            apt_entry.insert(0, apt_list_box.get(apt_list_box.curselection()))
            apt_show_infos()

        def apt_entry_delete():
            apt_entry.delete(0, END)

        def apt_search_check(e):
            typed = apt_entry.get()
            if typed == "":
                apt_data = get_apt_cache()
            else:
                apt_data = []
                for item in get_apt_cache():
                    if typed.lower() in item.lower():
                        apt_data.append(item)
            update_apt_list(apt_data)

        def get_debian_icon():
            if apt_entry.get() in apt_flatpak_matches:
                try:
                    url_output = f"https://dl.flathub.org/repo/appstream/x86_64/icons/128x128/{apt_flatpak_matches[apt_entry.get()]}.png"
                    with urlopen(url_output) as url_output:
                        self.deban_navbar_icon = Image.open(url_output)
                    self.deban_navbar_icon = resize2(self.deban_navbar_icon)

                    self.deban_navbar_icon = ImageTk.PhotoImage(self.deban_navbar_icon)
                    apt_pkg_icon.config(image=self.deban_navbar_icon)
                except urllib.error.HTTPError as e:
                    print(f"{e}")
                    apt_pkg_icon.config(image=self.debinstall_icon)
            else:
                apt_pkg_icon.config(image=self.debinstall_icon)

        def apt_screenshot():
            try:
                apt_app = str(apt_entry.get())
                url = f"https://screenshots.debian.net/package/{apt_app}#gallery-1"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                links = [
                    link.get("href")
                    for link in soup.find_all("a")
                    if link.get("href").endswith(".png")
                ]

                url_output = f"https://screenshots.debian.net{str(links[1])}"
                with urlopen(url_output) as url_output:
                    self.app_img = Image.open(url_output)
                self.app_img = resize(self.app_img)

                self.app_img = ImageTk.PhotoImage(self.app_img)
                apt_panel.config(image=self.app_img)
            except IndexError as e:
                print(f"{e}")
                if apt_entry.get() in apt_flatpak_matches:
                    try:
                        app_id = Flat_remote_dict[flatpak_entry.get()]
                        screenshot_url = extract_default_screenshot_url(app_id)
                        if screenshot_url:
                            print("Screenshot-URL {}:".format(app_id))
                            print(screenshot_url)
                        else:
                            print("No Screenshot Found {}.".format(app_id))

                        with urlopen(screenshot_url) as url_output:
                            self.img = Image.open(url_output)
                        self.img = resize(self.img)
                        self.img = ImageTk.PhotoImage(self.img)
                        apt_panel.config(image=self.img)

                    except requests.exceptions.RequestException as e:
                        print("Error fetching URL:", e)
                        apt_panel.config(self.no_img)

                    except subprocess.CalledProcessError as err:
                        print("Command returned non-zero exit status:", err)
                        if "returned non-zero exit status 4" in str(err):
                            try:
                                app_id += ".desktop"
                                screenshot_url = extract_default_screenshot_url(app_id)
                                if screenshot_url:
                                    print("Screenshot-URL {}:".format(app_id))
                                    print(screenshot_url)
                                else:
                                    print("No Screenshot Found {}.".format(app_id))

                                with urlopen(screenshot_url) as url_output:
                                    self.img = Image.open(url_output)
                                self.img = resize(self.img)
                                self.img = ImageTk.PhotoImage(self.img)
                                apt_panel.config(image=self.img)

                            except subprocess.CalledProcessError as err:
                                print("Command returned non-zero exit status again:", err)
                                apt_panel.config(self.no_img)

        def put_apt_description():
            pkg_infos = os.popen(f"apt show -a {apt_entry.get()}")
            read_pkg_infos = pkg_infos.read()

            insert_description = read_pkg_infos
            description_text.delete("1.0", "end")
            description_text.insert(END, insert_description)

        def hide_apt_search_container():
            apt_search_container.pack_forget()

        def apt_show_infos():
            if apt_entry.get() == "":
                error_message_0()
            elif apt_entry.get() not in get_apt_cache():
                error_message_1()
            else:
                apt_info_throber_frame.pack_forget()
                apt_info_container.pack(fill=BOTH, expand=True)
                apt_pkg_name.config(text=f"{apt_entry.get()}")
                pkg_infos_desc = os.popen(
                    f"apt show -a {apt_entry.get()} | grep -E 'Description:'"
                )
                read_pkg_infos_desc = pkg_infos_desc.read()

                apt_pkg_status.config(
                    text=f"{read_pkg_infos_desc.split(':')[1]}",
                    justify="left",
                    anchor="w",
                )

                if apt_entry.get() in get_installed_apt_pkgs():
                    apt_pkg_inst.config(
                        text="Uninstall",
                        width=10,
                        command=apt_uninstall,
                        style='Red.TButton'
                    )
                else:
                    apt_pkg_inst.config(
                        text="Install",
                        width=10,
                        command=apt_install,
                        style='Green.TButton'
                    )

                apt_panel.config(image=self.no_img)

                hide_apt_search_container()
                get_debian_icon()
                apt_screenshot()
                put_apt_description()

        def hide_apt_frame():
            apt_info_container.pack_forget()
            apt_search_container.pack(anchor="w", pady=20, padx=10,fill=BOTH, expand=True)
            apt_info_throber_frame.pack(fill="x", pady=20, padx=10)

        apt_main_container = Frame(self)
        apt_main_container.pack(fill="both", expand=True)

        apt_search_container = ttk.LabelFrame(
            apt_main_container,
            text="Suche",
            padding=20
        )
        apt_search_container.pack(anchor="w", pady=20, padx=10,fill="both", expand=True)

        apt_search_field = Frame(
            apt_search_container,
            borderwidth=0,
            highlightthickness=0,
        )
        apt_search_field.pack(fill="x", pady=5)

        apt_search_btn = Label(
            apt_search_field,
            image=self.search_btn,

        )

        apt_entry = ttk.Entry(
            apt_search_field, font=("Sans", 15)
        )
        listbox_ttp = CreateToolTip(
            apt_entry,
            " - Typ to finde a package\n\n - Single click on a listbox item to show more infos",
        )
        apt_entry.pack(fill="x", expand=True, side="left")

        apt_list_box = Listbox(
            apt_search_container,
            borderwidth=0,
            highlightthickness=0,
            selectmode=tk.SINGLE,
        )
        apt_list_box_scrollbar = ttk.Scrollbar(apt_search_container)
        apt_list_box_scrollbar.pack(side=RIGHT, fill=Y)
        apt_list_box.config(yscrollcommand=apt_list_box_scrollbar.set)
        apt_list_box_scrollbar.config(command=apt_list_box.yview)
        apt_list_box.pack(fill=BOTH,expand=True)

        update_apt_list(get_apt_cache())

        apt_list_box.bind("<ButtonRelease-1>", apt_list_fillout)

        apt_entry.bind("<KeyRelease>", apt_search_check)

        apt_info_throber_frame = Frame(apt_main_container)
        apt_info_throber_frame.pack(fill="x", pady=20, padx=10)

 
        self.store_btn0_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_0"]["Icon"]
        )

        self.store_btn1_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_1"]["Icon"]
        )

        def open_store(store_key):
            popen(f"""{SoftwareStore.store_dict[store_key]["Open"]}""")

        # Create the button frame first
        store_btn_frame = ttk.LabelFrame(apt_info_throber_frame, text="Softwareverwaltung", padding=20)
        store_btn_frame.pack( fill="x")

        store_btn_frame.grid_columnconfigure(0, weight=1)
        store_btn_frame.grid_columnconfigure(1, weight=1)

        store0_button = ttk.Button(
            store_btn_frame,
            text=SoftwareStore.store_dict["store_0"]["Name"],
            image=self.store_btn0_icon,
            command=lambda: open_store("store_0"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        store0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        store1_button = ttk.Button(
            store_btn_frame,
            text=SoftwareStore.store_dict["store_1"]["Name"],
            image=self.store_btn1_icon,
            command=lambda: open_store("store_1"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        store1_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        apt_info_container = ttk.Frame(apt_main_container,padding=20)
        apt_info_container.columnconfigure(0, weight=1)
        apt_info_container.rowconfigure(2, weight=1)

        apt_exit = ttk.Button(
            apt_info_container,
            text="Back",
            image=self.exit_btn,
            compound=LEFT,
            command=hide_apt_frame,
        )
        apt_exit.grid(row=0,column=0,sticky="ew")

        apt_pkg_header_1 = ttk.LabelFrame(
            apt_info_container,
            text="Application",
            padding=20
        )
        apt_pkg_header_1.grid(row=1,column=0,sticky="ew")

        apt_pkg_header_1_1 = Frame(
            apt_pkg_header_1, borderwidth=0, highlightthickness=0
        )
        apt_pkg_header_1_1.pack(fill="x")
        apt_pkg_header_1_1.columnconfigure(1, weight=2)

        apt_pkg_icon = Label(
            apt_pkg_header_1_1,
            image=self.debinstall_icon,
            font=font_10_b,
            justify="left",
            padx=10,
        )
        apt_pkg_icon.grid(row=0, rowspan=2, column=0)

        apt_pkg_name = Label(
            apt_pkg_header_1_1,
            text="",
            font=font_20,
            justify="left",
            anchor="w",
            padx=20,
        )
        apt_pkg_name.grid(row=0, column=1, sticky="ew")

        apt_pkg_status = Label(
            apt_pkg_header_1_1,
            text="",
            font=font_8,
            justify="left",
            anchor="w",
            padx=20,
        )
        apt_pkg_status.grid(row=1, column=1, sticky="ew")

        apt_pkg_inst = ttk.Button(
            apt_pkg_header_1_1,
            text="Install",
            width=10,
            command=apt_install,
            style='Green.TButton'
        )
        apt_pkg_inst.grid(row=0, column=2, sticky="e")


        apt_detail_frame = ttk.LabelFrame(apt_info_container, text="Details", padding=20)
        apt_detail_frame.grid(row=2, column=0, sticky="nsew")


        apt_detail_frame.columnconfigure(0, weight=1)
        apt_detail_frame.rowconfigure(0, weight=1)

        apt_canvas = Canvas(
            apt_detail_frame,
            borderwidth=0,
            highlightthickness=0
        )
        apt_canvas.grid(row=0, column=0, sticky="nsew")

        apt_canvas_scrollbar = ttk.Scrollbar(
            apt_detail_frame,
            orient="vertical",
            command=apt_canvas.yview
        )
        apt_canvas_scrollbar.grid(row=0, column=1, sticky="ns")

        apt_canvas.configure(yscrollcommand=apt_canvas_scrollbar.set)

        apt_canvas_frame = Frame(apt_canvas)
        apt_canvas.create_window((0, 0), window=apt_canvas_frame, anchor="nw")

        apt_canvas_frame.bind("<Configure>", lambda e: apt_canvas.configure(scrollregion=apt_canvas.bbox("all")))

        apt_panel = Label(apt_canvas_frame)
        apt_panel.grid(row=0, column=0, columnspan=2, pady=20)

        description_text = Text(
            apt_canvas_frame,
            borderwidth=0,
            highlightthickness=0,
            font=("Sans", 9),
            wrap=WORD,
            padx=20,
        )
        description_text.grid(row=1, column=0, sticky="nesw", padx=(20, 0))

        apt_canvas_frame.columnconfigure(0, weight=1)
        apt_canvas_frame.rowconfigure(1, weight=1)

        apt_info_container.columnconfigure(0, weight=1)
        apt_info_container.rowconfigure(2, weight=1)


class Custom_Installer(tk.Toplevel):
    """child window that makes the the install process graphicle"""

    def __init__(self, parent):
        super().__init__(parent)
        # self["background"] = maincolor
        self.icon = tk.PhotoImage(
            file="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png"
        )
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
        # self.configure(bg=maincolor)

        self.installer_main_frame = Frame(
            self,
        )
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
            self.installer_main_frame,
            image=self.boot_log_icon,  # bg=maincolor
        )

        self.icon_label.grid(row=0, rowspan=3, column=0, sticky="w", padx=10, pady=10)
        self.done_label = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            # bg=maincolor,
            # fg=label_frame_color,
            justify="left",
            anchor="w",
        )
        self.done_label.grid(row=0, column=1, sticky="nw")
        self.done_label2 = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            # bg=maincolor,
            # fg=main_font,
            justify="left",
            anchor="w",
        )
        self.done_label2.grid(row=1, column=1, sticky="nw")
        self.text = tk.Text(
            self.installer_main_frame,
            # bg=maincolor,
            # fg=main_font,
            height=1,
            borderwidth=0,
            highlightthickness=0,
            # highlightcolor=main_font,
        )

        self.text.grid(row=2, column=1, columnspan=3, sticky="ew")

        self.install_button = ttk.Button(
            self.installer_main_frame,
            text="Close",
            command=self.close_btn_command,
            # borderwidth=0,
            # highlightthickness=0,
            # background=ext_btn,
            # foreground=ext_btn_font,
            state=DISABLED,
            style="Accent.TButton",
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
            self.done_label.config(text=f"{task_label} Erledigt !")
            self.icon_label.config(image=self.install_ok_icon)
        else:
            self.done_label.config(text=f"Error! (Exit-Code: {exit_code})")
            self.icon_label.config(image=self.install_error_icon)
        self.install_button.config(state=NORMAL)

    def close_btn_command(self):
        Custom_Installer.destroy(self)

    def on_thread_finished(self):
        print("Thread beendet")
