import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
from resorcess import *
from pathlib import Path
import subprocess
import gettext
from logger_config import setup_logger

logger = setup_logger(__name__)

lang = gettext.translation(
    "messages", localedir=f"{application_path}/src/tabs/locale", languages=["de"]
)
lang.install()
_ = lang.gettext

# user = "live"


class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Icon für den Willkommensbildschirm laden

        self.welcome_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/guideo_font_logo_dark.png")
        )
        self.nvidia_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/nvidia-attentione.png")
        )
        self.guide_horn = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/guidehorn.png")
        )

        # Label für das Icon erstellen und im Fenster platzieren
        self.icon_label = ttk.Label(self, image=self.welcome_icon)
        self.icon_label.pack(pady=10)

        # Custom logic for 'live' or 'linux' user
        if user.lower() in ["live", "linux"]:
            welcome_message = "Hallo!"
            welcome_text_message = "Schön, dass du dir GuideOS anschaust. Du befindest dich im Live-Modus. Guck' dich in Ruhe um und wenn du möchste kannst du GuideOS über den Starter auf dem Desktop installieren. Wir wünschen dir viele Spaß."
            show_autostart = False
        else:
            welcome_message = _("""Welcome""") + f" {user.upper()} " + "!"
            welcome_text_message = """Dein einfacher Einstieg in die Welt von Linux
GuideOS ist eine Linux-Distribution, die von Mitgliedern des Linux Guides Forums ins Leben gerufen wurde. Sie wurde Ende 2024 entwickelt, um mit der Community gemeinsam einen Weg in die Welt von Linux zu finden. Unser Ziel ist es nicht nur, ein Betriebssystem zu schaffen, sondern vor allem den gemeinsamen Entwicklungsprozess zu erleben. Der Weg ist das Ziel!

GuideOS richtet sich nicht nur an Anfänger und Umsteiger, sondern lädt alle Interessierten ein, mitzuwirken – auch ohne Programmierkenntnisse. Jeder kann etwas beitragen, sei es durch das Testen neuer Funktionen, das Einbringen von Ideen oder das Teilen von Erfahrungen. Der Schwerpunkt liegt aktuell darauf, zu schauen, ob wir gemeinsam mit der Community eine solche Distribution erfolgreich auf die Beine stellen können. Ob du Fragen hast, Ideen einbringen oder einfach nur Teil dieser wachsenden Gemeinschaft werden möchtest – besuche uns im Forum unter forum.linuxguides.de. Wir freuen uns über jeden, der GuideOS nutzt und mitgestaltet!
"""
            show_autostart = True

        # Label für die Willkommensnachricht erstellen
        self.welcome_label = Label(
            self,
            text=welcome_message,
            font=("Ubuntu", 20),
            highlightthickness=0,
            borderwidth=0,
        )
        self.welcome_label.pack(pady=5)

        # Create the welcome text label first
        self.welcome_text_label = ttk.Label(
            self, text=welcome_text_message, wraplength=800, justify="left"
        )
        self.welcome_text_label.pack(pady=10)

        # If user is 'live' or 'linux', set image and compound
        if user.lower() in ["live", "linux"]:
            self.welcome_text_label.configure(image=self.guide_horn, compound="bottom")

        # Only show autostart frame if show_autostart is True
        if show_autostart:
            # LabelFrame für Autostart-Optionen erstellen
            self.autostart_frame = ttk.Labelframe(self, text="Autostart")
            self.autostart_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

            # Konfigurieren der Spalten im LabelFrame
            self.autostart_frame.columnconfigure(0, weight=1)  # Spalte für den Text
            self.autostart_frame.columnconfigure(
                1, weight=0
            )  # Spalte für den Checkbutton

            # Beschreibung für Autostart hinzufügen (nimmt die erste Spalte ein)
            self.autostart_description = ttk.Label(
                self.autostart_frame,
                text=_(
                    "Hier kannst Du den Autostart dieses Programms deaktivieren. Nach dem nächsten Start wird der Willkommensbildschirm entfernt, und Primo wird zu einem Systemtool."
                ),
                wraplength=600,
            )
            self.autostart_description.grid(
                row=0, column=0, padx=10, pady=10, sticky="w"
            )

            # BooleanVar für den Autostart-Status
            self.autostart_enabled = tk.BooleanVar()

            # Checkbutton für das Umschalten des Autostarts (rechtsbündig in der zweiten Spalte)
            self.autostart_checkbutton = ttk.Checkbutton(
                self.autostart_frame,
                variable=self.autostart_enabled,
                command=self.toggle_autostart,
                style="Switch.TCheckbutton",
            )
            self.autostart_checkbutton.grid(
                row=0, column=1, padx=10, pady=10, sticky="e"
            )

        # Only show NVIDIA button if not 'live' or 'linux' user
        if user.lower() not in ["live", "linux"]:
            if has_nvidia_gpu():
                # Function to start the NVIDIA manager
                def open_nvidia_manager():
                    try:
                        subprocess.Popen(["/usr/lib/guideos-nvidia-tools/main"])
                    except Exception as e:
                        logger.error(f"Error starting NVIDIA Manager: {e}")

                self.nvidia_button = ttk.Button(
                    self,
                    text=_("NVIDIA-Manager öffnen"),
                    image=self.nvidia_icon,
                    compound="left",
                    command=open_nvidia_manager,
                )
                self.nvidia_button.pack(pady=10)

        # Check den aktuellen Autostart-Status und setze den Checkbutton korrekt
        # self.check_autostart_status()

    def check_autostart_status(self):
        """Überprüft den aktuellen Autostart-Status anhand der .desktop-Datei."""
        autostart_file = Path(
            os.path.expanduser("/etc/xdg/autostart/primo-di-tutto.desktop")
        )

        # Setzt den Checkbutton-Status basierend auf der .desktop-Datei
        if autostart_file.exists():
            with open(autostart_file, "r") as file:
                for line in file:
                    if line.startswith("X-GNOME-Autostart-enabled="):
                        self.autostart_enabled.set(line.strip().endswith("true"))
                        break
        else:
            self.autostart_enabled.set(False)

    def toggle_autostart(self):
        """Aktualisiert sowohl die Konfigurationsdatei als auch die Autostart-Desktop-Datei."""
        # Pfad zur Konfigurationsdatei
        config_file_path = Path(os.path.expanduser("~/.primo/primo.conf"))
        autostart_file_path = Path(
            os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop")
        )

        # 1. Konfigurationsdatei bearbeiten (firstrun auf 'no' setzen)
        self.update_config_file(config_file_path)

        # 2. Autostart-Desktop-Datei aktualisieren
        self.update_autostart_file(autostart_file_path)

    def update_config_file(self, config_file_path):
        """Aktualisiert die Konfigurationsdatei, um den Autostart zu deaktivieren."""
        if config_file_path.exists():
            with open(config_file_path, "r") as config_file:
                config_lines = config_file.readlines()
        else:
            config_lines = []

        with open(config_file_path, "w") as config_file:
            firstrun_set = False
            for line in config_lines:
                if line.startswith("firstrun="):
                    config_file.write("firstrun=no\n")
                    firstrun_set = True
                else:
                    config_file.write(line)

            # Falls "firstrun=" nicht gefunden wurde, am Ende hinzufügen
            if not firstrun_set:
                config_file.write("firstrun=no\n")

    def update_autostart_file(self, autostart_file_path):
        """Aktualisiert die .desktop-Datei für den Autostart basierend auf dem Checkbutton-Status."""
        autostart_enabled = self.autostart_enabled.get()

        # Datei lesen, wenn sie existiert
        if autostart_file_path.exists():
            with open(autostart_file_path, "r") as file:
                lines = file.readlines()

            # Autostart-Eintrag aktualisieren
            with open(autostart_file_path, "w") as file:
                for line in lines:
                    if line.startswith("X-GNOME-Autostart-enabled="):
                        file.write(
                            f"X-GNOME-Autostart-enabled={'true' if autostart_enabled else 'false'}\n"
                        )
                    else:
                        file.write(line)
        else:
            # Wenn die Datei nicht existiert, wird sie neu erstellt
            with open(autostart_file_path, "w") as file:
                file.write(
                    f"""[Desktop Entry]
Type=Application
Exec=python3 /opt/primo-di-tutto/src/main.py
X-GNOME-Autostart-enabled=false
NoDisplay=false
Hidden=false
Name[de_DE]=primo-di-tutto.desktop
Comment[de_DE]=Keine Beschreibung
X-GNOME-Autostart-Delay=0
"""
                )
