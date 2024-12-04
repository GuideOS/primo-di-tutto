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

        if "dark" in theme_name or "Dark" in theme_name:
            self.folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/folder_s.png"
            )
            self.up_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/pack_up_s.png"
            )
            self.gup_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/pack_upg_s.png"
            )
            self.recover_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/recover_s.png"
            )
            self.fup_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/pack_fupg_s.png"
            )
            self.allow_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/allow_s.png"
            )
            self.arm_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/del_s.png"
            )
            self.confa_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/confa_s.png"
            )
            self.re_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/re_s.png"
            )
            self.inst_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/debinst_s.png"
            )

        else:
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


        def update_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt update -y |lolcat && sleep 5 && exit ; exec bash"'
                    % wid
                )

        def upgrade_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            command = (
                f"xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "
                "\"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY bash -c 'apt update -y && apt upgrade -y' | lolcat && "
                'sleep 5 && exit; exec bash"' % wid
            )
            os.popen(command)

        def apt_showupgrade_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f"xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "
                "\"apt list --upgradable |lolcat && read -p 'Press Enter to exit.' && exit; exec bash\""
                % wid
            )

        def apt_autremove_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt autoremove -y |lolcat && sleep 5 && exit ; exec bash"'
                % wid
            )
        def apt_broken_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt --fix-broken install |lolcat && sleep 5 && exit; exec bash"'
                % wid
            )

        def apt_missing_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt install --fix-missing |lolcat && sleep 5 && exit; exec bash"'
                % wid
            )

        def apt_reconf_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} dpkg --configure -a |lolcat && sleep 5 && exit; exec bash"'
                % wid
            )
        def flatpak_update_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "flatpak update -y && sleep 5 && exit ; exec bash"'
                % wid
            )
        def flatpak_clean_action():
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            os.popen(
                f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "flatpak uninstall --unused -y && sleep 5 && exit; exec bash"'
                % wid
            )


        self.update_button_frame = ttk.Frame(self, padding=20)
        self.update_button_frame.grid(row=0, column=0, sticky="ns")

        self.all_up_button = ttk.Button(
            self.update_button_frame,
            text=_("Alles Aktualisieren"),
            style="Accent.TButton",
            width=20,
            command=all_up_action,
        )
        self.all_up_button.pack(fill="x")


        self.apt_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text="APT-Optionen",
        )
        self.apt_option_frame.pack(pady=10)

        self.apt_update_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Update"),
            image=self.up_icon,
            command=update_action,
            width=20,
        )

        self.apt_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.apt_upgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Update & Upgrade"),
            image=self.gup_icon,
            command=upgrade_action,
            width=20,
        )

        self.apt_upgrade_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.apt_showupgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Show Upgradeble"),
            image=self.up_icon,
            command=apt_showupgrade_action,
            width=20,
        )

        self.apt_showupgrade_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.apt_autoremove_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Autoremove"),
            image=self.arm_icon,
            command=apt_autremove_action,
            width=20,
        )

        self.apt_autoremove_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.apt_broken_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fix Broken"),
            image=self.up_icon,
            command=apt_broken_action,
            width=20,
        )

        self.apt_broken_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.apt_missing_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fix Missing"),
            image=self.confa_icon,
            command=apt_missing_action,
            width=20,
        )

        self.apt_missing_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.apt_cinfigure_a_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("dpkg --configure -a"),
            image=self.up_icon,
            command=apt_reconf_action,
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
            image=self.up_icon,
            command=flatpak_update_action,
            width=20,
        )

        self.flatpak_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_clean_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text=_("uninstall --unused"),
            image=self.arm_icon,
            command=flatpak_clean_action,
            width=20,
        )

        self.flatpak_clean_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

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
        self.update_info_frame = ttk.LabelFrame(self, text="Info",padding=20)
        self.update_info_frame.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=20
        )

        self.update_info_label = ttk.Label(self.update_info_frame)
        self.update_info_label.pack(anchor="w")

        self.all_up_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Aktualisiert das gesammte Betriebsystem inklusive Flatpak-Anwendungen."))
        self.all_up_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_update_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Es wird der Befehl 'apt update' ausgeführ um die Paketliste auf den neusten Stand zu bringen."))
        self.apt_update_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_upgrade_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Es wird der Befehl 'apt update && apt upgrade' ausgeführ um die Paketliste auf den neusten Stand zu bringen und alle Pakete zu aktualisieren."))
        self.apt_upgrade_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_showupgrade_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Es werden aktualisierbare Pakete aufgelistet."))
        self.apt_showupgrade_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_autoremove_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Pakete oder Abhängikeiten, die zurückgeblieben sind werden entfernt."))
        self.apt_autoremove_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_broken_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Der Befehl 'apt --fix-broken install' repariert fehlerhafte oder unvollständige Paketinstallationen, indem fehlende\nAbhängigkeiten installiert oder beschädigte Pakete korrigiert werden."))
        self.apt_broken_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_missing_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Der Befehl 'apt install --fix-missing' lädt fehlende Paketdateien nach, falls sie beim ersten Versuch\nnicht heruntergeladen wurden, und setzt die Installation fort."))
        self.apt_missing_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.apt_cinfigure_a_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Der Befehl 'dpkg --configure -a' richtet alle Pakete ein, die heruntergeladen, aber noch nicht\nvollständig konfiguriert wurden, und behebt so Installationsprobleme."))
        self.apt_cinfigure_a_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.flatpak_update_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Es werden alle installierten Flatpak-Programme aktualisiert."))
        self.flatpak_update_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

        self.flatpak_clean_button.bind("<Enter>", lambda event: self.update_info_label.configure(text="Zurückgebliebene Abhängigkeiten werden entfernt."))
        self.flatpak_clean_button.bind("<Leave>", lambda event: self.update_info_label.configure(text=""))

