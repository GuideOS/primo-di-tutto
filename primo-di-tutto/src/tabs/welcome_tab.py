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
from tabs.pop_ups import *
from tabs.software_tab import Custom_Installer
import subprocess
import re
import gettext
lang = gettext.translation('messages', localedir=f"{application_path}/src/tabs/locale", languages=['de'])
lang.install()
_ = lang.gettext



class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Icon für den Willkommensbildschirm laden

        if "dark" in theme_name or "Dark" in theme_name:
            self.welcome_icon = ImageTk.PhotoImage(
                Image.open(f"{application_path}/images/icons/pigro_icons/guideo_font_logo_dark.png")
            )
        else:
            self.welcome_icon = ImageTk.PhotoImage(
                Image.open(f"{application_path}/images/icons/pigro_icons/guideo_font_logo_light.png")
            )




        self.nvidia_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/nvidia-attentione.png")
        )



        # Label für das Icon erstellen und im Fenster platzieren
        self.icon_label = ttk.Label(self, image=self.welcome_icon)
        self.icon_label.pack(pady=20)

        # Willkommensnachricht definieren
        welcome_message = _("""Welcome""")

        # Label für die Willkommensnachricht erstellen
        self.welcome_label = ttk.Label(self, text=welcome_message, font=("Ubuntu",20))
        self.welcome_label.pack(pady=10)
                # Willkommensnachricht definieren
        welcome_text_message = _("""GuideOS is a Linux distribution developed by members of the forum [https://linuxguides.de](https://linuxguides.de). The concept was realized at the end of 2024 and aims to make starting or switching to Linux understandable for every user. Based on Debian and featuring the Cinnamon desktop, we have selected many of the installable programs based on years of experience. Our goal is to further develop GuideOS together with you. Are you interested in becoming part of this community? Then check out [https://forum.linuxguides.de](https://forum.linuxguides.de). There, you can register, ask questions, and share your ideas. We look forward to everyone who uses GuideOS and welcome every new idea!""")

        # Label für die Willkommensnachricht erstellen
        self.welcome_text_label = ttk.Label(self, text=welcome_text_message,wraplength=800,justify="center")
        self.welcome_text_label.pack(pady=10)

        # LabelFrame für Autostart-Optionen erstellen
        self.autostart_frame = ttk.Labelframe(self, text="Autostart")
        self.autostart_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

        def get_gpu_model_inxi():
            try:
                output = subprocess.check_output("inxi -G", shell=True, text=True)
                gpu_model = output.strip()
                #print("GPU Modell (über inxi):", gpu_model)
                return gpu_model
            except subprocess.CalledProcessError:
                print("Fehler beim Auslesen des GPU-Modells über inxi.")
                return None


        def check_nvidia_driver():
            try:
                driver_info = subprocess.check_output("nvidia-smi --query-gpu=driver_version --format=csv,noheader", shell=True, text=True)
                print("NVIDIA Treiber Version:", driver_info.strip())
                return True
            except subprocess.CalledProcessError:
                print("NVIDIA-Treiber nicht installiert, möglicherweise läuft der Nouveau-Treiber.")
                return False

        def check_nvidia_gpu():
            try:
                if "NVIDIA" in get_gpu_model_inxi():
                    return True
                else:
                    return False
            except subprocess.CalledProcessError as e:
                print("Error running 'lspci'")
                return False


        def get_nvidia_gpu_model():
            try:
                model_info = subprocess.check_output("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True, text=True)
                model = model_info.strip()
                print("NVIDIA GPU Modell:", model)
                return model
            except subprocess.CalledProcessError:
                print("Fehler beim Abrufen des NVIDIA-GPU-Modells. Bitte überprüfen Sie, ob 'nvidia-smi' installiert ist.")
                return None

        def open_software_properties_tab():
            popen(
                f"x-terminal-emulator -e 'bash -c \"pkexec apt install nvidia-driver-assistant && clear && nvidia-driver-assistant; exec bash\"'"
            )


        def driver_recognition():
            if check_nvidia_gpu():
                print("NVIDIA-GPU erkannt.")
                if check_nvidia_driver():
                    get_nvidia_gpu_model()  # Modell der GPU abrufen und ausgeben
                else:
                    self.nvidia_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)
            else:
                print("Keine NVIDIA-GPU erkannt.")

        





        # LabelFrame für Autostart-Optionen erstellen
        self.nvidia_frame = ttk.Labelframe(self, text="NVIDIA-Treiber")
        #self.nvidia_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)
        driver_recognition()
        nvidia_text_message = """Das System hat erkannt das noch kein Treiber für die Eingebaue Grafikarte installiert ist."""

        # Label für die Willkommensnachricht erstellen
        self.nvidia_text_label = ttk.Label(self.nvidia_frame, text=nvidia_text_message,image=self.nvidia_icon, wraplength=800,justify="center",compound="left")
        self.nvidia_text_label.pack(pady=10,padx=10,fill="x")

        self.drivers_button = ttk.Button(
                self.nvidia_frame,
                text="Nvidia Treiber installieren",
                command=open_software_properties_tab,
                style="Accent.TButton",
            )
        self.drivers_button.pack(pady=10,padx=10,fill="x")



        # Konfigurieren der Spalten im LabelFrame
        self.autostart_frame.columnconfigure(0, weight=1)  # Spalte für den Text
        self.autostart_frame.columnconfigure(1, weight=0)  # Spalte für den Checkbutton

        # Beschreibung für Autostart hinzufügen (nimmt die erste Spalte ein)
        self.autostart_description = ttk.Label(
            self.autostart_frame,
            text=_("Hier kannst Du den Autostart dieses Programms deaktivieren. Nach dem nächsten Start wird der Willkommensbildschirm entfernt, und Primo wird zu einem Systemtool."
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
        #self.check_autostart_status()

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
                    f"""#!/usr/bin/env xdg-open
[Desktop Entry]
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
