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
    SoftwareAudioVideo,
    SoftwareImageEditing,
)
from apt_manage import *
from snap_manage import *
from flatpak_manage import flatpak_path
from flatpak_manage import Flat_remote_dict
from flatpak_manage import refresh_flatpak_installs
from software import InstallableAppFactory, InstallableApp


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
        logger.error(f"Error executing the command: {e.stderr}")
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
        logger.info("Standard-Screenshot-URL für {}:".format(app_id))
        logger.info(screenshot_url)

    else:
        logger.warning("Kein Standard-Screenshot gefunden für {}.".format(app_id))


class SoftwareTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")


        if "dark" in theme_name or "Dark" in theme_name:
            self.deb_nav = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/debian_dark_24x24.png"
            )

            self.flatpak_nav = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/flatpak_dark_24x24.png"
            )

        else:
            self.deb_nav = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/debian_light_24x24.png"
            )

            self.flatpak_nav = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/flatpak_light_24x24.png"
            )

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        com_frame = ttk.Frame(self.inst_notebook)
        office_frame = ttk.Frame(self.inst_notebook)
        av_frame = ttk.Frame(self.inst_notebook)
        image_frame = ttk.Frame(self.inst_notebook)
        gaming_frame = ttk.Frame(self.inst_notebook)
        #apt_frame = ttk.Frame(self.inst_notebook)
        #flat_frame = ttk.Frame(self.inst_notebook)


        com_frame.pack(fill="both", expand=True)
        office_frame.pack(fill="both", expand=True)
        av_frame.pack(fill="both", expand=True)
        image_frame.pack(fill="both", expand=True)
        gaming_frame.pack(fill="both", expand=True)
        #apt_frame.pack(fill="both", expand=True)
        #flat_frame.pack(fill="both", expand=True)


        self.inst_notebook.add(com_frame, compound=LEFT, text="Web & Chat")
        self.inst_notebook.add(office_frame, compound=LEFT, text="Büro")
        self.inst_notebook.add(av_frame, compound=LEFT, text="Audio & Video")
        self.inst_notebook.add(image_frame, compound=LEFT, text="Bildbearbeitung")
        self.inst_notebook.add(gaming_frame, compound=LEFT, text="Gaming")
        #self.inst_notebook.add(apt_frame, compound=LEFT, text="APT Store",image=self.deb_nav)
        #self.inst_notebook.add(flat_frame, compound=LEFT, text="Flatpak Store",image=self.flatpak_nav)


        com_note_frame = ComPanel(com_frame)
        com_note_frame.pack(fill=tk.BOTH, expand=True)

        office_note_frame = OfficePanel(office_frame)
        office_note_frame.pack(fill=tk.BOTH, expand=True)

        av_note_frame = AVPanel(av_frame)
        av_note_frame.pack(fill=tk.BOTH, expand=True)

        image_note_frame = ImageEditingPanel(image_frame)
        image_note_frame.pack(fill=tk.BOTH, expand=True)

        gaming_note_frame = GamingPanel(gaming_frame)
        gaming_note_frame.pack(fill=tk.BOTH, expand=True)

        #apt_search_panel = AptSearchPanel(apt_frame)
        #apt_search_panel.pack(fill=tk.BOTH, expand=True)

        #flatpack_search_panel = FlatpakSearchPanel(flat_frame)
        #flatpack_search_panel.pack(fill=tk.BOTH, expand=True)


class OfficePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            office_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            office_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            office_detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            office_btn_frame.pack_forget()
            office_ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        # Funktion für das Hover-Ereignis
        def on_hover( event, key):
            office_ttp_label.configure(text=SoftwareOffice.office_dict[key]["Description"])

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            office_ttp_label.configure(text="\n\n\n")

        def open_gnome_software():
            subprocess.Popen("env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY gnome-software", shell=True)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")

        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        office_btn_frame = ttk.LabelFrame(self, text="Büro | Empfehlungen", padding=20)
        office_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        office_btn_frame.grid_columnconfigure(0, weight=1)
        office_btn_frame.grid_columnconfigure(1, weight=1)
        office_btn_frame.grid_columnconfigure(2, weight=1)
        office_btn_frame.grid_columnconfigure(3, weight=1)
        office_btn_frame.grid_columnconfigure(4, weight=1)

        office_ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        office_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")

        office_ttp_label = ttk.Label(
            office_ttp_frame, text="\n\n\n", padding=20, wraplength=700
        )
        office_ttp_label.pack(fill="x", side="bottom")

        def run_installation(app):
            primo_skript_task = "Installation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_install_command()
            )
            self.master.wait_window(custom_installer)
            self.office_detail_inst.config(text="Deinstallieren")

            refresh_status(app)

        def run_uninstall(app):
            primo_skript_task = "Deinstallation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_uninstall_command()
            )
            self.master.wait_window(custom_installer)
            self.office_detail_inst.config(text="Installieren")

            refresh_status(app)

        def open_website(office_key):
            path = SoftwareOffice.office_dict[office_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(app):
            if (app.is_installed()):
                self.office_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(app),
                    style="Red.TButton",
                )
            else:
                self.office_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(app),
                    style="Green.TButton",
                )

        def office_btn_action(office_key):
            app = InstallableAppFactory.create(
                type=SoftwareOffice.office_dict[office_key]["Package"],
                name=SoftwareOffice.office_dict[office_key]["Name"],
                icon=SoftwareOffice.office_dict[office_key]["Icon"],
                description=SoftwareOffice.office_dict[office_key]["Description"],
                path=SoftwareOffice.office_dict[office_key]["Path"],
                thumbnail=SoftwareOffice.office_dict[office_key]["Thumbnail"],
                install_command=SoftwareOffice.office_dict[office_key]["Install"],
                uninstall_command=SoftwareOffice.office_dict[office_key]["Uninstall"],
            )


            thumb_img = Image.open(app.get_thumbnail())
            resized_thumb_img = resize700(thumb_img)
            self.office_thumb = ImageTk.PhotoImage(resized_thumb_img)

            icon_img = Image.open(app.get_icon())
            resized_icon_img = resize46(icon_img)
            self.office_icon = ImageTk.PhotoImage(resized_icon_img)

            self.office_detail_icon.configure(image=self.office_icon)
            self.office_detail_name.config(text=f"{app.get_name()}")
            self.office_detail_pak.config(text=f"{app.get_type()}")
            self.office_detail_desc.config(text=f"\n{app.get_description()}")

            self.office_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.office_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            office_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            refresh_status(app)

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
            office_button.bind("<Enter>", lambda event, key=office_key: on_hover(event, key))
            office_button.bind("<Leave>", on_leave)

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


class ImageEditingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            img_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            img_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            img_detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            img_btn_frame.pack_forget()
            img_ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        # Funktion für das Hover-Ereignis
        def on_hover( event, key):
            img_ttp_label.configure(text=SoftwareImageEditing.img_dict[key]["Description"])

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            img_ttp_label.configure(text="\n\n\n")

        def open_gnome_software():
            subprocess.Popen("gnome-software", shell=True)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")

        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        img_btn_frame = ttk.LabelFrame(self, text="Bildbearbeitung | Empfehlungen", padding=20)
        img_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        img_btn_frame.grid_columnconfigure(0, weight=1)
        img_btn_frame.grid_columnconfigure(1, weight=1)
        img_btn_frame.grid_columnconfigure(2, weight=1)
        img_btn_frame.grid_columnconfigure(3, weight=1)
        img_btn_frame.grid_columnconfigure(4, weight=1)

        img_ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        img_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")

        img_ttp_label = ttk.Label(
            img_ttp_frame, text="\n\n", padding=20, wraplength=700
        )
        img_ttp_label.pack(fill="x", side="bottom")


        def run_installation(app):
            primo_skript_task = "Installation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_install_command()
            )
            self.master.wait_window(custom_installer)
            self.img_detail_inst.config(text="Deinstallieren")

            refresh_status(app)

        def run_uninstall(app):
            primo_skript_task = "Deinstallation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_uninstall_command()
            )
            self.master.wait_window(custom_installer)
            self.img_detail_inst.config(text="Installieren")

            refresh_status(app)

        def open_website(img_key):
            path = SoftwareImageEditing.img_dict[img_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(app):
            if (app.is_installed()):
                logger.info(f"{app.get_name()} is installed")
                self.img_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(app),
                    style="Red.TButton",
                )
            else:
                logger.info(f"{app.get_name()} is not installed")
                self.img_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(app),
                    style="Green.TButton",
                )

        def img_btn_action(img_key):
            app = InstallableAppFactory.create(
                type=SoftwareImageEditing.img_dict[img_key]["Package"],
                name=SoftwareImageEditing.img_dict[img_key]["Name"],
                icon=SoftwareImageEditing.img_dict[img_key]["Icon"],
                description=SoftwareImageEditing.img_dict[img_key]["Description"],
                path=SoftwareImageEditing.img_dict[img_key]["Path"],
                thumbnail=SoftwareImageEditing.img_dict[img_key]["Thumbnail"],
                install_command=SoftwareImageEditing.img_dict[img_key]["Install"],
                uninstall_command=SoftwareImageEditing.img_dict[img_key]["Uninstall"],
            )


            thumb_img = Image.open(app.get_thumbnail())
            resized_thumb_img = resize700(thumb_img)
            self.img_thumb = ImageTk.PhotoImage(resized_thumb_img)

            icon_img = Image.open(app.get_icon())
            resized_icon_img = resize46(icon_img)
            self.img_icon = ImageTk.PhotoImage(resized_icon_img)

            self.img_detail_icon.configure(image=self.img_icon)
            self.img_detail_name.config(text=f"{app.get_name()}")
            self.img_detail_pak.config(text=f"{app.get_type()}")
            self.img_detail_desc.config(text=f"\n{app.get_description()}")

            self.img_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.img_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            img_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            refresh_status(app)

        self.img_btn_icons = []

        for i, (img_key, img_info) in enumerate(SoftwareImageEditing.img_dict.items()):
            img = Image.open(img_info["Icon"])
            resized_img = resize46(img)
            icon = ImageTk.PhotoImage(resized_img)
            self.img_btn_icons.append(icon)

        max_columns = 5

        for i, (img_key, img_info) in enumerate(SoftwareImageEditing.img_dict.items()):
            row = i // max_columns
            column = i % max_columns

            img_button = ttk.Button(
                img_btn_frame,
                text=img_info["Name"],
                image=self.img_btn_icons[i],
                command=lambda key=img_key: img_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=20,
            )
            img_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")
            img_button.bind("<Enter>", lambda event, key=img_key: on_hover(event, key))
            img_button.bind("<Leave>", on_leave)

        img_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        img_detail_frame.grid_columnconfigure(1, weight=1)
        img_detail_frame.grid_rowconfigure(3, weight=1)

        self.img_detail_icon = Label(
            img_detail_frame,
        )
        self.img_detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.img_detail_name = Label(
            img_detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.img_detail_name.grid(column=1, row=0, sticky="w")

        self.img_detail_pak = Label(
            img_detail_frame, text="", justify="left", anchor="w"
        )
        self.img_detail_pak.grid(column=1, row=1, sticky="we")

        self.img_detail_desc = Label(
            img_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.img_detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.img_detail_inst = ttk.Button(
            img_detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            img_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global img_wid
        img_wid = self.termf.winfo_id()


class GamingPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            game_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            game_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            game_detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            game_btn_frame.pack_forget()
            game_ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        # Funktion für das Hover-Ereignis
        def on_hover( event, key):
            game_ttp_label.configure(text=SoftwareGame.game_dict[key]["Description"])

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            game_ttp_label.configure(text="\n\n\n")

        def open_gnome_software():
            subprocess.Popen("gnome-software", shell=True)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")

        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        game_btn_frame = ttk.LabelFrame(self, text="Gaming | Empfehlungen", padding=20)
        game_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        game_btn_frame.grid_columnconfigure(0, weight=1)
        game_btn_frame.grid_columnconfigure(1, weight=1)
        game_btn_frame.grid_columnconfigure(2, weight=1)
        game_btn_frame.grid_columnconfigure(3, weight=1)
        game_btn_frame.grid_columnconfigure(4, weight=1)

        game_ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        game_ttp_frame.pack(pady=20, padx=20,fill="x")

        game_ttp_label = ttk.Label(
            game_ttp_frame, text="\n\n\n", padding=20, wraplength=700
        )
        game_ttp_label.pack(fill="x")

        def run_installation(app: InstallableApp):
            primo_skript_task = "Installation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_install_command()
            )
            self.master.wait_window(custom_installer)
            self.game_detail_inst.config(text="Deinstallieren")

            refresh_status(app)

        def run_uninstall(app: InstallableApp):
            primo_skript_task = "Deinstallation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_uninstall_command()
            )
            self.master.wait_window(custom_installer)
            self.game_detail_inst.config(text="Installieren")

            refresh_status(app)

        def open_website(game_key):
            path = SoftwareGame.game_dict[game_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(app: InstallableApp):
            if (app.is_installed()):
                logger.info(f"{app.get_name()} is installed")
                self.game_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(app),
                    style="Red.TButton",
                )
            else:
                logger.info(f"{app.get_name()} is not installed")
                self.game_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(app),
                    style="Green.TButton",
                )

        def game_btn_action(game_key):
            logger.info("game_btn_action", game_key)

            app = InstallableAppFactory.create(
                type=SoftwareGame.game_dict[game_key]["Package"],
                name=SoftwareGame.game_dict[game_key]["Name"],
                icon=SoftwareGame.game_dict[game_key]["Icon"],
                description=SoftwareGame.game_dict[game_key]["Description"],
                path=SoftwareGame.game_dict[game_key]["Path"],
                thumbnail=SoftwareGame.game_dict[game_key]["Thumbnail"],
                install_command=SoftwareGame.game_dict[game_key]["Install"],
                uninstall_command=SoftwareGame.game_dict[game_key]["Uninstall"],
            )


            thumb_img = Image.open(app.get_thumbnail())
            resized_thumb_img = resize700(thumb_img)
            self.game_thumb = ImageTk.PhotoImage(resized_thumb_img)

            icon_img = Image.open(app.get_icon())
            resized_icon_img = resize46(icon_img)
            self.game_icon = ImageTk.PhotoImage(resized_icon_img)

            self.game_detail_icon.configure(image=self.game_icon)
            self.game_detail_name.config(text=f"{app.get_name()}")
            self.game_detail_pak.config(text=f"{app.get_type()}")
            self.game_detail_desc.config(text=f"\n{app.get_description()}")

            self.game_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.game_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            game_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            refresh_status(app)

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
            game_button.bind("<Enter>", lambda event, key=game_key: on_hover(event, key))
            game_button.bind("<Leave>", on_leave)

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


class AVPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            av_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            av_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            av_detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            av_btn_frame.pack_forget()
            av_ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        # Funktion für das Hover-Ereignis
        def on_hover( event, key):
            av_ttp_label.configure(text=SoftwareAudioVideo.av_dict[key]["Description"])

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            av_ttp_label.configure(text="\n\n\n")

        def open_gnome_software():
            subprocess.Popen("gnome-software", shell=True)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")


        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        av_btn_frame = ttk.LabelFrame(self, text="Audio/Video | Empfehlungen", padding=20)
        av_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        av_btn_frame.grid_columnconfigure(0, weight=1)
        av_btn_frame.grid_columnconfigure(1, weight=1)
        av_btn_frame.grid_columnconfigure(2, weight=1)
        av_btn_frame.grid_columnconfigure(3, weight=1)
        av_btn_frame.grid_columnconfigure(4, weight=1)

        av_ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        av_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")

        av_ttp_label = ttk.Label(
            av_ttp_frame, text="\n\n\n", padding=20, wraplength=700
        )
        av_ttp_label.pack(fill="x", side="bottom")

        def run_installation(app: InstallableApp):
            primo_skript_task = "Installation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_install_command()
            )
            self.master.wait_window(custom_installer)
            self.av_detail_inst.config(text="Deinstallieren")

            refresh_status(app)

        def run_uninstall(app: InstallableApp):
            primo_skript_task = "Deinstallation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_uninstall_command()
            )
            self.master.wait_window(custom_installer)
            self.av_detail_inst.config(text="Installieren")

            refresh_status(app)

        def open_website(av_key):
            path = SoftwareAudioVideo.av_dict[av_key]["Path"]
            subprocess.run(f'xdg-open "{path}"', shell=True)

        def refresh_status(app: InstallableApp):
            if app.is_installed():
                logger.info(f"{app.get_name()} is installed")
                self.av_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(app),
                    style="Red.TButton",
                )
            else:
                logger.info(f"{app.get_name()} is not installed")
                self.av_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(app),
                    style="Green.TButton",
                )

        def av_btn_action(av_key):
            app = InstallableAppFactory.create(
                type=SoftwareAudioVideo.av_dict[av_key]["Package"],
                name=SoftwareAudioVideo.av_dict[av_key]["Name"],
                icon=SoftwareAudioVideo.av_dict[av_key]["Icon"],
                description=SoftwareAudioVideo.av_dict[av_key]["Description"],
                path=SoftwareAudioVideo.av_dict[av_key]["Path"],
                thumbnail=SoftwareAudioVideo.av_dict[av_key]["Thumbnail"],
                install_command=SoftwareAudioVideo.av_dict[av_key]["Install"],
                uninstall_command=SoftwareAudioVideo.av_dict[av_key]["Uninstall"],
            )

            thumb_img = Image.open(app.get_thumbnail())
            resized_thumb_img = resize700(thumb_img)
            self.av_thumb = ImageTk.PhotoImage(resized_thumb_img)

            icon_img = Image.open(app.get_icon())
            resized_icon_img = resize46(icon_img)
            self.av_icon = ImageTk.PhotoImage(resized_icon_img)

            self.av_detail_icon.configure(image=self.av_icon)
            self.av_detail_name.config(text=f"{app.get_name()}")
            self.av_detail_pak.config(text=f"{app.get_type()}")
            self.av_detail_desc.config(text=f"\n{app.get_description()}")

            self.av_detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.av_thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            av_detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            refresh_status(app)

        self.av_btn_icons = []

        for i, (av_key, av_info) in enumerate(SoftwareAudioVideo.av_dict.items()):
            img = Image.open(av_info["Icon"])
            resized_img = resize46(img)
            icon = ImageTk.PhotoImage(resized_img)
            self.av_btn_icons.append(icon)

        max_columns = 5

        for i, (av_key, av_info) in enumerate(SoftwareAudioVideo.av_dict.items()):
            row = i // max_columns
            column = i % max_columns

            av_button = ttk.Button(
                av_btn_frame,
                text=av_info["Name"],
                image=self.av_btn_icons[i],
                command=lambda key=av_key: av_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=20,
            )
            av_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")
            av_button.bind("<Enter>", lambda event, key=av_key: on_hover(event, key))
            av_button.bind("<Leave>", on_leave)

        av_detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        av_detail_frame.grid_columnconfigure(1, weight=1)
        av_detail_frame.grid_rowconfigure(3, weight=1)

        self.av_detail_icon = Label(
            av_detail_frame,
        )
        self.av_detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.av_detail_name = Label(
            av_detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.av_detail_name.grid(column=1, row=0, sticky="w")

        self.av_detail_pak = Label(av_detail_frame, text="", justify="left", anchor="w")
        self.av_detail_pak.grid(column=1, row=1, sticky="we")

        self.av_detail_desc = Label(
            av_detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.av_detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.av_detail_inst = ttk.Button(
            av_detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            av_detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global av_wid
        av_wid = self.termf.winfo_id()


class ComPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            com_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            com_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            com_detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            com_btn_frame.pack_forget()
            com_ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        # Funktion für das Hover-Ereignis
        def on_hover( event, key):
            com_ttp_label.configure(text=SoftwareCommunication.com_dict[key]["Description"])

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            com_ttp_label.configure(text="\n\n\n")

        def open_gnome_software():
            subprocess.Popen("gnome-software", shell=True)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")

        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        com_btn_frame = ttk.LabelFrame(
            self, text="Web & Chat | Empfehlungen", padding=20
        )
        com_btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        com_ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        com_ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")

        com_ttp_label = ttk.Label(
            com_ttp_frame, text="\n\n\n", padding=20, wraplength=700
        )
        com_ttp_label.pack(fill="x", side="bottom")


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
            com_pakage = SoftwareCommunication.com_dict[com_key]["Package"].value
            com_disc = SoftwareCommunication.com_dict[com_key]["Description"]
            com_path = SoftwareCommunication.com_dict[com_key]["Path"]

            installed_apt = com_path in get_installed_apt_pkgs()

            flatpak_installs = refresh_flatpak_installs()
            installed_flatpak = com_path in flatpak_installs.values()
            installed_snap = com_path in get_installed_snaps()

            if installed_snap or installed_apt or installed_flatpak:
                logger.info(f"{com_name} is installed")
                self.com_detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(com_key),
                    style="Red.TButton",
                )
            else:
                logger.info(f"{com_name} is not installed")
                self.com_detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(com_key),
                    style="Green.TButton",
                )

        def com_btn_action(com_key):
            com_icon_img = SoftwareCommunication.com_dict[com_key]["Icon"]
            com_name = SoftwareCommunication.com_dict[com_key]["Name"]
            com_pakage = SoftwareCommunication.com_dict[com_key]["Package"].value
            com_disc = SoftwareCommunication.com_dict[com_key]["Description"]
            com_path = SoftwareCommunication.com_dict[com_key]["Path"]
            com_thumb = SoftwareCommunication.com_dict[com_key]["Thumbnail"]

            thumb_img = Image.open(com_thumb)
            resized_thumb_img = resize700(thumb_img)
            self.com_thumb = ImageTk.PhotoImage(resized_thumb_img)

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

            com_button.bind("<Enter>", lambda event, key=com_key: on_hover(event, key))
            com_button.bind("<Leave>", on_leave)

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
            pigro_skript_task = "Installation ..."
            pigro_skript_task_app = f"{apt_entry.get()}"
            pigro_skript = f"{permit} apt install -y {apt_entry.get()}"
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )
            self.master.wait_window(custom_installer)

        def apt_uninstall():
            hide_apt_frame()
            pigro_skript_task = "Deinstalltion ..."
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
                    logger.error(f"{e}")
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
                logger.error(f"{e}")
                if apt_entry.get() in apt_flatpak_matches:
                    try:
                        app_id = Flat_remote_dict[flatpak_entry.get()]
                        screenshot_url = extract_default_screenshot_url(app_id)
                        if screenshot_url:
                            logger.info("Screenshot-URL {}:".format(app_id))
                            logger.info(screenshot_url)
                        else:
                            logger.warning("No Screenshot Found {}.".format(app_id))

                        with urlopen(screenshot_url) as url_output:
                            self.img = Image.open(url_output)
                        self.img = resize(self.img)
                        self.img = ImageTk.PhotoImage(self.img)
                        apt_panel.config(image=self.img)

                    except requests.exceptions.RequestException as e:
                        logger.error("Error fetching URL:", e)
                        apt_panel.config(self.no_img)

                    except subprocess.CalledProcessError as err:
                        logger.error("Command returned non-zero exit status:", err)
                        if "returned non-zero exit status 4" in str(err):
                            try:
                                app_id += ".desktop"
                                screenshot_url = extract_default_screenshot_url(app_id)
                                if screenshot_url:
                                    logger.info("Screenshot-URL {}:".format(app_id))
                                    logger.info(screenshot_url)
                                else:
                                    logger.warning("No Screenshot Found {}.".format(app_id))

                                with urlopen(screenshot_url) as url_output:
                                    self.img = Image.open(url_output)
                                self.img = resize(self.img)
                                self.img = ImageTk.PhotoImage(self.img)
                                apt_panel.config(image=self.img)

                            except subprocess.CalledProcessError as err:
                                logger.error(
                                    "Command returned non-zero exit status again:", err
                                )
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
                        style="Red.TButton",
                    )
                else:
                    apt_pkg_inst.config(
                        text="Install",
                        width=10,
                        command=apt_install,
                        style="Green.TButton",
                    )

                apt_panel.config(image=self.no_img)

                hide_apt_search_container()
                get_debian_icon()
                apt_screenshot()
                put_apt_description()

        def hide_apt_frame():
            apt_info_container.pack_forget()
            apt_search_container.pack(
                anchor="w", pady=20, padx=10, fill=BOTH, expand=True
            )
            apt_info_throber_frame.pack(fill="x", pady=20, padx=10)

        apt_main_container = Frame(self)
        apt_main_container.pack(fill="both", expand=True)

        apt_search_container = ttk.LabelFrame(
            apt_main_container, text="Suche", padding=20
        )
        apt_search_container.pack(
            anchor="w", pady=20, padx=10, fill="both", expand=True
        )

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

        apt_entry = ttk.Entry(apt_search_field, font=("Sans", 15))
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
        apt_list_box.pack(fill=BOTH, expand=True)

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

        store_btn_frame = ttk.LabelFrame(
            apt_info_throber_frame, text="Softwareverwaltung", padding=20
        )
        store_btn_frame.pack(fill="x")

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

        apt_info_container = ttk.Frame(apt_main_container, padding=20)
        apt_info_container.columnconfigure(0, weight=1)
        apt_info_container.rowconfigure(2, weight=1)

        apt_exit = ttk.Button(
            apt_info_container,
            text="Zurück",
            #image=self.exit_btn,
            style="Custom.TButton",
            compound=LEFT,
            command=hide_apt_frame,
        )
        apt_exit.grid(row=0, column=0, sticky="e")

        apt_pkg_header_1 = ttk.LabelFrame(
            apt_info_container, text="Application", padding=20
        )
        apt_pkg_header_1.grid(row=1, column=0, sticky="ew")

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
            style="Green.TButton",
        )
        apt_pkg_inst.grid(row=0, column=2, sticky="e")

        apt_detail_frame = ttk.LabelFrame(
            apt_info_container, text="Details", padding=20
        )
        apt_detail_frame.grid(row=2, column=0, sticky="nsew")

        apt_detail_frame.columnconfigure(0, weight=1)
        apt_detail_frame.rowconfigure(0, weight=1)

        apt_canvas = Canvas(apt_detail_frame, borderwidth=0, highlightthickness=0)
        apt_canvas.grid(row=0, column=0, sticky="nsew")

        apt_canvas_scrollbar = ttk.Scrollbar(
            apt_detail_frame, orient="vertical", command=apt_canvas.yview
        )
        apt_canvas_scrollbar.grid(row=0, column=1, sticky="ns")

        apt_canvas.configure(yscrollcommand=apt_canvas_scrollbar.set)

        apt_canvas_frame = Frame(apt_canvas)
        apt_canvas.create_window((0, 0), window=apt_canvas_frame, anchor="nw")

        apt_canvas_frame.bind(
            "<Configure>",
            lambda e: apt_canvas.configure(scrollregion=apt_canvas.bbox("all")),
        )

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


class FlatpakSearchPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.no_img = PhotoImage(file=f"{application_path}/images/apps/no_image.png")

        if "dark" in theme or "noir" in theme:
            self.flatpak_butt = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/flatpak_dark_24x24.png"
            )
        else:
            self.flatpak_butt = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/flatpak_light_24x24.png"
            )
        self.flatpak_big_icon = PhotoImage(
            file=f"{application_path}/images/icons/flatpak-glogo.png"
        )

        self.debinstall_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/debian-logo.png"
        )
        self.search_btn = PhotoImage(
            file=f"{application_path}/images/icons/nav_bar/glass_icon.png"
        )
        self.exit_btn = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/exit_btn.png"
        )
        self.flatpak_appsinstall_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/flathub64x64.png"
        )

        def error_message_0():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        def error_message_1():
            e_mass = Error_Mass(self)
            e_mass.grab_set()

        def hide_flatpak_frame():
            flatpak_info_frame.pack_forget()
            flatpak_search_frame.pack(
                anchor="w", pady=20, padx=10, fill=BOTH, expand=True
            )
            flatpak_info_throber_frame.pack(fill="x", pady=20, padx=10)

        def flatpak_install():
            hide_flatpak_frame()

            pigro_skript_task = "Installation ..."
            pigro_skript_task_app = f"{flatpak_entry.get()}"
            pigro_skript =f"flatpak install -y flathub {Flat_remote_dict[flatpak_entry.get()]}"
            logger.info({Flat_remote_dict[flatpak_entry.get()]})
            custom_installer = Custom_Installer(master)

            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )

            update_flatpak(Flat_remote_dict.keys())

        def flatpak_uninstall():
            hide_flatpak_frame()

            pigro_skript_task = "Deinstallation ..."
            pigro_skript_task_app = f"{flatpak_entry.get()}"
            pigro_skript = f"flatpak uninstall {Flat_remote_dict[flatpak_entry.get()]} -y"
            logger.info({Flat_remote_dict[flatpak_entry.get()]})

            custom_installer = Custom_Installer(master)

            custom_installer.do_task(
                pigro_skript_task, pigro_skript_task_app, pigro_skript
            )

            update_flatpak(Flat_remote_dict.keys())

        def update_flatpak(flatpak_data):
            flatpak_data = sorted(flatpak_data)
            flatpak_list_box.delete(0, END)
            for item in flatpak_data:
                flatpak_list_box.insert(END, item)

        def flatpak_list_fillout(e):
            flatpak_entry.delete(0, END)
            flatpak_entry.insert(
                0, flatpak_list_box.get(flatpak_list_box.curselection())
            )
            flatpak_show_infos()

        def flatpak_search_check(e):
            typed = flatpak_entry.get()
            if typed == "":
                flatpak_data = Flat_remote_dict.keys()
            else:
                flatpak_data = []
                for item in Flat_remote_dict.keys():
                    if typed.lower() in item.lower():
                        flatpak_data.append(item)
            update_flatpak(flatpak_data)

        def get_flatpak_icon():
            try:
                url_output = f"https://dl.flathub.org/repo/appstream/x86_64/icons/128x128/{Flat_remote_dict[flatpak_entry.get()]}.png"
                with urlopen(url_output) as url_output:
                    self.flat_icon = Image.open(url_output)
                self.flat_icon = resize2(self.flat_icon)

                self.flat_icon = ImageTk.PhotoImage(self.flat_icon)
                flatpak_pkg_icon.config(image=self.flat_icon)
            except urllib.error.HTTPError as e:
                flatpak_pkg_icon.config(image=self.flatpak_appsinstall_icon)

        def get_flatpak_screenshot():
            try:
                app_id = Flat_remote_dict[flatpak_entry.get()]
                screenshot_url = extract_default_screenshot_url(app_id)
                if screenshot_url:
                    logger.info("Screenshot-URL {}:".format(app_id))
                    logger.info(screenshot_url)
                else:
                    logger.error("No Screenshot Found {}.".format(app_id))

                with urlopen(screenshot_url) as url_output:
                    self.img = Image.open(url_output)
                self.img = resize(self.img)
                self.img = ImageTk.PhotoImage(self.img)
                flatpak_panel.config(image=self.img)

            except requests.exceptions.RequestException as e:
                logger.error("Error fetching URL:", e)
                flatpak_panel.config(self.no_img)

            except subprocess.CalledProcessError as err:
                logger.error("Command returned non-zero exit status:", err)
                if "returned non-zero exit status 4" in str(err):
                    try:
                        app_id += ".desktop"
                        screenshot_url = extract_default_screenshot_url(app_id)
                        if screenshot_url:
                            logger.info("Screenshot-URL {}:".format(app_id))
                            logger.info(screenshot_url)
                        else:
                            logger.warning("No Screenshot Found {}.".format(app_id))

                        with urlopen(screenshot_url) as url_output:
                            self.img = Image.open(url_output)
                        self.img = resize(self.img)
                        self.img = ImageTk.PhotoImage(self.img)
                        flatpak_panel.config(image=self.img)

                    except subprocess.CalledProcessError as err:
                        logger.error("Command returned non-zero exit status again:", err)
                        flatpak_panel.config(self.no_img)

        def get_flatpak_description():
            url = f"https://flathub.org/apps/{Flat_remote_dict[flatpak_entry.get()]}"

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            prose_element = soup.find(
                "div", {"class": "prose dark:prose-invert xl:max-w-[75%]"}
            )
            flatpak_description_text.delete("1.0", "end")
            flatpak_description_text.insert(tk.END, prose_element.text)

        def flatpak_show_infos():
            if flatpak_entry.get() == "":
                error_message_0()
            elif flatpak_entry.get() not in Flat_remote_dict.keys():
                error_message_1()
            else:
                flatpak_search_frame.pack_forget()
                flatpak_info_throber_frame.pack_forget()
                flatpak_info_frame.pack(fill=BOTH, expand=True)
                get_flatpak_icon()
                get_flatpak_screenshot()
                get_flatpak_description()

                flatpak_pkg_name.config(text=f"{flatpak_entry.get()}")
                if flatpak_entry.get() in refresh_flatpak_installs().keys():
                    flatpak_pkg_inst.config(
                        text="Uninstall",
                        width=10,
                        command=flatpak_uninstall,
                        style="Red.TButton",
                    )
                else:
                    flatpak_pkg_inst.config(
                        text="Install",
                        width=10,
                        command=flatpak_install,
                        style="Green.TButton",
                    )

        flatpak_inst_main_frame = Frame(self)
        flatpak_inst_main_frame.pack(fill="both", expand=True)

        flatpak_search_frame = ttk.LabelFrame(
            flatpak_inst_main_frame,
            text="Suche",
            padding=20,
        )
        flatpak_search_frame.pack(
            anchor="n", pady=20, padx=10, fill="both", expand=True, side=TOP
        )

        flatpak_search_field = Frame(
            flatpak_search_frame,
            borderwidth=0,
            highlightthickness=0,
        )
        flatpak_search_field.pack(fill="x", pady=5)

        flatpak_search_btn = Label(
            flatpak_search_field,
            image=self.search_btn,
        )

        flatpak_entry = ttk.Entry(
            flatpak_search_field,
            font=("Sans", 15),
        )
        flatpak_entry.pack(fill="x", expand=True, side="left")
        listbox_ttp = CreateToolTip(
            flatpak_entry,
            " - Typ to finde a package\n\n - Single click on a listbox item to show more infos",
        )

        flatpak_list_box = Listbox(
            flatpak_search_frame,
            borderwidth=0,
            highlightthickness=0,
            selectmode=tk.SINGLE,
        )

        flatpak_list_scrollbar = ttk.Scrollbar(flatpak_search_frame)
        flatpak_list_scrollbar.pack(side=RIGHT, fill=Y)
        flatpak_list_box.config(yscrollcommand=flatpak_list_scrollbar.set)
        flatpak_list_scrollbar.config(command=flatpak_list_box.yview)
        flatpak_list_box.pack(fill=BOTH, expand=True)

        update_flatpak(Flat_remote_dict.keys())

        flatpak_list_box.bind("<ButtonRelease-1>", flatpak_list_fillout)

        flatpak_entry.bind("<KeyRelease>", flatpak_search_check)

        flatpak_info_throber_frame = Frame(flatpak_inst_main_frame)
        flatpak_info_throber_frame.pack(fill="x", pady=20, padx=10)

        self.store_btn0_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_0"]["Icon"]
        )

        self.store_btn1_icon = PhotoImage(
            file=SoftwareStore.store_dict["store_1"]["Icon"]
        )

        def open_store(store_key):
            popen(f"""{SoftwareStore.store_dict[store_key]["Open"]}""")

        store_btn_frame = ttk.LabelFrame(
            flatpak_info_throber_frame, text="Softwareverwaltung", padding=20
        )
        store_btn_frame.pack(fill="x")

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

        flatpak_info_frame = ttk.Frame(flatpak_inst_main_frame, padding=20)
        flatpak_info_frame.columnconfigure(0, weight=1)
        flatpak_info_frame.rowconfigure(2, weight=1)

        flatpak_exit = ttk.Button(
            flatpak_info_frame,
            text="Zurück",
            style="Custom.TButton",
            command=hide_flatpak_frame,
        )
        flatpak_exit.grid(row=0, column=0, sticky="e")

        flatpak_application_labelframe = ttk.LabelFrame(
            flatpak_info_frame,
            text="Application",
            padding=20,
        )
        flatpak_application_labelframe.grid(row=1, column=0, sticky="ew")

        flatpak_pkg_header_frame = Frame(
            flatpak_application_labelframe,
            borderwidth=0,
            highlightthickness=0,
        )
        flatpak_pkg_header_frame.pack(fill="x")
        flatpak_pkg_header_frame.columnconfigure(1, weight=2)

        flatpak_pkg_icon = Label(
            flatpak_pkg_header_frame,
            image=self.debinstall_icon,
            font=font_10_b,
            justify="left",
            padx=10,
        )
        flatpak_pkg_icon.grid(row=0, rowspan=2, column=0)

        flatpak_pkg_name = Label(
            flatpak_pkg_header_frame,
            text="",
            font=font_20,
            justify="left",
            anchor="w",
            padx=20,
        )
        flatpak_pkg_name.grid(row=0, column=1, sticky="ew")

        flatpak_pkg_status = Label(
            flatpak_pkg_header_frame,
            text="",
            font=font_8,
            justify="left",
            anchor="w",
            padx=20,
        )
        flatpak_pkg_status.grid(row=1, column=1, sticky="ew")

        flatpak_pkg_inst = ttk.Button(
            flatpak_pkg_header_frame,
            text="Install",
            command=flatpak_install,
        )
        flatpak_pkg_inst.grid(row=0, column=2, sticky="e")

        flatpak_detail_frame = ttk.LabelFrame(
            flatpak_info_frame, text="Details", padding=20
        )
        flatpak_detail_frame.grid(row=2, column=0, sticky="nsew")

        flatpak_detail_frame.columnconfigure(0, weight=1)
        flatpak_detail_frame.rowconfigure(0, weight=1)

        flatpak_canvas = Canvas(
            flatpak_detail_frame, borderwidth=0, highlightthickness=0
        )
        flatpak_canvas.grid(row=0, column=0, sticky="nsew")

        flatpak_canvas_scrollbar = ttk.Scrollbar(
            flatpak_detail_frame, orient="vertical", command=flatpak_canvas.yview
        )
        flatpak_canvas_scrollbar.grid(row=0, column=1, sticky="ns")

        flatpak_canvas.configure(yscrollcommand=flatpak_canvas_scrollbar.set)

        flatpak_canvas_frame = Frame(flatpak_canvas)
        flatpak_canvas.create_window((0, 0), window=flatpak_canvas_frame, anchor="nw")

        flatpak_canvas_frame.bind(
            "<Configure>",
            lambda e: flatpak_canvas.configure(scrollregion=flatpak_canvas.bbox("all")),
        )

        flatpak_panel = Label(flatpak_canvas_frame)
        flatpak_panel.grid(row=0, column=0, columnspan=2, pady=20)

        flatpak_description_text = Text(
            flatpak_canvas_frame,
            borderwidth=0,
            highlightthickness=0,
            font=("Sans", 9),
            wrap=WORD,
            padx=20,
        )
        flatpak_description_text.grid(row=1, column=0, sticky="nesw", padx=(20, 0))

        flatpak_canvas_frame.columnconfigure(0, weight=1)
        flatpak_canvas_frame.rowconfigure(1, weight=1)

        flatpak_info_frame.columnconfigure(0, weight=1)
        flatpak_info_frame.rowconfigure(2, weight=1)




class Custom_Installer(tk.Toplevel):
    """child window that makes the the install process graphicle"""

    def __init__(self, parent):
        super().__init__(parent)
        self.icon = tk.PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/unpack.png"
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
        self.title("Primo")

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
            image=self.boot_log_icon,
        )

        self.icon_label.grid(row=0, rowspan=3, column=0, sticky="w", padx=10, pady=10)
        self.done_label = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            justify="left",
            anchor="w",
        )
        self.done_label.grid(row=0, column=1, sticky="nw")
        self.done_label2 = tk.Label(
            self.installer_main_frame,
            text="",
            font=("Helvetica", 16),
            justify="left",
            anchor="w",
        )
        self.done_label2.grid(row=1, column=1, sticky="nw")
        self.text = tk.Text(
            self.installer_main_frame,
            height=1,
            borderwidth=0,
            highlightthickness=0,
        )

        self.text.grid(row=2, column=1, columnspan=3, sticky="ew")

        self.install_button = ttk.Button(
            self.installer_main_frame,
            text="Schließen",
            command=self.close_btn_command,
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
        logger.info("Thread beendet")
