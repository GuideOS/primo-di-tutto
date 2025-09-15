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
import gettext
import threading
from logger_config import setup_logger
import subprocess

logger = setup_logger(__name__)

# Set up gettext
gettext.bindtextdomain('primo-di-tutto', f'{application_path}/src/locale')
gettext.textdomain('primo-di-tutto')
_ = gettext.gettext


class UpdateTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.term_logo = PhotoImage(
            file=f"{application_path}/images/icons/papirus/goterminal.png"
        )

        # kill_term soll % wid beenden

        def execute_command(command, event=None):
            self.term_logo_label.grid_forget()
            self.terminal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            self.terminal_scroll.grid(row=0, column=1, sticky="ns")
            self.terminal.config(yscrollcommand=self.terminal_scroll.set)
            if command.strip() == "":
                return

            # Starte den Befehl in einem separaten Thread, um das GUI nicht zu blockieren
            thread = threading.Thread(target=run_command, args=(command,))
            thread.start()

        def run_command(command):
            # Starte den Prozess mit Popen
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            # Lese Zeile für Zeile und aktualisiere das Text-Widget
            for line in iter(process.stdout.readline, ""):
                self.terminal.insert(tk.END, line)
                self.terminal.see(tk.END)  # Auto-Scroll

            process.stdout.close()
            process.wait()
            self.term_quit_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        def kill_term():
            self.terminal.delete(1.0, tk.END)
            self.terminal.grid_forget()
            self.terminal_scroll.grid_forget()
            self.term_quit_button.grid_forget()
            self.term_logo_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        def all_up_action():
            allup = f"{permit} {application_path}/scripts/all_up"
            execute_command(allup)

        def update_action():
            update_command = f"{permit} {application_path}/scripts/nala_update_wrap"
            execute_command(update_command)

        def upgrade_action():
            upgrade_command = f"{permit} {application_path}/scripts/nala_upgrade_wrap"
            execute_command(upgrade_command)

        def apt_showupgrade_action():
            show_command = f"{application_path}/scripts/apt_list_upgradeble_wrap"
            execute_command(show_command)

        def apt_autremove_action():
            autorm_command = f"pkexec {application_path}/scripts/nala_autopurge_wrap"
            execute_command(autorm_command)

        def apt_broken_action():
            fix_broken_action = f"pkexec {application_path}/scripts/apt_fix_broken_wrap"
            execute_command(fix_broken_action)

        def apt_missing_action():
            fix_missing_action = (
                f"pkexec {application_path}/scripts/apt_fix_missing_wrap"
            )
            execute_command(fix_missing_action)

        def apt_reconf_action():
            fix_missing_action = f"pkexec {application_path}/scripts/conf-a_wrap"
            execute_command(fix_missing_action)

        def flatpak_update_action():
            flat_up_command = (
                f"{application_path}/scripts/flatpak_update_wrap && exit ; exec bash"
            )
            execute_command(flat_up_command)

        def flatpak_clean_action():
            flat_clean_command = f"{application_path}/scripts/flatpak_clean_wrap"
            execute_command(flat_clean_command)

        self.update_button_frame = ttk.Frame(self, padding=20)
        self.update_button_frame.grid(row=0, column=0, sticky="ns")

        self.all_up_button = ttk.Button(
            self.update_button_frame,
            text=_("Update Everything"),
            style="Accent.TButton",
            width=20,
            command=all_up_action,
        )
        self.all_up_button.pack(fill="x")

        self.apt_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text=_("APT Options"),
        )
        self.apt_option_frame.pack(pady=10)

        self.apt_update_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Update List"),
            command=update_action,
            width=20,
        )

        self.apt_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.apt_upgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Upgrade Packages"),
            command=upgrade_action,
            width=20,
        )

        self.apt_upgrade_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.apt_showupgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Available Updates"),
            command=apt_showupgrade_action,
            width=20,
        )

        self.apt_showupgrade_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.apt_autoremove_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Clean Up"),
            command=apt_autremove_action,
            width=20,
        )

        self.apt_autoremove_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.apt_broken_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fix Errors"),
            command=apt_broken_action,
            width=20,
        )

        self.apt_broken_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.apt_missing_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Fetch Missing Packages"),
            command=apt_missing_action,
            width=20,
        )

        self.apt_missing_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.apt_cinfigure_a_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text=_("Repair"),
            command=apt_reconf_action,
            width=20,
        )

        self.apt_cinfigure_a_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text=_("Flatpak Options"),
        )
        self.flatpak_option_frame.pack(pady=10)

        self.flatpak_update_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text=_("Update"),
            command=flatpak_update_action,
            width=20,
        )

        self.flatpak_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_clean_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text=_("Clean Up"),
            command=flatpak_clean_action,
            width=20,
        )

        self.flatpak_clean_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.update_term_frame = ttk.LabelFrame(self, text=_("Process"))
        self.update_term_frame.grid(row=0, column=1, sticky="nesw", padx=20, pady=20)
        self.update_term_frame.grid_rowconfigure(0, weight=1)
        self.update_term_frame.grid_columnconfigure(0, weight=1)

        self.term_logo_label = Label(
            self.update_term_frame,
            image=self.term_logo,
        )
        self.term_logo_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.terminal = tk.Text(
            self.update_term_frame, height=20, borderwidth=0, highlightthickness=0
        )

        self.terminal_scroll = ttk.Scrollbar(
            self.update_term_frame, orient="vertical", command=self.terminal.yview
        )

        self.term_quit_button = ttk.Button(
            self.update_term_frame,
            text=_("Quit"),
            style="Accent.TButton",
            command=kill_term,
        )

        self.update_info_frame = ttk.LabelFrame(self, text=_("Info"))
        self.update_info_frame.grid(
            row=1, column=0, columnspan=2, sticky="nesw", padx=20, pady=20
        )
        self.update_info_frame.pack_propagate(False)

        self.update_info_label = ttk.Label(
            self.update_info_frame, text="", justify="left", wraplength=900
        )
        self.update_info_label.pack(anchor="nw", fill="x", padx=10, pady=5)

        self.all_up_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Updates the entire operating system including Flatpak applications.")
            ),
        )
        self.all_up_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_update_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Runs 'apt update' to bring the package list up to date.")
            ),
        )
        self.apt_update_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_upgrade_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Runs 'apt update && apt upgrade' to update the package list and upgrade all packages.")
            ),
        )
        self.apt_upgrade_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_showupgrade_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Lists upgradable packages.")
            ),
        )
        self.apt_showupgrade_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_autoremove_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Removes packages or dependencies that are left behind.")
            ),
        )
        self.apt_autoremove_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_broken_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("The command 'apt --fix-broken install' repairs faulty or incomplete package installations by installing missing dependencies or fixing broken packages.")
            ),
        )
        self.apt_broken_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_missing_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("The command 'apt install --fix-missing' downloads missing package files if they were not downloaded the first time and continues the installation.")
            ),
        )
        self.apt_missing_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_cinfigure_a_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("The command 'dpkg --configure -a' configures all packages that have been downloaded but not yet fully set up, thus fixing installation problems.")
            ),
        )
        self.apt_cinfigure_a_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.flatpak_update_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("All installed Flatpak applications are updated.")
            ),
        )
        self.flatpak_update_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.flatpak_clean_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text=_("Leftover dependencies are removed.")
            ),
        )
        self.flatpak_clean_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )
