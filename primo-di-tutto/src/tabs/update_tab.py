#!/usr/bin/python3

import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_alias_list import *
from flatpak_manage import *
from tool_tipps import CreateToolTip
from tool_tipps import TipsText
from tabs.pop_ups import *
from tabs.text_dict_lib import Update_Tab_Buttons
from resorcess import pi_identify

import gettext
lang = gettext.translation('messages', localedir=f"{application_path}/src/tabs/locale", languages=['de'])
lang.install()
_ = lang.gettext

class UpdateTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.folder_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/folder_s_light.png"
        )
        self.up_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_up_s_light.png"
        )
        self.gup_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_upg_s_light.png"
        )
        self.recover_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/recover_s_light.png"
        )
        self.fup_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_fupg_s_light.png"
        )
        self.allow_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/allow_s_light.png"
        )
        self.arm_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/del_s_light.png"
        )
        self.confa_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/confa_s_light.png"
        )
        self.re_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/re_s_light.png"
        )
        self.inst_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/debinst_s_light.png"
        )
        self.term_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/terminal_s_light.png"
        )

        self.term_logo = PhotoImage(
            file=f"{application_path}/images/icons/papirus/goterminal.png"
        )

        def all_up_action():
            """Passes commands for auto-generated buttons"""
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()

            command = (
                f"xterm -into {wid} -bg Grey11 -geometry {frame_height}x{frame_width} -e "
                "\"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY bash -c 'apt update -y && apt upgrade -y && apt autoremove -y && flatpak update -y && flatpak uninstall --unused -y' | lolcat && "
                'sleep 5 && exit; exec bash"'
            )

            # Ausführung des Befehls und Statusüberprüfung
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                print(_("Update erfolgreich ausgeführt!"))
                send_notification(
                    "Primo Di Tutto",
                    _("Update erfolgreich ausgeführt!"),
                    icon_path="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png",
                    urgency="critical",
                )
            except subprocess.CalledProcessError as e:
                send_notification(
                    "Primo Di Tutto",
                    _("Update war nichterfolgreich !"),
                    icon_path="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png",
                    urgency="critical",
                )
                print(f"Fehlermeldung: {e.stderr.decode()}")
            # Beispielaufruf mit Icon und hoher Dringlichkeit

        self.update_button_frame = ttk.Frame(self, padding=20)
        self.update_button_frame.grid(row=0, column=0, sticky="ns")

        self.all_up_button = ttk.Button(
            self.update_button_frame,
            text=_("All Up"),
            style="Accent.TButton",
            width=20,
            command=all_up_action,
        )
        self.all_up_button.pack()

        self.apt_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text="APT-Optionen",
        )
        self.apt_option_frame.pack(pady=10)

        self.apt_update_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Update"),
            # command=
            width=20,
        )

        self.apt_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.apt_upgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Update & Upgrade"),
            # command=
            width=20,
        )

        self.apt_upgrade_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.apt_upgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Show Upgradeble"),
            # command=
            width=20,
        )

        self.apt_upgrade_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.apt_autoremove_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Autoremove"),
            # command=
            width=20,
        )

        self.apt_autoremove_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.apt_broken_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fix Broken"),
            # command=
            width=20,
        )

        self.apt_broken_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.apt_missing_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fix Missing"),
            # command=
            width=20,
        )

        self.apt_missing_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.apt_cinfigure_a_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("dpkg --configure -a"),
            # command=
            width=20,
        )

        self.apt_cinfigure_a_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text=_("Flatpak-Optionen"),
        )
        self.flatpak_option_frame.pack(pady=10)

        self.flatpak_update_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text=_("Update"),
            # command=
            width=20,
        )

        self.flatpak_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_upgrade_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text=_("uninstall --unused"),
            # command=
            width=20,
        )

        self.flatpak_upgrade_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ######################
        self.update_term_frame = ttk.LabelFrame(self, text=_("Prozess"))
        self.update_term_frame.grid(row=0, column=1, sticky="nesw", padx=20, pady=20)

        self.termf = ttk.Frame(self.update_term_frame)

        self.term_logo_label = Label(
            self.termf,
            image=self.term_logo,  # background=frame_color
        )
        self.term_logo_label.pack(fill=BOTH, expand=True)

        self.termf.pack(fill=BOTH, expand=True, padx=10, pady=5)

        global wid
        wid = self.termf.winfo_id()

        ########################
        self.update_info_frame = ttk.LabelFrame(self, text="Info")
        self.update_info_frame.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=20
        )

        self.all_up_button = ttk.Label(self.update_info_frame, text="Bla\n")
        self.all_up_button.pack()
