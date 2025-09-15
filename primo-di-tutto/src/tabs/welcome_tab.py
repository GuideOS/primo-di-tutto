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
from logger_config import setup_logger

logger = setup_logger(__name__)

# Set up gettext
gettext.bindtextdomain('primo-di-tutto', f'{application_path}/src/locale')
gettext.textdomain('primo-di-tutto')
_ = gettext.gettext

#user = "live"


class WelcomeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

    # Load icon for welcome screen

        self.welcome_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/guideo_font_logo_dark.png")
        )
        self.nvidia_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/nvidia-attentione.png")
        )
        self.guide_horn = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/guidehorn.png")
        )

    # Create label for icon and place in window
        self.icon_label = ttk.Label(self, image=self.welcome_icon)
        self.icon_label.pack(pady=10)

        # Custom logic for 'live' or 'linux' user
        if user.lower() in ["live", "linux"]:
            welcome_message = _("Hello!")
            welcome_text_message = _("Thank you for trying GuideOS. You are currently in live mode. Feel free to look around, and if you want, you can install GuideOS using the starter on the desktop. We wish you lots of fun.")
            show_autostart = False
        else:
            welcome_message = _("Welcome") + f" {user.upper()} " + "!"
            welcome_text_message = _("Your easy start into the world of Linux\nGuideOS is a Linux distribution created by members of the Linux Guides Forum. It was developed at the end of 2024 to find a way into the world of Linux together with the community. Our goal is not only to create an operating system, but above all to experience the joint development process. The journey is the destination!\n\nGuideOS is not only aimed at beginners and switchers, but invites everyone interested to participate – even without programming knowledge. Everyone can contribute, whether by testing new features, bringing in ideas, or sharing experiences. The current focus is to see whether we can successfully launch such a distribution together with the community. If you have questions, want to contribute ideas, or simply want to be part of this growing community – visit us in the forum at forum.linuxguides.de. We welcome everyone who uses and helps shape GuideOS!")
            show_autostart = True

        # Create label for welcome message
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
            # Create LabelFrame for autostart options
            self.autostart_frame = ttk.Labelframe(self, text=_("Autostart"))
            self.autostart_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

            # Configure columns in LabelFrame
            self.autostart_frame.columnconfigure(0, weight=1)
            self.autostart_frame.columnconfigure(1, weight=0)

            # Add description for autostart (occupies first column)
            self.autostart_description = ttk.Label(
                self.autostart_frame,
                text=_("Here you can disable the autostart of this program. After the next start, the welcome screen will be removed and Primo will become a system tool."),
                wraplength=600,
            )
            self.autostart_description.grid(
                row=0, column=0, padx=10, pady=10, sticky="w"
            )

            # BooleanVar for autostart status
            self.autostart_enabled = tk.BooleanVar()

            # Checkbutton for toggling autostart (right-aligned in second column)
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
                    text=_("Open NVIDIA Manager"),
                    image=self.nvidia_icon,
                    compound="left",
                    command=open_nvidia_manager,
                )
                self.nvidia_button.pack(pady=10)

        # Check den aktuellen Autostart-Status und setze den Checkbutton korrekt
        # self.check_autostart_status()

    def check_autostart_status(self):
        """Checks the current autostart status based on the .desktop file."""
        autostart_file = Path(
            os.path.expanduser("/etc/xdg/autostart/primo-di-tutto.desktop")
        )

    # Sets the checkbutton status based on the .desktop file
        if autostart_file.exists():
            with open(autostart_file, "r") as file:
                for line in file:
                    if line.startswith("X-GNOME-Autostart-enabled="):
                        self.autostart_enabled.set(line.strip().endswith("true"))
                        break
        else:
            self.autostart_enabled.set(False)

    def toggle_autostart(self):
        """Updates both the config file and the autostart desktop file."""
    # Path to config file
        config_file_path = Path(os.path.expanduser("~/.primo/primo.conf"))
        autostart_file_path = Path(
            os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop")
        )

        # 1. Konfigurationsdatei bearbeiten (firstrun auf 'no' setzen)
        self.update_config_file(config_file_path)

        # 2. Autostart-Desktop-Datei aktualisieren
        self.update_autostart_file(autostart_file_path)

    def update_config_file(self, config_file_path):
        """Updates the config file to disable autostart."""
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

            # If "firstrun=" not found, add at end
            if not firstrun_set:
                config_file.write("firstrun=no\n")

    def update_autostart_file(self, autostart_file_path):
        """Updates the .desktop file for autostart based on the checkbutton status."""
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
