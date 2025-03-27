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
    SoftwareGamingTools,
    SoftwareGame,
    SoftwareOffice,
    SoftwareStore,
    SoftwareCommunication,
    SoftwareAudioVideo,
    SoftwareImageEditing,
    SoftwareBackup
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
        gaming_tools_frame = ttk.Frame(self.inst_notebook)
        gaming_frame = ttk.Frame(self.inst_notebook)
        backup_frame = ttk.Frame(self.inst_notebook)
        saifty_frame = ttk.Frame(self.inst_notebook)



        com_frame.pack(fill="both", expand=True)
        office_frame.pack(fill="both", expand=True)
        av_frame.pack(fill="both", expand=True)
        image_frame.pack(fill="both", expand=True)
        gaming_tools_frame.pack(fill="both", expand=True)
        gaming_frame.pack(fill="both", expand=True)
        backup_frame.pack(fill="both", expand=True)
        saifty_frame.pack(fill="both", expand=True)


        self.inst_notebook.add(com_frame, compound=LEFT, text="Web & Chat")
        self.inst_notebook.add(office_frame, compound=LEFT, text="Büro")
        self.inst_notebook.add(av_frame, compound=LEFT, text="Audio & Video")
        self.inst_notebook.add(image_frame, compound=LEFT, text="Bildbearbeitung")
        self.inst_notebook.add(gaming_tools_frame, compound=LEFT, text="Gaming Tools")
        self.inst_notebook.add(gaming_frame, compound=LEFT, text="Native Games")
        self.inst_notebook.add(backup_frame, compound=LEFT, text="Backup")
        self.inst_notebook.add(saifty_frame, compound=LEFT, text="Sicherheit")

        # Com Panel
        com_apps = [];
        for i, (key, info) in enumerate(SoftwareCommunication.com_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareCommunication.com_dict[key]["Package"],
                name=SoftwareCommunication.com_dict[key]["Name"],
                icon=SoftwareCommunication.com_dict[key]["Icon"],
                description=SoftwareCommunication.com_dict[key]["Description"],
                path=SoftwareCommunication.com_dict[key]["Path"],
                thumbnail=SoftwareCommunication.com_dict[key]["Thumbnail"],
                install_command=SoftwareCommunication.com_dict[key]["Install"],
                uninstall_command=SoftwareCommunication.com_dict[key]["Uninstall"],
            )
            com_apps.append(app)

        com_note_frame = AppCollectionPanel(category_title="Web & Chat", apps=com_apps, master=com_frame)
        com_note_frame.pack(fill=tk.BOTH, expand=True)

        # Office Panel
        office_apps = [];
        for i, (key, info) in enumerate(SoftwareOffice.office_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareOffice.office_dict[key]["Package"],
                name=SoftwareOffice.office_dict[key]["Name"],
                icon=SoftwareOffice.office_dict[key]["Icon"],
                description=SoftwareOffice.office_dict[key]["Description"],
                path=SoftwareOffice.office_dict[key]["Path"],
                thumbnail=SoftwareOffice.office_dict[key]["Thumbnail"],
                install_command=SoftwareOffice.office_dict[key]["Install"],
                uninstall_command=SoftwareOffice.office_dict[key]["Uninstall"],
            )
            office_apps.append(app)

        office_note_frame = AppCollectionPanel(category_title="Büro", apps=office_apps, master=office_frame)
        office_note_frame.pack(fill=tk.BOTH, expand=True)

        # A/V Panel
        av_apps = [];
        for i, (key, info) in enumerate(SoftwareAudioVideo.av_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareAudioVideo.av_dict[key]["Package"],
                name=SoftwareAudioVideo.av_dict[key]["Name"],
                icon=SoftwareAudioVideo.av_dict[key]["Icon"],
                description=SoftwareAudioVideo.av_dict[key]["Description"],
                path=SoftwareAudioVideo.av_dict[key]["Path"],
                thumbnail=SoftwareAudioVideo.av_dict[key]["Thumbnail"],
                install_command=SoftwareAudioVideo.av_dict[key]["Install"],
                uninstall_command=SoftwareAudioVideo.av_dict[key]["Uninstall"],
            )
            av_apps.append(app)

        av_note_frame = AppCollectionPanel(category_title="Audio/Video", apps=av_apps, master=av_frame)
        av_note_frame.pack(fill=tk.BOTH, expand=True)

        # Image Editing Panel
        image_apps = [];
        for i, (key, info) in enumerate(SoftwareImageEditing.img_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareImageEditing.img_dict[key]["Package"],
                name=SoftwareImageEditing.img_dict[key]["Name"],
                icon=SoftwareImageEditing.img_dict[key]["Icon"],
                description=SoftwareImageEditing.img_dict[key]["Description"],
                path=SoftwareImageEditing.img_dict[key]["Path"],
                thumbnail=SoftwareImageEditing.img_dict[key]["Thumbnail"],
                install_command=SoftwareImageEditing.img_dict[key]["Install"],
                uninstall_command=SoftwareImageEditing.img_dict[key]["Uninstall"],
            )
            image_apps.append(app)

        image_note_frame = AppCollectionPanel(category_title="Bildbearbeitung", apps=image_apps, master=image_frame)
        image_note_frame.pack(fill=tk.BOTH, expand=True)

        # Gaming Panel
        gaming_apps = [];
        for i, (key, info) in enumerate(SoftwareGame.game_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareGame.game_dict[key]["Package"],
                name=SoftwareGame.game_dict[key]["Name"],
                icon=SoftwareGame.game_dict[key]["Icon"],
                description=SoftwareGame.game_dict[key]["Description"],
                path=SoftwareGame.game_dict[key]["Path"],
                thumbnail=SoftwareGame.game_dict[key]["Thumbnail"],
                install_command=SoftwareGame.game_dict[key]["Install"],
                uninstall_command=SoftwareGame.game_dict[key]["Uninstall"],
            )
            gaming_apps.append(app)

        gaming_note_frame = AppCollectionPanel(category_title="Gaming", apps=gaming_apps, master=gaming_frame)
        gaming_note_frame.pack(fill=tk.BOTH, expand=True)

        # Gaming Panel
        gaming_tools_apps = [];
        for i, (key, info) in enumerate(SoftwareGamingTools.game_tool_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareGamingTools.game_tool_dict[key]["Package"],
                name=SoftwareGamingTools.game_tool_dict[key]["Name"],
                icon=SoftwareGamingTools.game_tool_dict[key]["Icon"],
                description=SoftwareGamingTools.game_tool_dict[key]["Description"],
                path=SoftwareGamingTools.game_tool_dict[key]["Path"],
                thumbnail=SoftwareGamingTools.game_tool_dict[key]["Thumbnail"],
                install_command=SoftwareGamingTools.game_tool_dict[key]["Install"],
                uninstall_command=SoftwareGamingTools.game_tool_dict[key]["Uninstall"],
            )
            gaming_tools_apps.append(app)

        gaming_tool_note_frame = AppCollectionPanel(category_title="Gaming", apps=gaming_tools_apps, master=gaming_tools_frame)
        gaming_tool_note_frame.pack(fill=tk.BOTH, expand=True)

        # Backup Panel
        bak_apps = [];
        for i, (key, info) in enumerate(SoftwareBackup.bak_dict.items()):
            app = InstallableAppFactory.create(
                type=SoftwareBackup.bak_dict[key]["Package"],
                name=SoftwareBackup.bak_dict[key]["Name"],
                icon=SoftwareBackup.bak_dict[key]["Icon"],
                description=SoftwareBackup.bak_dict[key]["Description"],
                path=SoftwareBackup.bak_dict[key]["Path"],
                thumbnail=SoftwareBackup.bak_dict[key]["Thumbnail"],
                install_command=SoftwareBackup.bak_dict[key]["Install"],
                uninstall_command=SoftwareBackup.bak_dict[key]["Uninstall"],
            )
            bak_apps.append(app)

        gaming_tool_note_frame = AppCollectionPanel(category_title="Gaming", apps=bak_apps, master=backup_frame)
        gaming_tool_note_frame.pack(fill=tk.BOTH, expand=True)



