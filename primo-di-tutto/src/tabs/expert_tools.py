import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from resorcess import *
from tabs.pop_ups import *
from tabs.system_dict_lib import SoftwareSys
from logger_config import setup_logger
import threading
import subprocess
import gettext

logger = setup_logger(__name__)

lang = gettext.translation(
    "messages", localedir=f"{application_path}/src/tabs/locale", languages=["de"]
)
lang.install()
_ = lang.gettext


class ExpertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        source_frame = ttk.Frame(self.inst_notebook)
        admin_frame = ttk.Frame(self.inst_notebook)
        apt_tools_frame = ttk.Frame(self.inst_notebook)

        source_frame.pack(fill="both", expand=True)
        admin_frame.pack(fill="both", expand=True)
        apt_tools_frame.pack(fill="both", expand=True)

        self.inst_notebook.add(source_frame, compound=LEFT, text="Quellen")
        self.inst_notebook.add(admin_frame, compound=LEFT, text="Werkzeuge")
        self.inst_notebook.add(apt_tools_frame, compound=LEFT, text="APT-Werkzeuge")

        source_note_frame = SourcePanel(source_frame)
        source_note_frame.pack(fill=tk.BOTH, expand=True)

        admin_note_frame = AdminPanel(admin_frame)
        admin_note_frame.pack(fill=tk.BOTH, expand=True)

        apt_tools_frame = AptToolsFrame(apt_tools_frame)
        apt_tools_frame.pack(fill=tk.BOTH, expand=True)


class AdminPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Frame für Canvas und Scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas-Container für sys_btn_frame
        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame in den Canvas einfügen
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # sys_btn_frame in das scrollbare Frame einfügen
        sys_btn_frame = ttk.LabelFrame(scrollable_frame, text="Werkzeuge", padding=20)
        sys_btn_frame.pack(fill="both", expand=tk.TRUE)

        sys_btn_frame.grid_columnconfigure(0, weight=2)
        sys_btn_frame.grid_columnconfigure(1, weight=2)
        sys_btn_frame.grid_columnconfigure(2, weight=2)
        sys_btn_frame.grid_columnconfigure(3, weight=1)
        sys_btn_frame.grid_columnconfigure(4, weight=2)

        def sys_btn_action(sys_key):
            # SoftwareSys.sys_dict[sys_key]["Action"]
            command = SoftwareSys.sys_dict[sys_key]["Action"]
            print(command)
            os.popen(command)

        self.sys_btn_icons = []

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            icon = tk.PhotoImage(file=sys_info["Icon"])
            self.sys_btn_icons.append(icon)

        max_columns = 4

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            row = i // max_columns
            column = i % max_columns

            sys_button = ttk.Button(
                sys_btn_frame,
                text=sys_info["Name"],
                image=self.sys_btn_icons[i],
                command=lambda key=sys_key: sys_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            sys_button.grid(row=row, column=column, padx=5, pady=5, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_button.bind(
                "<Enter>", lambda event, key=sys_key: self.on_hover(event, key)
            )
            sys_button.bind("<Leave>", self.on_leave)

        sys_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        sys_info_frame.pack(pady=20, padx=20, fill="both")

        # Label für die Anzeige der Beschreibung
        self.sys_info_label = tk.Label(sys_info_frame, justify="left", wraplength=900)
        self.sys_info_label.pack(anchor="w")

    # Funktion für das Hover-Ereignis
    def on_hover(self, event, key):
        self.sys_info_label.configure(text=SoftwareSys.sys_dict[key]["Description"])

    # Funktion für das Verlassen des Buttons
    def on_leave(self, event):
        self.sys_info_label.configure(text="")


class AptToolsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
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
            text=_("Alles Aktualisieren"),
            style="Accent.TButton",
            width=20,
            command=all_up_action,
        )
        #self.all_up_button.pack(fill="x")

        self.apt_option_frame = ttk.LabelFrame(
            self.update_button_frame,
            text="APT-Optionen",
        )
        self.apt_option_frame.pack(pady=10)

        self.apt_update_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt update",
            command=update_action,
            width=20,
        )

        self.apt_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.apt_upgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt upgrade",
            command=upgrade_action,
            width=20,
        )

        self.apt_upgrade_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.apt_showupgrade_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt list --upgradable",
            command=apt_showupgrade_action,
            width=25,
        )

        self.apt_showupgrade_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.apt_autoremove_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt autoremove",
            command=apt_autremove_action,
            width=20,
        )

        self.apt_autoremove_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.apt_broken_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt --fix-broken install",
            command=apt_broken_action,
            width=25,
        )

        self.apt_broken_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.apt_missing_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="apt --fix-missing install",
            command=apt_missing_action,
            width=25,
        )

        self.apt_missing_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.apt_cinfigure_a_button = ttk.Button(
            self.apt_option_frame,
            compound="left",
            text="dpkg --configure -a",
            command=apt_reconf_action,
            width=25,
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
            text="flatpak update",
            command=flatpak_update_action,
            width=20,
        )

        self.flatpak_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.flatpak_clean_button = ttk.Button(
            self.flatpak_option_frame,
            compound="left",
            text="flatpak uninstall --unused",
            command=flatpak_clean_action,
            width=25,
        )

        self.flatpak_clean_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.update_term_frame = ttk.LabelFrame(self, text=_("Prozess"))
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
            text=_("Beenden"),
            style="Accent.TButton",
            command=kill_term,
        )

        self.update_info_frame = ttk.LabelFrame(self, text="Info")
        self.update_info_frame.grid(
            row=1, column=0, columnspan=2, sticky="nesw", padx=20, pady=20
        )
        self.update_info_frame.pack_propagate(False)

        self.update_info_label = ttk.Label(
            self.update_info_frame, text="", justify="left", wraplength=900
        )
        self.update_info_label.pack(anchor="w", fill="x", padx=10, pady=5)

        self.all_up_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Aktualisiert das gesammte Betriebsystem inklusive Flatpak-Anwendungen."
            ),
        )
        self.all_up_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_update_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Bringt die Paketliste auf den neusten Stand."
            ),
        )
        self.apt_update_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_upgrade_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Aktualisiert alle installierten Pakete auf die neuste Version."
            ),
        )
        self.apt_upgrade_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_showupgrade_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Es werden aktualisierbare Pakete aufgelistet."
            ),
        )
        self.apt_showupgrade_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_autoremove_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Pakete oder Abhängikeiten, die zurückgeblieben sind werden entfernt."
            ),
        )
        self.apt_autoremove_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_broken_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Repartiert fehlerhafte oder unvollständige Paketinstallationen."
            ),
        )
        self.apt_broken_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_missing_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Lädt fehlende Pakete und deren Abhängigkeiten herunter und installiert sie."
            ),
        )
        self.apt_missing_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.apt_cinfigure_a_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Richtet alle Pakete neu ein, die nicht richtig konfiguriert wurden."
            ),
        )
        self.apt_cinfigure_a_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.flatpak_update_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Es werden alle installierten Flatpak-Programme aktualisiert."
            ),
        )
        self.flatpak_update_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )

        self.flatpak_clean_button.bind(
            "<Enter>",
            lambda event: self.update_info_label.configure(
                text="Zurückgebliebene Abhängigkeiten werden entfernt."
            ),
        )
        self.flatpak_clean_button.bind(
            "<Leave>", lambda event: self.update_info_label.configure(text="")
        )


class SourcePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")

        self.added_repositories = ttk.LabelFrame(
            self, text="Eingebundene Repositories", padding=20
        )
        self.added_repositories.pack(fill="both", expand=True, padx=20, pady=20)

        self.added_tree_frame = tk.Frame(self.added_repositories)
        self.added_tree_frame.pack(fill="both", expand=True)

        self.added_treeview = ttk.Treeview(
            self.added_tree_frame, columns=("name"), show="headings"
        )
        self.added_treeview.heading("name", text="Name")
        self.added_treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.added_tree_frame, orient="vertical", command=self.added_treeview.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.added_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.add_sources_to_treeview()

        def open_source_f_d():
            popen(f"pkexec nemo /etc/apt/sources.list.d")

        self.open_source_folder = ttk.Button(
            self.added_repositories,
            text="Quellen bearbeiten (Nur für erfahrene Nutzer!)",
            command=open_source_f_d,
            style="Custom.TButton",
        )
        self.open_source_folder.pack(pady=20, fill="x")

    def add_sources_to_treeview(self):
        sources_d1 = os.listdir("/etc/apt/sources.list.d")

        for file in sources_d1:
            self.added_treeview.insert("", "end", values=(file))
