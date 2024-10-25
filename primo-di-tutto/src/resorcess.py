#!/usr/bin/python3

import os
from os import popen
import os.path
import distro
import subprocess
from tabs.system_tab_check import check_pipanel
import requests
import platform


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


current_version = "0.4.6"

print(f"[Info] You are using Primo Di Tutto {current_version}")


home = os.path.expanduser("~")


script_dir = os.path.dirname(os.path.abspath(__file__))
application_path = os.path.dirname(script_dir)

autostart_dir_path = f"{home}/.config/autostart/"

if not os.path.exists(autostart_dir_path):
    os.makedirs(autostart_dir_path)

    print(f"[Info] {autostart_dir_path} created successfully")

else:
    print(f"[Info] {autostart_dir_path} already exists")


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
                print(f"[Info] firstrun: {firstrun_value}")

    return firstrun_value


distro_get = distro.id()

nice_name = popen("egrep '^(PRETTY_NAME)=' /etc/os-release")
nice_name = nice_name.read()

machiene_arch = platform.machine()
print(platform.machine())
architecture_arch = platform.architecture()[0]
print(platform.architecture()[0])

if machiene_arch == "x86_64" and architecture_arch == "64bit":
    os_arch_output = "amd64"
if machiene_arch == "aarch64" and architecture_arch == "64bit":
    os_arch_output = "arm64"


def run_command(command):
    """Helper function to run shell commands and capture output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


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
        print("Directory does not exist. Creating", directory_path)
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
            kde_theme = run_command(f"grep 'Name=' {kde_config_file}")
            if kde_theme:
                return kde_theme.split("=")[-1].strip().strip("'")
        return "KDE theme not found."

    elif "CINNAMON" in de:
        theme = run_command("gsettings get org.cinnamon.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "UNITY" in de:
        theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "GNOME" in de:
        theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "BUDGIE" in de:
        theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."

    elif "PI-WAYFIRE" in de:
        theme = run_command("gsettings get org.gnome.desktop.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "MATE" in de:
        theme = run_command("gsettings get org.mate.interface gtk-theme")
        return theme.strip("'") if theme else "Theme not found."
    elif "XFCE" in de:
        theme = run_command("xfconf-query -c xsettings -p /Net/ThemeName")
        return theme.strip("'") if theme else "Theme not found."
    elif "LXDE" in de or "LXDE-PI" in de:
        return get_lxde_theme_name()

    # Fallback for unknown DE
    return "Unsupported Desktop Environment."


theme_name = get_theme()
# print(f"Current theme: {theme_name}")


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

# if "dark" in theme or "noir" in theme:
maincolor = "#1e1e1e"
nav_color = "#242424"
nav2_color = "#131313"
frame_color = "#1e1e1e"
main_font = "white"
info_color = "yellow"
ext_btn = "#007acc"
ext_btn_font = "white"
label_frame_color = "#cf274e"
# else:
# maincolor = "#f5f5f5"
# nav_color = "#d3d3d3"
# nav2_color = "#383838"
# frame_color = "#f5f5f5"
# main_font = "#454545"
# info_color = "#0075b7"
# ext_btn = "#d3d3d3"
# ext_btn_font = "#454545"
# label_frame_color = "#454545"


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
