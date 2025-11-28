#!/usr/bin/python3

import os
from os import popen
import os.path
import distro
import subprocess
from subprocess import TimeoutExpired
import requests
import platform
from constants import NotificationUrgency
import re
from logger_config import setup_logger

logger = setup_logger(__name__)


def ping_github():
    try:
        response = requests.get("https://api.github.com", timeout=1)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False


user = os.environ["USER"]


current_version = "0.6.2"

logger.info(f"You are using Primo Di Tutto {current_version}")


def create_plank_directories():
    directories = [
        os.path.expanduser("~/.local/share/plank/themes"),
        os.path.expanduser("~/.config/plank"),
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory created: {directory}")
        else:
            logger.info(f"Directory already exists: {directory}")


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
    # Path to the configuration file
    primo_config_file = os.path.expanduser("~/.primo/primo.conf")

    # Read the file line by line
    with open(primo_config_file, "r") as file:
        for line in file:
            if line.startswith("firstrun="):
                # Extract the value after the equals sign
                firstrun_value = line.split("=")[1].strip()
                logger.info(f"firstrun: {firstrun_value}")

    return firstrun_value


distro_get = distro.id()

nice_name = None  # Lazy loaded

def get_nice_name():
    global nice_name
    if nice_name is None:
        p = popen("egrep '^(PRETTY_NAME)=' /etc/os-release")
        nice_name = p.read()
    return nice_name

machiene_arch = platform.machine()
logger.info(platform.machine())
architecture_arch = platform.architecture()[0]
logger.info(platform.architecture()[0])

if machiene_arch == "x86_64" and architecture_arch == "64bit":
    os_arch_output = "amd64"
if machiene_arch == "aarch64" and architecture_arch == "64bit":
    os_arch_output = "arm64"


def send_notification(
    message: str,
    title="Primo Di Tutto",
    icon_path="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png",
    urgency: str = NotificationUrgency.NORMAL,
):
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
            timeout=300,  # 5 Minutes Timeout
            text=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error("Error while executing the command", e)
        return False, None
    except TimeoutExpired as e:
        logger.error("Timeout while executing the command", e)
        return False, None
    except PermissionError as e:
        logger.error("Missing permissions", e)
        return False, None
    except Exception as e:
        logger.exception("Unknown error", e)
        return False, None


def get_desktop_environment():
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if xdg_current_desktop in ["x-cinnamon", "cinnamon"]:
        return "CINNAMON"
    return "Unknown"



def get_theme():
    try:
        output = subprocess.check_output(
            "gsettings get org.cinnamon.desktop.interface gtk-theme",
            shell=True,
            universal_newlines=True,
        )
        return output.strip().strip("'")
    except Exception:
        return "N/A"


theme_name = None  # Lazy loaded
theme = None  # Lazy loaded

def get_theme_cached():
    global theme_name, theme
    if theme_name is None:
        theme_name = get_theme()
        theme = theme_name.lower()
    return theme_name

# Define Permission Method
permit = "pkexec"


def has_nvidia_gpu():
    try:
        # Execute lspci -nnk
        output = subprocess.check_output(["lspci", "-nnk"], text=True)
    except subprocess.CalledProcessError as e:
        print("Error while executing lspci:", e)
        return False
    except FileNotFoundError:
        print("lspci is not installed or not in PATH.")
        return False

    # Extract all VGA sections
    lines = output.splitlines()
    capture = False
    for line in lines:
        if re.search(r"VGA compatible controller", line):
            capture = True
            if "NVIDIA" in line:
                return True  # NVIDIA found
        elif capture:
            if not (line.startswith("\t") or line.startswith(" ")):
                capture = False  # End of section
            elif "NVIDIA" in line:
                return True  # NVIDIA found within the block

    return False


def get_cinnamon_version():
    """Einfache Funktion um die Cinnamon Version zu ermitteln."""
    try:
        result = popen("dpkg-query -W -f='${Version}' cinnamon").read().strip().strip("'\"")
        return result if result else "N/A"
    except:
        return "N/A"


def print_cinnamon_version():
    """Gibt die Cinnamon Version direkt aus."""
    version = get_cinnamon_version()
    print(f"Cinnamon Version: {version}")
    return version