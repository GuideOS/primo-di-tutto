#!/usr/bin/python3

import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.pop_ups import *
from tabs.system_tab_check import *
from tabs.text_dict_lib import SystemTabDict
from tool_tipps import CreateToolTip


class SystemTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        """System Tab Icons"""
        self.rascinna_config_cli_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/distributor-logo-raspbian.png"
        )
        self.rascinna_config_gui_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/distributor-logo-raspbian.png"
        )
        self.rename_user_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/distributor-logo-raspbian.png"
        )
        self.edit_config_txt_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/mousepad.png"
        )
        self.gparted_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/gparted.png"
        )
        self.mouse_keyboard_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/gnome-settings-keybinding.png"
        )
        self.deskpipro_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/deskpi.png"
        )
        self.network_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/blueman-server.png"
        )
        self.sd_card_copier_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/media-flash-sd-mmc.png"
        )
        self.printer_settings_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/boomaga.png"
        )
        self.desktop_settings_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/com.github.bluesabre.darkbar.png"
        )
        self.screen_settings_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/grandr.png"
        )
        self.neofetch_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/neofetch.png"
        )
        self.fm_godmode_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/folder-yellow.png"
        )
        self.kernel_2_latest_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/distributor-logo-madlinux.png"
        )
        self.boot_log_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/bash.png"
        )
        self.xfce_autostarts_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/desktop-environment-xfce.png"
        )
        self.xfce_settings_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/desktop-environment-xfce.png"
        )
        self.taskmanager_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png"
        )
        self.bash_history_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/bash.png"
        )
        self.cron_job_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/mousepad.png"
        )
        self.alacard_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/classicmenu-indicator-light.png"
        )
        self.source_settings_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/applications-interfacedesign.png"
        )

        self.update_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/aptdaemon-upgrade.png"
        )
        self.bookshelf_icon = PhotoImage(
            file=f"{application_path}/images/icons/PiXflat/bookshelf.png"
        )
        self.rascinna_pipanel = PhotoImage(
            file=f"{application_path}/images/icons/PiXflat/preferences-desktop-theme.png"
        )
        self.gnome_ext_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/org.gnome.Extensions.png"
        )
        self.gnome_tweaks_icon = PhotoImage(
            file=f"{application_path}/images/icons/papirus/48x48/gnome-tweak-tool.png"
        )

        def cinna_settings(text):
            """commands for auto generated buttons"""
            if text == "Gparted":
                popen(f"{permit}  gparted")
            if text == "NeoFetch":
                popen("x-terminal-emulator -e 'bash -c \"neofetch; exec bash\"'")
            if text == "FM God Mode":
                popen(
                    f"{permit} nemo"
                )
            if text == "dmesg":
                popen("x-terminal-emulator -e 'bash -c \"pkexec dmesg; exec bash\"'")

            if text == "dmesg --follow":
                popen(
                    "x-terminal-emulator -e 'bash -c \"sudo dmesg --follow; exec bash\"'"
                )
            if text == "Bash History":
                popen(f"xdg-open {home}/.bash_history")

            if text == "Cron Job":
                popen(f"{permit}  mousepad /etc/crontab")

            if text == "Menu Settings\nAlacart":
                popen("alacarte")

            if text == "Update-Alternatives":
                add_auto = Update_Alternatives(self)
                add_auto.grab_set()

            if text == "Reconfigure Keyboard":
                popen(
                    "x-terminal-emulator -e 'bash -c \"sudo dpkg-reconfigure keyboard-configuration; exec bash\"'"
                )

            if text == "Reconfigure Locales":
                popen(
                    "x-terminal-emulator -e 'bash -c \"sudo dpkg-reconfigure locales; exec bash\"'"
                )

        self.cinna_set = ttk.LabelFrame(
            self, text="Wichtige Werkzeuge auf einen Blick", padding=20
        )
        self.cinna_set.pack(pady=20, padx=20, fill="both", expand=True)
        # self.cinna_set["background"] = frame_color
        # self.cinna_set.columnconfigure(1,wei)
        self.cinna_set.grid_columnconfigure(0, weight=2)
        self.cinna_set.grid_columnconfigure(1, weight=2)
        self.cinna_set.grid_columnconfigure(2, weight=1)
        self.cinna_set.grid_columnconfigure(3, weight=2)
        self.cinna_set.grid_columnconfigure(4, weight=1)

        cinna_settings_btn_list = [
            "Bash History",
            "Cron Job",
            "dmesg --follow",
            "dmesg",
            "FM God Mode",
            "Gparted",
            "Menu Optionen",
            "Reconfigure Keyboard",
            "Reconfigure Locales",
            "Update-Alternatives",
        ]
        cinna_settings_btn_list1 = []
        conf_row = 0
        conf_column = 0
        for cinna_settings_btn in cinna_settings_btn_list:
            self.cinna_button_x = ttk.Button(
                self.cinna_set,
                # width=140,
                # height=110,
                text=cinna_settings_btn,
                command=lambda text=cinna_settings_btn: cinna_settings(text),
                # highlightthickness=0,
                # borderwidth=0,
                # background=frame_color,
                # foreground=main_font,
                compound=TOP,
                # activebackground=ext_btn,
                style="Custom.TButton",
            )
            self.cinna_button_x.grid(
                row=conf_row, column=conf_column, padx=5, pady=5, sticky="ew"
            )
            cinna_settings_btn_list1.append(self.cinna_button_x)
            conf_column = conf_column + 1
            if conf_column == 5:
                conf_row = conf_row + 1
                conf_column = 0

            if cinna_settings_btn == "Edit Config.txt":
                self.cinna_button_x.config(image=self.edit_config_txt_icon)


            if cinna_settings_btn == "NeoFetch":
                self.cinna_button_x.config(image=self.neofetch_icon)
                if os.path.isfile("/bin/neofetch"):
                    print("[Info] Neofetch is installed")
                    self.cinna_button_x.configure(state=NORMAL)
                else:
                    print("[Info] Neofetch is not installed")
                    self.cinna_button_x.configure(state=DISABLED)

            if cinna_settings_btn == "Gparted":
                self.cinna_button_x.config(image=self.gparted_icon)
                if os.path.isfile("/usr/sbin/gparted"):
                    print("[Info] Gparted is installed")
                    self.cinna_button_x.configure(state=NORMAL)
                else:
                    print("[Info] Gparted is not installed")
                    self.cinna_button_x.configure(state=DISABLED)

            if cinna_settings_btn == "FM God Mode":
                self.cinna_button_x.config(image=self.fm_godmode_icon)

            if cinna_settings_btn == "dmesg --follow":
                self.cinna_button_x.config(image=self.boot_log_icon)
            if cinna_settings_btn == "dmesg":
                self.cinna_button_x.config(image=self.boot_log_icon)

            if cinna_settings_btn == "Reconfigure Keyboard":
                self.cinna_button_x.config(image=self.boot_log_icon)
            if cinna_settings_btn == "Reconfigure Locales":
                self.cinna_button_x.config(image=self.boot_log_icon)


            if cinna_settings_btn == "Bash History":
                self.cinna_button_x.config(image=self.bash_history_icon)

            if cinna_settings_btn == "Cron Job":
                self.cinna_button_x.config(image=self.cron_job_icon)

            if cinna_settings_btn == "Menu Optionen":
                self.cinna_button_x.config(image=self.alacard_icon)
                if check_alacarte() == False:
                    self.cinna_button_x.configure(state=DISABLED)

            if cinna_settings_btn == "Update-Alternatives":
                self.cinna_button_x.config(image=self.bash_history_icon)

