import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
import psutil
from time import strftime
import socket
from PIL import ImageTk, Image
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_manage import count_flatpaks
from flatpak_alias_list import *
from tabs.pop_ups import *
from tool_tipps import CreateToolTip
from pathlib import Path


class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Icon für den Willkommensbildschirm laden
        self.welcome_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/pigro_icons/test2.png")
        )

        # Label für das Icon erstellen und im Fenster platzieren
        self.icon_label = ttk.Label(self, image=self.welcome_icon)
        self.icon_label.pack(pady=20)

        # Willkommensnachricht definieren
        welcome_message = """Willkommen"""

        # Label für die Willkommensnachricht erstellen
        self.welcome_label = ttk.Label(self, text=welcome_message, font=("Ubuntu",20))
        self.welcome_label.pack(pady=10)
                # Willkommensnachricht definieren
        welcome_text_message = """GuideOS ist eine Linux Distribution, dem sich Mitglieder des Forums https://linuxguides.de angenommen haben.Die Idee wurde Ende 2024 umgesetzt und hat zum Ziel auch den Einstieg oder Umstieg auf Linux für jeden Anwender verständlich zu machen. Als Basis dient UBUNTU und der Desktop Cinnamon. Viele der installierbaren Programme haben wir aus langjähriger Erfahrung ausgewählt und unser Ziel ist GuideOS mit euch gemeinsam weiter zu entwickeln. Du hast Lust ein Teil dieser Community zu sein, dann schaue doch mal bei https://forum.linuxguides.de vorbei. Dort kannst du dich auch registrieren und Fragen und Ideen los werden.\n\nWir freuen uns auf jeden, der GuideOS nutzt und auch über jede neue Idee!"""

        # Label für die Willkommensnachricht erstellen
        self.welcome_text_label = ttk.Label(self, text=welcome_text_message,wraplength=800,justify="center")
        self.welcome_text_label.pack(pady=10)

        # LabelFrame für Autostart-Optionen erstellen
        self.autostart_frame = ttk.Labelframe(self, text="Autostart")
        self.autostart_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

        def open_software_properties_tab():
            # Der Befehl und seine Argumente als Liste
            command = ["/usr/bin/software-properties-gtk", "--open-tab=4"]
            
            try:
                # subprocess.run ausführen und auf Rückgabewert prüfen
                subprocess.run(command, check=True)
                print("Software Properties erfolgreich geöffnet.")
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Öffnen von Software Properties: {e}")


        # LabelFrame für Autostart-Optionen erstellen
        self.nvidia_frame = ttk.Labelframe(self, text="BAUSTELLE!!!!!!! BAUSTELLE!!!!!!! BAUSTELLE!!!!!!! BAUSTELLE!!!!!!!")
        self.nvidia_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

        nvidia_text_message = """Dieser Bereich wird in der fertigen Version nur Angezeigt, wenn du deinen Nvidia-Teiber nicht installiert hast. JUNGE!"""

        # Label für die Willkommensnachricht erstellen
        self.nvidia_text_label = ttk.Label(self.nvidia_frame, text=nvidia_text_message,wraplength=800,justify="center")
        self.nvidia_text_label.pack(pady=10)

        self.drivers_button = ttk.Button(
                self.nvidia_frame,
                text="Zusätzliche Treiber",
                command=open_software_properties_tab,
                style="Custom.TButton",
            )
        self.drivers_button.pack(pady=10)



        # Konfigurieren der Spalten im LabelFrame
        self.autostart_frame.columnconfigure(0, weight=1)  # Spalte für den Text
        self.autostart_frame.columnconfigure(1, weight=0)  # Spalte für den Checkbutton

        # Beschreibung für Autostart hinzufügen (nimmt die erste Spalte ein)
        self.autostart_description = ttk.Label(
            self.autostart_frame,
            text=(
                "Hier kannst du den Autostart dieses Programms deaktivieren. "
                "Nach dem nächsten Start wird der Willkommensbildschirm entfernt "
                "und Piazza wird zu einem System-Tool."
            ),
            wraplength=600,
        )
        self.autostart_description.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # BooleanVar für den Autostart-Status
        self.autostart_enabled = tk.BooleanVar()

        # Checkbutton für das Umschalten des Autostarts (rechtsbündig in der zweiten Spalte)
        self.autostart_checkbutton = ttk.Checkbutton(
            self.autostart_frame,
            variable=self.autostart_enabled,
            command=self.toggle_autostart,
            style="Switch.TCheckbutton",
        )
        self.autostart_checkbutton.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Check den aktuellen Autostart-Status und setze den Checkbutton korrekt
        self.check_autostart_status()

    def check_autostart_status(self):
        """Überprüft den aktuellen Autostart-Status anhand der .desktop-Datei."""
        autostart_file = Path(
            os.path.expanduser("~/.config/autostart/primo-di-tutto-autostart.desktop")
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
            os.path.expanduser("~/.config/autostart/primo-di-tutto-autostart.desktop")
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
Version=2.1
Exec=primo-di-tutto
Name=Primo Di Tutto
GenericName=Primo
Encoding=UTF-8
Terminal=false
StartupWMClass=Primo
Type=Application
Categories=System
Icon=primo-di-tutto-logo
Path=/opt/primo-di-tutto/
X-GNOME-Autostart-enabled={'true' if autostart_enabled else 'false'}
"""
                )