class AppCollectionPanel(tk.Frame):
    def __init__(self, category_title: str, apps, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.update_interval = 1000
        self.button_icons = []
        self.buttons = []
        self.apps = apps

        def show_button_frame():
            self.software_store.pack(padx=20,pady=5,fill="x")
            btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)
            ttp_frame.pack(pady=20, padx=20,fill="x", side="bottom")
            back_button.pack_forget()
            detail_frame.pack_forget()

        def hide_button_frame():
            self.software_store.pack_forget()
            btn_frame.pack_forget()
            ttp_frame.pack_forget()
            back_button.pack(pady=20, padx=20, anchor="w")

        def open_gnome_software():
            subprocess.Popen("gnome-software", shell=True)

        def on_hover( event, app: InstallableApp):
            ttp_label.configure(text=app.get_description())

        # Funktion für das Verlassen des Buttons
        def on_leave( event):
            ttp_label.configure(text="")

        def run_installation(app: InstallableApp):
            primo_skript_task = "Installation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_install_command()
            )
            self.master.wait_window(custom_installer)
            self.detail_inst.config(text="Deinstallieren")

            refresh_status(app)

        def run_uninstall(app: InstallableApp):
            primo_skript_task = "Deinstallation ..."
            custom_installer = Custom_Installer(master)
            custom_installer.do_task(
                primo_skript_task, app.get_name(), app.get_uninstall_command()
            )
            self.master.wait_window(custom_installer)
            self.detail_inst.config(text="Installieren")

            refresh_status(app)

        def refresh_status(app: InstallableApp):
            if (app.is_installed()):
                logger.info(f"{app.get_name()} is installed")
                self.detail_inst.config(
                    text="Deinstallieren",
                    command=lambda: run_uninstall(app),
                    style="Red.TButton",
                )
            else:
                logger.info(f"{app.get_name()} is not installed")
                self.detail_inst.config(
                    text="Installieren",
                    command=lambda: run_installation(app),
                    style="Green.TButton",
                )

            index = self.apps.index(app)
            update_button_icon(self.buttons[index], app, index)

        def app_btn_action(app):
            logger.info(f"btn_action {app.get_name()}")

            thumb_img = Image.open(app.get_thumbnail())
            resized_thumb_img = resize700(thumb_img)
            self.thumb = ImageTk.PhotoImage(resized_thumb_img)

            icon_img = Image.open(app.get_icon())
            resized_icon_img = resize46(icon_img)
            self.icon = ImageTk.PhotoImage(resized_icon_img)

            self.detail_icon.configure(image=self.icon)
            self.detail_name.config(text=f"{app.get_name()}")
            self.detail_pak.config(text=f"{app.get_type()}")
            self.detail_desc.config(text=f"\n{app.get_description()}")

            self.detail_inst.grid(column=2, row=0, rowspan=2, sticky="e")
            self.termf.grid(column=0, columnspan=3, row=3)
            self.thumb_lbl.configure(image=self.thumb)
            self.thumb_lbl.pack()

            hide_button_frame()
            detail_frame.pack(pady=20, padx=20, fill="both", expand=True)

            refresh_status(app)

        self.gnome_software_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/64x64/gnome-software.png"
        )

        self.software_store = ttk.Button(self, text="Software-Center öffnen", compound="left",image=self.gnome_software_icon, style="Accent2.TButton", command=open_gnome_software)
        self.software_store.pack(padx=20,pady=5,fill="x")

        back_button = ttk.Button(self, text="Zurück",style="Custom.TButton", command=show_button_frame)

        btn_frame = ttk.LabelFrame(self, text=f"{category_title} | Empfehlungen", padding=20)
        btn_frame.pack(pady=20, padx=20, fill="both", expand=TRUE)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)
        btn_frame.grid_columnconfigure(4, weight=1)

        ttp_frame = ttk.LabelFrame(
            self, text="Beschreibung"
        )
        ttp_frame.pack(pady=20, padx=20,fill="x")
        ttp_frame.config(height=200)
        ttp_frame.pack_propagate(False)

        ttp_label = ttk.Label(
            ttp_frame, text="", padding=20, wraplength=700
        )
        ttp_label.pack(fill="x")

        max_columns = 5

        def generate_app_button(app):
            img = Image.open(app.get_icon())
            resized_img = resize46(img)
            combined_image = resized_img

            # add indicator if app is already installed
            if app.is_installed():
                indicator = Image.open(f"{application_path}/images/icons/pigro_icons/installed.png").resize(resized_img.size)
                combined_image = Image.alpha_composite(resized_img.convert("RGBA"), indicator.convert("RGBA"))

            return combined_image

        def update_button_icon(button, app, index):
            combined_image = generate_app_button(app)

            icon = ImageTk.PhotoImage(combined_image)
            self.button_icons[index] = icon
            button.config(image=icon)

        for (i , app) in enumerate(self.apps):
            row = i // max_columns
            column = i % max_columns

            combined_image = generate_app_button(app)


            icon = ImageTk.PhotoImage(combined_image)
            self.button_icons.append(icon)

            button = ttk.Button(
                btn_frame,
                text=app.get_name(),
                image=icon,
                command=lambda key=i: app_btn_action(self.apps[key]),
                compound=tk.TOP,
                style="Custom.TButton",
                width=20,
            )
            button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")
            button.bind("<Enter>", lambda event, key=i: on_hover(event, self.apps[key]))
            button.bind("<Leave>", on_leave)
            self.buttons.append(button)


        detail_frame = ttk.LabelFrame(self, text="Details", padding=20)

        detail_frame.grid_columnconfigure(1, weight=1)
        detail_frame.grid_rowconfigure(3, weight=1)
        self.detail_icon = Label(
            detail_frame,
        )
        self.detail_icon.grid(column=0, row=0, rowspan=2, sticky="we")

        self.detail_name = Label(
            detail_frame, text="", justify="left", anchor="w", font=font_16
        )
        self.detail_name.grid(column=1, row=0, sticky="w")

        self.detail_pak = Label(
            detail_frame, text="", justify="left", anchor="w"
        )
        self.detail_pak.grid(column=1, row=1, sticky="we")

        self.detail_desc = Label(
            detail_frame, text="", justify="left", anchor="w", wraplength=750
        )
        self.detail_desc.grid(column=0, row=2, columnspan=3, sticky="ew")

        self.detail_inst = ttk.Button(
            detail_frame, text="Install", style="Custom.TButton"
        )

        self.termf = Frame(
            detail_frame,
        )
        self.thumb_lbl = Label(self.termf)

        global wid
        wid = self.termf.winfo_id()



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
