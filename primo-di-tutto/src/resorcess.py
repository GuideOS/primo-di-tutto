#!/usr/bin/python3

import os
from os import popen
import os.path
import distro
import subprocess
from subprocess import TimeoutExpired
from tabs.system_tab_check import check_pipanel
import requests
import platform
from constants import NotificationUrgency
import re
from logger_config import setup_logger

logger = setup_logger(__name__)


def ping_github():
    try:
        response = requests.get("https://api.github.com", timeout=5)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False


ping_github()
user = os.environ["USER"]


current_version = "0.6.2"

logger.info(f"You are using Primo Di Tutto {current_version}")

def create_plank_directories():
    directories = [
        os.path.expanduser("~/.local/share/plank/themes"),
        os.path.expanduser("~/.config/plank")
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Verzeichnis erstellt: {directory}")
        else:
            logger.info(f"Verzeichnis existiert bereits: {directory}")

create_plank_directories()

home = os.path.expanduser("~")


script_dir = os.path.dirname(os.path.abspath(__file__))
application_path = os.path.dirname(script_dir)

autostart_dir_path = f"{home}/.config/autostart/"

if not os.path.exists(autostart_dir_path):
    os.makedirs(autostart_dir_path)

    logger.info(f"{autostart_dir_path} created successfully")

else:
    logger.info(f"{autostart_dir_path} already exists")


primo_config_dir = f"{home}/.primo"
primo_config_file = f"{primo_config_dir}/primo.conf"

if not os.path.exists(primo_config_dir):
    os.mkdir(primo_config_dir)

    with open(primo_config_file, "w") as f:
        f.write("[Primo Di Tutto Configs]\n\nfirstrun=yes")


def get_first_run():
    # Pfad zur Konfigurationsdatei
    primo_config_file = os.path.expanduser("~/.primo/primo.conf")

    # Die Datei Zeile für Zeile durchgehen
    with open(primo_config_file, "r") as file:
        for line in file:
            if line.startswith("firstrun="):
                # Den Wert nach dem Gleichheitszeichen extrahieren
                firstrun_value = line.split("=")[1].strip()
                logger.info(f"firstrun: {firstrun_value}")

    return firstrun_value


distro_get = distro.id()

nice_name = popen("egrep '^(PRETTY_NAME)=' /etc/os-release")
nice_name = nice_name.read()

machiene_arch = platform.machine()
logger.info(platform.machine())
architecture_arch = platform.architecture()[0]
logger.info(platform.architecture()[0])

if machiene_arch == "x86_64" and architecture_arch == "64bit":
    os_arch_output = "amd64"
if machiene_arch == "aarch64" and architecture_arch == "64bit":
    os_arch_output = "arm64"


def send_notification(message: str, title="Primo Di Tutto", icon_path="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png", urgency: str = NotificationUrgency.NORMAL):
    command = ["notify-send", title, message, "-u", urgency]
    if icon_path:
        command.extend(["-i", icon_path])
    subprocess.run(command)



def run_command(command):
    """Helper function to run shell commands and capture output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300, # 5 Minutes Timeout
            text=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error("Fehler bei der Ausführung des Befehls", e)
        return False, None
    except TimeoutExpired as e:
        logger.error("Timeout bei der Ausführung des Befehls", e)
        return False, None
    except PermissionError as e:
        logger.error("Fehlende Berechtigungen", e)
        return False, None
    except Exception as e:
        logger.exception("Unbekannter Fehler", e)
        return False, None


def get_desktop_environment():
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP").lower()
    # print(xdg_current_desktop)
    # Check for specific desktop environments
    if xdg_current_desktop == "x-cinnamon" or xdg_current_desktop == "cinnamon":
        return "CINNAMON"
    elif xdg_current_desktop == "unity":
        return "UNITY"
    elif xdg_current_desktop == "ubuntu:gnome":
        return "GNOME"
    elif "gnome" in xdg_current_desktop:
        return "GNOME"
    elif "plasma" == xdg_current_desktop or "kde" == xdg_current_desktop:
        return "KDE"
    elif "xfce" == xdg_current_desktop:
        return "XFCE"
    elif "lxde" == xdg_current_desktop:
        return "LXDE"
    elif "lxde-pi-wayfire" == xdg_current_desktop:
        return "PI-WAYFIRE"
    elif "mate" == xdg_current_desktop:
        return "MATE"
    else:
        return "Unknown"


def get_lxde_theme_name():
    """Retrieve the current theme for LXDE from the desktop.conf file."""
    directory_path = os.path.expanduser("~/.config/lxsession/LXDE-pi/")
    config_file_path = os.path.join(directory_path, "desktop.conf")

    # Ensure ~/.config/lxsession/LXDE-pi/desktop.conf exists
    if not os.path.exists(directory_path):
        logger.info("Directory does not exist. Creating", directory_path)
        os.makedirs(directory_path)
        with open(config_file_path, "w") as f:
            f.write(
                """[GTK]
sNet/ThemeName=PiXflat
sGtk/ColorScheme=selected_bg_color:#87919B\nselected_fg_color:#F0F0F0\nbar_bg_color:#EDECEB\nbar_fg_color:#000000\n
sGtk/FontName=PibotoLt 12
iGtk/ToolbarIconSize=3
sGtk/IconSizes=gtk-large-toolbar=24,24
iGtk/CursorThemeSize=24"""
            )
        return "PiXflat"
    else:
        with open(config_file_path, "r") as file:
            for line in file:
                if "sNet/ThemeName=" in line:
                    theme_name = line.split("=")[1].strip()
                    return theme_name
        return "Theme not found."


def get_theme():
    """Get the current GTK or KDE theme based on the desktop environment."""
    de = get_desktop_environment()

    if not de:
        return "Desktop Environment not detected."

    # KDE/Plasma
    if "KDE" in de or "PLASMA" in de:
        kde_config_file = os.path.expanduser("~/.config/kdeglobals")
        if os.path.exists(kde_config_file):
            success, kde_theme = run_command(f"grep 'Name=' {kde_config_file}")
            if kde_theme:
                return kde_theme.split("=")[-1].strip().strip("'")
        return "KDE theme not found."

    elif "CINNAMON" in de:
        success, theme = run_command("gsettings get org.cinnamon.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "UNITY" in de:
        success, theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "GNOME" in de:
        success, theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "BUDGIE" in de:
        success, theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "PI-WAYFIRE" in de:
        success, theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "MATE" in de:
        success, theme = run_command("gsettings get org.mate.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "XFCE" in de:
        success, theme = run_command("xfconf-query -c xsettings -p /Net/ThemeName")
        return theme.strip("'") if theme else "Theme not found."
    elif "LXDE" in de or "LXDE-PI" in de:
        return get_lxde_theme_name()

    return "Unsupported Desktop Environment."


theme_name = get_theme()
# logger.debug(f"Current theme: {theme_name}")


# Define Permission Method
def pi_identify():
    if get_desktop_environment == "lxde-pi-wayfire" or check_pipanel() == True:
        os_name_tag = "pi_os"
    else:
        os_name_tag = distro_get
    return os_name_tag


if pi_identify() == "pi_os":
    permit = "sudo"
else:
    permit = "pkexec"

theme = get_theme().lower()

def has_nvidia_gpu():
    try:
        # lspci -nnk ausführen
        output = subprocess.check_output(['lspci', '-nnk'], text=True)
    except subprocess.CalledProcessError as e:
        print("Fehler beim Ausführen von lspci:", e)
        return False
    except FileNotFoundError:
        print("lspci ist nicht installiert oder nicht im PATH.")
        return False

    # Alle VGA-Abschnitte extrahieren
    lines = output.splitlines()
    capture = False
    for line in lines:
        if re.search(r'VGA compatible controller', line):
            capture = True
            if "NVIDIA" in line:
                return True  # NVIDIA gefunden
        elif capture:
            if not (line.startswith('\t') or line.startswith(' ')):
                capture = False  # Ende der Section
            elif "NVIDIA" in line:
                return True  # NVIDIA innerhalb des Blocks gefunden

    return False

# Font Definition Vars
font_20 = ("Sans", 20)
font_16_b = ("Sans", 16, "bold")
font_16 = ("Sans", 16)
font_14 = ("Sans", 14)
font_12_b = ("Sans", 12, "bold")
font_12 = ("Sans", 12)
font_10 = ("Sans", 11)
font_10_b = ("Sans", 10, "bold")
font_9_b = ("Sans", 9, "bold")
font_9 = ("Sans", 9)
font_8_b = ("Sans", 8, "bold")
font_8 = ("Sans", 8)
