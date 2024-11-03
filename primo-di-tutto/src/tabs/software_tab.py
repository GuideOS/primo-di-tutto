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
from tabs.text_dict_lib import (
    SoftwareGame,
    SoftwareBrowser,
    SoftwareOffice,
    SoftwareStore,
)
from apt_manage import *
from snap_manage import *
from flatpak_manage import flatpak_path
from flatpak_manage import Flat_remote_dict
from flatpak_manage import refresh_flatpak_installs


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

        test_frame = ttk.Frame(self.inst_notebook)
        store_frame = ttk.Frame(self.inst_notebook)
        browser_frame = ttk.Frame(self.inst_notebook)
        office_frame = ttk.Frame(self.inst_notebook)
        edu_frame = ttk.Frame(self.inst_notebook)
        gaming_frame = ttk.Frame(self.inst_notebook)

        store_frame.pack(fill="both", expand=True)
        browser_frame.pack(fill="both", expand=True)
        office_frame.pack(fill="both", expand=True)
        edu_frame.pack(fill="both", expand=True)
        gaming_frame.pack(fill="both", expand=True)

        # add frames to notebook
        self.inst_notebook.add(store_frame, compound=LEFT, text="Start")
        self.inst_notebook.add(office_frame, compound=LEFT, text="Textverarbeitung")
        self.inst_notebook.add(edu_frame, compound=LEFT, text="Bildbearbeitung")
        self.inst_notebook.add(browser_frame, compound=LEFT, text="Browser")
        self.inst_notebook.add(gaming_frame, compound=LEFT, text="Gaming")

        store_note_frame = StorePanel(store_frame)
        store_note_frame.pack(fill=tk.BOTH, expand=True)

        browser_note_frame = BrowserPanel(browser_frame)
        browser_note_frame.pack(fill=tk.BOTH, expand=True)

        office_note_frame = OfficePanel(office_frame)
        office_note_frame.pack(fill=tk.BOTH, expand=True)

        edu_note_frame = EduPanel(edu_frame)
        edu_note_frame.pack(fill=tk.BOTH, expand=True)

        gaming_note_frame = GamingPanel(gaming_frame)
        gaming_note_frame.pack(fill=tk.BOTH, expand=True)


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
        store_btn_frame.pack(pady=20, padx=20, fill="x")

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
        # refresh_flatpak_installs()

        self.office_btn0_icon = PhotoImage(
            file=SoftwareOffice.office_dict["office_0"]["Icon"]
        )

        # self.office_btn2_icon = PhotoImage(
        #    file=SoftwareOffice.office_dict["office_2"]["Icon"]
        # )

        # elf.office_btn3_icon = PhotoImage(
        #    file=SoftwareOffice.office_dict["office_3"]["Icon"]
        # )

        # self.office_btn4_icon = PhotoImage(
        #    file=SoftwareOffice.office_dict["office_4"]["Icon"]
        # )

        # Create the button frame first

        def show_button_frame():
            office_btn_frame.pack(pady=20, padx=20, fill="x")
            back_button.pack_forget()
            office_detail_frame.pack_forget()

        def hide_button_frame():
            office_btn_frame.pack_forget()
            back_button.pack(pady=20, padx=20, fill="x")

        back_button = ttk.Button(self, text="Zurück", command=show_button_frame)

        office_btn_frame = ttk.LabelFrame(self, text="Office-Auswahl", padding=20)
        office_btn_frame.pack(pady=20, padx=20, fill="x")

        office_btn_frame.grid_columnconfigure(0, weight=1)
        office_btn_frame.grid_columnconfigure(1, weight=1)
        office_btn_frame.grid_columnconfigure(2, weight=1)
        office_btn_frame.grid_columnconfigure(3, weight=1)
        office_btn_frame.grid_columnconfigure(4, weight=1)

        def run_installation(office_key):
            # hide_apt_frame()
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareOffice.office_dict[office_key]["Name"]
            primo_skript = SoftwareOffice.office_dict[office_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.office_inst_btn.config(text="Deinstallieren")

            refresh_status(office_key)

        def run_uninstall(office_key):
            # hide_apt_frame()
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareOffice.office_dict[office_key]["Name"]
            primo_skript = SoftwareOffice.office_dict[office_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.office_inst_btn.config(text="Installieren")

            refresh_status(office_key)

        def refresh_status(office_key):
            office_name = SoftwareOffice.office_dict[office_key]["Name"]
            office_pakage = SoftwareOffice.office_dict[office_key]["Package"]
            office_disc = SoftwareOffice.office_dict[office_key]["Description"]
            office_path = SoftwareOffice.office_dict[office_key]["Path"]
            # APT-Pakete und Flatpak-Installationen überprüfen
            installed_apt = office_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `office_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = office_path in flatpak_installs.values()
            installed_snap = office_path in get_installed_snaps()
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if not installed_snap or installed_apt or installed_flatpak:
                print(f"{office_name} is not installed")
                self.office_inst_btn.config(
                    text="Installieren",
                    command=lambda: run_installation(office_key),
                    style="Green.TButton",
                )
            if installed_snap or installed_apt or installed_flatpak:
                print(f"{office_name} is installed")
                self.office_inst_btn.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(office_key),
                    style="Red.TButton",
                )
            else:
                print(f"{office_name} is not installed")
                self.office_inst_btn.config(
                    text="Installieren",
                    command=lambda: run_installation(office_key),
                    style="Green.TButton",
                )

        def office_btn_action(office_key):
            # Den Namen des Spiels aus der SoftwareOffice-Klasse holen
            office_name = SoftwareOffice.office_dict[office_key]["Name"]
            office_pakage = SoftwareOffice.office_dict[office_key]["Package"]
            office_disc = SoftwareOffice.office_dict[office_key]["Description"]
            office_path = SoftwareOffice.office_dict[office_key]["Path"]
            office_thumb = SoftwareOffice.office_dict[office_key]["Thumbnail"]
            hide_button_frame()
            office_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            self.office_thumb = PhotoImage(file=office_thumb)

            self.office_name.config(text=f"Name: {office_name}")
            self.office_pak.config(text=f"Paket: {office_pakage}")
            self.office_desc.config(text=f"Beschreibung: {office_disc}")

            self.office_inst_btn.grid(column=1, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=2, row=3)
            self.thumb_lbl.configure(image=self.office_thumb)
            self.thumb_lbl.pack()

            print(get_installed_snaps())
            refresh_status(office_key)

        office0_button = ttk.Button(
            office_btn_frame,
            text=SoftwareOffice.office_dict["office_0"]["Name"],
            image=self.office_btn0_icon,
            command=lambda: office_btn_action("office_0"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        office0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        # office2_button = ttk.Button(
        #     office_btn_frame,
        #     text=SoftwareOffice.office_dict["office_2"]["Name"],
        #     image=self.office_btn2_icon,
        #     command=lambda: office_btn_action("office_2"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # office2_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        # office3_button = ttk.Button(
        #     office_btn_frame,
        #     text=SoftwareOffice.office_dict["office_3"]["Name"],
        #     image=self.office_btn3_icon,
        #     command=lambda: office_btn_action("office_3"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # office3_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        # office4_button = ttk.Button(
        #     office_btn_frame,
        #     text=SoftwareOffice.office_dict["office_4"]["Name"],
        #     image=self.office_btn4_icon,
        #     command=lambda: open_website("office_4"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # office4_button.grid(row=0, column=4, padx=5, pady=5, sticky="nesw")
        # print(SoftwareOffice.office_dict)

        # Create the detail frame
        office_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        office_detail_frame.grid_columnconfigure(0, weight=1)
        office_detail_frame.grid_columnconfigure(1, weight=1)
        office_detail_frame.grid_rowconfigure(3, weight=1)

        self.office_name = Label(
            office_detail_frame, text="", justify="left", anchor="w"
        )
        self.office_name.grid(column=0, row=0, sticky="ew")

        self.office_pak = Label(
            office_detail_frame, text="", justify="left", anchor="w"
        )
        self.office_pak.grid(column=0, row=1, sticky="ew")
        self.office_desc = Label(
            office_detail_frame, text="", justify="left", anchor="w", wraplength=600
        )
        self.office_desc.grid(column=0, row=2, sticky="ew")

        self.office_inst_btn = ttk.Button(
            office_detail_frame, text="Install", style="Custom.TButton"
        )

        # Initialize termf and pack it below the install button
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
        # refresh_flatpak_installs()

        self.game_btn0_icon = PhotoImage(file=SoftwareGame.game_dict["game_0"]["Icon"])

        self.game_btn1_icon = PhotoImage(file=SoftwareGame.game_dict["game_1"]["Icon"])

        self.game_btn2_icon = PhotoImage(file=SoftwareGame.game_dict["game_2"]["Icon"])

        self.game_btn3_icon = PhotoImage(file=SoftwareGame.game_dict["game_3"]["Icon"])

        self.game_btn4_icon = PhotoImage(file=SoftwareGame.game_dict["game_4"]["Icon"])

        self.game_btn5_icon = PhotoImage(file=SoftwareGame.game_dict["game_5"]["Icon"])

        self.game_btn6_icon = PhotoImage(file=SoftwareGame.game_dict["game_6"]["Icon"])

        self.game_btn7_icon = PhotoImage(file=SoftwareGame.game_dict["game_7"]["Icon"])

        self.game_btn8_icon = PhotoImage(file=SoftwareGame.game_dict["game_8"]["Icon"])

        self.game_btn9_icon = PhotoImage(file=SoftwareGame.game_dict["game_9"]["Icon"])

        def show_button_frame():
            game_btn_frame.pack(pady=20, padx=20, fill="x")
            back_button.pack_forget()
            game_detail_frame.pack_forget()

        def hide_button_frame():
            game_btn_frame.pack_forget()
            back_button.pack(pady=20, padx=20, fill="x")

        back_button = ttk.Button(self, text="Zurück", command=show_button_frame)

        # Create the button frame first
        game_btn_frame = ttk.LabelFrame(self, text="Gaming Empfehlungen", padding=20)
        game_btn_frame.pack(pady=20, padx=20, fill="x")

        game_btn_frame.grid_columnconfigure(0, weight=2)
        game_btn_frame.grid_columnconfigure(1, weight=2)
        game_btn_frame.grid_columnconfigure(2, weight=2)
        game_btn_frame.grid_columnconfigure(3, weight=1)
        game_btn_frame.grid_columnconfigure(4, weight=2)

        def run_installation(game_key):
            # hide_apt_frame()
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            primo_skript = SoftwareGame.game_dict[game_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.gaming_inst_btn.config(text="Deinstallieren")

            refresh_status(game_key)

        def run_uninstall(game_key):
            # hide_apt_frame()
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareGame.game_dict[game_key]["Name"]
            primo_skript = SoftwareGame.game_dict[game_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.gaming_inst_btn.config(text="Installieren")

            refresh_status(game_key)

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
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if installed_apt or installed_flatpak:
                print(f"{game_name} is installed")
                self.gaming_inst_btn.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(game_key),
                    style="Red.TButton",
                )
            else:
                print(f"{game_name} is not installed")
                self.gaming_inst_btn.config(
                    text="Installieren",
                    command=lambda: run_installation(game_key),
                    style="Green.TButton",
                )

        def game_btn_action(game_key):
            # Den Namen des Spiels aus der SoftwareGame-Klasse holen
            game_name = SoftwareGame.game_dict[game_key]["Name"]
            game_pakage = SoftwareGame.game_dict[game_key]["Package"]
            game_disc = SoftwareGame.game_dict[game_key]["Description"]
            game_path = SoftwareGame.game_dict[game_key]["Path"]
            game_thumb = SoftwareGame.game_dict[game_key]["Thumbnail"]

            self.game_thumb = PhotoImage(file=game_thumb)

            self.gaming_name.config(text=f"Name: {game_name}")
            self.gaming_pak.config(text=f"Paket: {game_pakage}")
            self.gaming_desc.config(text=f"Beschreibung: {game_disc}")

            self.gaming_inst_btn.grid(column=1, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=2, row=3)
            self.thumb_lbl.configure(image=self.game_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            game_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # print(get_installed_apt_pkgs())
            refresh_status(game_key)

        game0_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_0"]["Name"],
            image=self.game_btn0_icon,
            command=lambda: game_btn_action("game_0"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        game1_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_1"]["Name"],
            image=self.game_btn1_icon,
            command=lambda: game_btn_action("game_1"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game1_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        game2_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_2"]["Name"],
            image=self.game_btn2_icon,
            command=lambda: game_btn_action("game_2"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game2_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        game3_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_3"]["Name"],
            image=self.game_btn3_icon,
            command=lambda: game_btn_action("game_3"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game3_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        game4_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_4"]["Name"],
            image=self.game_btn4_icon,
            command=lambda: open_website("game_4"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game4_button.grid(row=0, column=4, padx=5, pady=5, sticky="nesw")

        game5_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_5"]["Name"],
            image=self.game_btn5_icon,
            command=lambda: game_btn_action("game_5"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game5_button.grid(row=1, column=0, padx=5, pady=5, sticky="nesw")

        game6_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_6"]["Name"],
            image=self.game_btn6_icon,
            command=lambda: game_btn_action("game_6"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game6_button.grid(row=1, column=1, padx=5, pady=5, sticky="nesw")

        game7_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_7"]["Name"],
            image=self.game_btn7_icon,
            command=lambda: game_btn_action("game_7"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game7_button.grid(row=1, column=2, padx=5, pady=5, sticky="nesw")
        # print(SoftwareGame.game_dict)
        game8_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_8"]["Name"],
            image=self.game_btn8_icon,
            command=lambda: game_btn_action("game_8"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game8_button.grid(row=1, column=3, padx=5, pady=5, sticky="nesw")

        game9_button = ttk.Button(
            game_btn_frame,
            text=SoftwareGame.game_dict["game_9"]["Name"],
            image=self.game_btn9_icon,
            command=lambda: game_btn_action("game_9"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        game9_button.grid(row=1, column=4, padx=5, pady=5, sticky="nesw")

        # Create the detail frame
        game_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)
        # game_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

        game_detail_frame.grid_columnconfigure(0, weight=1)
        game_detail_frame.grid_columnconfigure(1, weight=1)
        game_detail_frame.grid_rowconfigure(3, weight=1)

        self.gaming_name = Label(game_detail_frame, text="", justify="left", anchor="w")
        self.gaming_name.grid(column=0, row=0, sticky="ew")

        self.gaming_pak = Label(game_detail_frame, text="", justify="left", anchor="w")
        self.gaming_pak.grid(column=0, row=1, sticky="ew")
        self.gaming_desc = Label(
            game_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.gaming_desc.grid(column=0, row=2, columnspan=2, sticky="ew")

        self.gaming_inst_btn = ttk.Button(
            game_detail_frame, text="Install", style="Custom.TButton"
        )

        # Initialize termf and pack it below the install button
        self.termf = Frame(
            game_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global game_wid
        game_wid = self.termf.winfo_id()


class BrowserPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000
        # refresh_flatpak_installs()

        self.browser_btn0_icon = PhotoImage(
            file=SoftwareBrowser.browser_dict["browser_0"]["Icon"]
        )

        self.browser_btn1_icon = PhotoImage(
            file=SoftwareBrowser.browser_dict["browser_1"]["Icon"]
        )

        # self.browser_btn2_icon = PhotoImage(
        #    file=SoftwareBrowser.browser_dict["browser_2"]["Icon"]
        # )

        # elf.browser_btn3_icon = PhotoImage(
        #    file=SoftwareBrowser.browser_dict["browser_3"]["Icon"]
        # )

        # self.browser_btn4_icon = PhotoImage(
        #    file=SoftwareBrowser.browser_dict["browser_4"]["Icon"]
        # )

        # Create the button frame first
        browser_btn_frame = ttk.LabelFrame(self, text="Browser-Auswahl", padding=20)
        browser_btn_frame.pack(pady=20, padx=20, fill="x")

        browser_btn_frame.grid_columnconfigure(0, weight=1)
        browser_btn_frame.grid_columnconfigure(1, weight=1)
        browser_btn_frame.grid_columnconfigure(2, weight=1)
        browser_btn_frame.grid_columnconfigure(3, weight=1)
        browser_btn_frame.grid_columnconfigure(4, weight=1)

        def run_installation(browser_key):
            # hide_apt_frame()
            primo_skript_task = "Installation ..."
            primo_skript_task_app = SoftwareBrowser.browser_dict[browser_key]["Name"]
            primo_skript = SoftwareBrowser.browser_dict[browser_key]["Install"]
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.browser_inst_btn.config(text="Deinstallieren")

            refresh_status(browser_key)

        def run_uninstall(browser_key):
            # hide_apt_frame()
            primo_skript_task = "Deinstallation ..."
            primo_skript_task_app = SoftwareBrowser.browser_dict[browser_key]["Name"]
            primo_skript = SoftwareBrowser.browser_dict[browser_key]["Uninstall"]

            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, primo_skript_task_app, primo_skript
            )
            self.master.wait_window(custom_installer)
            self.browser_inst_btn.config(text="Installieren")

            refresh_status(browser_key)

        def refresh_status(browser_key):
            browser_name = SoftwareBrowser.browser_dict[browser_key]["Name"]
            browser_pakage = SoftwareBrowser.browser_dict[browser_key]["Package"]
            browser_disc = SoftwareBrowser.browser_dict[browser_key]["Description"]
            browser_path = SoftwareBrowser.browser_dict[browser_key]["Path"]
            # APT-Pakete und Flatpak-Installationen überprüfen
            installed_apt = browser_path in get_installed_apt_pkgs()

            # Flatpak-Installationen abrufen und prüfen, ob der `browser_path` in den Werten vorhanden ist
            flatpak_installs = refresh_flatpak_installs()  # Funktion korrekt aufrufen
            installed_flatpak = browser_path in flatpak_installs.values()
            installed_snap = browser_path in get_installed_snaps()
            # self.master.wait_window(custom_installer)
            # Wenn das Spiel als APT-Paket oder Flatpak installiert ist
            if not installed_snap or installed_apt or installed_flatpak:
                print(f"{browser_name} is not installed")
                self.browser_inst_btn.config(
                    text="Installieren",
                    command=lambda: run_installation(browser_key),
                    style="Green.TButton",
                )
            if installed_snap or installed_apt or installed_flatpak:
                print(f"{browser_name} is installed")
                self.browser_inst_btn.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(browser_key),
                    style="Red.TButton",
                )
            else:
                print(f"{browser_name} is not installed")
                self.browser_inst_btn.config(
                    text="Installieren",
                    command=lambda: run_installation(browser_key),
                    style="Green.TButton",
                )

        def browser_btn_action(browser_key):
            # Den Namen des Spiels aus der SoftwareBrowser-Klasse holen
            browser_name = SoftwareBrowser.browser_dict[browser_key]["Name"]
            browser_pakage = SoftwareBrowser.browser_dict[browser_key]["Package"]
            browser_disc = SoftwareBrowser.browser_dict[browser_key]["Description"]
            browser_path = SoftwareBrowser.browser_dict[browser_key]["Path"]
            browser_thumb = SoftwareBrowser.browser_dict[browser_key]["Thumbnail"]

            self.browser_thumb = PhotoImage(file=browser_thumb)

            self.browser_name.config(text=f"Name: {browser_name}")
            self.browser_pak.config(text=f"Paket: {browser_pakage}")
            self.browser_desc.config(text=f"Beschreibung: {browser_disc}")

            self.browser_inst_btn.grid(column=1, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=2, row=3)
            self.thumb_lbl.configure(image=self.browser_thumb)
            self.thumb_lbl.pack()

            print(get_installed_snaps())
            refresh_status(browser_key)

        browser0_button = ttk.Button(
            browser_btn_frame,
            text=SoftwareBrowser.browser_dict["browser_0"]["Name"],
            image=self.browser_btn0_icon,
            command=lambda: browser_btn_action("browser_0"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        browser0_button.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

        browser1_button = ttk.Button(
            browser_btn_frame,
            text=SoftwareBrowser.browser_dict["browser_1"]["Name"],
            image=self.browser_btn1_icon,
            command=lambda: browser_btn_action("browser_1"),
            compound=tk.TOP,
            style="Custom.TButton",
        )
        browser1_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        # browser2_button = ttk.Button(
        #     browser_btn_frame,
        #     text=SoftwareBrowser.browser_dict["browser_2"]["Name"],
        #     image=self.browser_btn2_icon,
        #     command=lambda: browser_btn_action("browser_2"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # browser2_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        # browser3_button = ttk.Button(
        #     browser_btn_frame,
        #     text=SoftwareBrowser.browser_dict["browser_3"]["Name"],
        #     image=self.browser_btn3_icon,
        #     command=lambda: browser_btn_action("browser_3"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # browser3_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        # browser4_button = ttk.Button(
        #     browser_btn_frame,
        #     text=SoftwareBrowser.browser_dict["browser_4"]["Name"],
        #     image=self.browser_btn4_icon,
        #     command=lambda: open_website("browser_4"),
        #     compound=tk.TOP,
        #     style="Custom.TButton"
        # )
        # browser4_button.grid(row=0, column=4, padx=5, pady=5, sticky="nesw")
        # print(SoftwareBrowser.browser_dict)

        # Create the detail frame
        browser_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)
        browser_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

        browser_detail_frame.grid_columnconfigure(0, weight=1)
        browser_detail_frame.grid_columnconfigure(1, weight=1)
        browser_detail_frame.grid_rowconfigure(3, weight=1)

        self.browser_name = Label(
            browser_detail_frame, text="", justify="left", anchor="w"
        )
        self.browser_name.grid(column=0, row=0, sticky="ew")

        self.browser_pak = Label(
            browser_detail_frame, text="", justify="left", anchor="w"
        )
        self.browser_pak.grid(column=0, row=1, sticky="ew")
        self.browser_desc = Label(
            browser_detail_frame, text="", justify="left", anchor="w", wraplength=600
        )
        self.browser_desc.grid(column=0, row=2, sticky="ew")

        self.browser_inst_btn = ttk.Button(
            browser_detail_frame, text="Install", style="Custom.TButton"
        )

        # Initialize termf and pack it below the install button
        self.termf = Frame(
            browser_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global browser_wid
        browser_wid = self.termf.winfo_id()


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
