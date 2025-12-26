#!/usr/bin/python3

# import os
# import os.path
from tkinter import *
from tkinter import ttk
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_manage import *
from tabs.pop_ups import *
import gettext
import threading
from logger_config import setup_logger
import subprocess

logger = setup_logger(__name__)

lang = gettext.translation(
    "messages", localedir=f"{application_path}/src/tabs/locale", languages=["de"]
)
lang.install()
_ = lang.gettext


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
            self.terminal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

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
            self.term_quit_button.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        def kill_term():
            self.terminal.delete(1.0, tk.END)
            self.terminal.grid_forget()
            self.terminal_scroll.grid_forget()
            self.term_quit_button.grid_forget()
            self.term_logo_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        def all_up_action():
            allup = f"{permit} {application_path}/scripts/all_up"
            execute_command(allup)

        self.update_button_frame = ttk.Frame(self, padding=20)
        self.update_button_frame.pack(side="top", fill="x")

        self.all_up_button = ttk.Button(
            self.update_button_frame,
            text=_("Alles Aktualisieren"),
            style="Accent.TButton",
            width=20,
            command=all_up_action,
        )
        self.all_up_button.pack(fill="x")

        self.update_info_label = ttk.Label(
            self.update_button_frame,
            # Der text für anfänger angemessen erklären was all_up macht
            text="Hier kannst Du alle verfügbaren Aktualisierungen für Dein System installieren. Dies umfasst Updates für das Betriebssystem, installierte Software und Anwendungen aus verschiedenen Quellen wie APT und Flatpak. Klicke einfach auf 'Alles Aktualisieren', um den Prozess zu starten. Während der Aktualisierung werden alle Schritte in einem Terminalfenster angezeigt, damit Du den Fortschritt verfolgen kannst.",
            justify="left",
            # Der zeilenumbruch soll eine gute lesbarkeit haben
            wraplength=950,
        )
        self.update_info_label.pack(anchor="nw", fill="x", pady=5)

        self.update_term_frame = ttk.LabelFrame(self, text=_("Prozess"))
        self.update_term_frame.pack(
            side="top", fill="both", expand=True, padx=20, pady=20
        )

        # Configure grid weights for proper resizing
        self.update_term_frame.grid_rowconfigure(0, weight=1)
        self.update_term_frame.grid_columnconfigure(0, weight=1)

        self.term_logo_label = Label(
            self.update_term_frame,
            image=self.term_logo,
        )

        # self.term_logo_label soll zentriert sein
        self.term_logo_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
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
