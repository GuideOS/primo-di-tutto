import os
import json
import subprocess
import socket
import platform
from resorcess import home
from logger_config import setup_logger
from cache import Cache

logger = setup_logger(__name__)


def count_flatpaks():
    if flatpak_path:
        flat_count = os.popen("flatpak list | wc --lines")
        flat_counted = flat_count.read()
        flat_count.close()
        flat_counted = flat_counted[:-1]
    else:
        flat_counted = "-"
    return flat_counted


def is_internet_available():
    try:
        host = socket.gethostbyname("www.github.com")
        socket.create_connection((host, 80), 2)
        return True
    except socket.error:
        pass
    return False

def refresh_flatpak_installs():
    result = Cache.get('flatpak_installs')
    if result is None:
        result = Cache.set_result('flatpak_installs', load_flatpak_installs)

    return result


def load_flatpak_installs():
    command = "flatpak list --columns=name --columns=application --app"
    output = subprocess.check_output(command, shell=True, text=True)
    logger.debug(output)

    lines = output.strip().split("\n")
    data = {}

    for line in lines:
        if not line.startswith("Name\tApplication"):
            split_values = line.split("\t")
            if len(split_values) == 2:
                name, application = split_values
                data[name] = application
            elif line.strip():
                logger.error(f"Warnung: Unerwartetes Format in Zeile '{line}'")

    json_file_path = f"{home}/.primo/flatpak_installed.json"
    expanded_json_file_path = os.path.expanduser(json_file_path)

    with open(expanded_json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)

    with open(expanded_json_file_path, "r") as json_file:
        flat_uninstalled_dict = json.load(json_file)

    logger.debug(flat_uninstalled_dict)
    return flat_uninstalled_dict


# Check ob Flatpak installiert ist
flatpak_path = os.path.exists("/bin/flatpak")


if flatpak_path:
    logger.info("Flatpak is installed. List will be added")

    home = os.path.expanduser("~")
    json_file_path = f"{home}/.primo/flat_remote_data.json"
    expanded_json_file_path = os.path.expanduser(json_file_path)

    if is_internet_available():
        command = f"flatpak remote-ls --columns=name --columns=application --app --arch={platform.machine()}"
        output = subprocess.check_output(command, shell=True, text=True)

        lines = output.strip().split("\n")
        flat_remote_data = {}

        for line in lines[1:]:
            name, application = line.split("\t")
            flat_remote_data[name] = application

        if os.path.exists(expanded_json_file_path):
            with open(expanded_json_file_path, "r") as json_file:
                flat_remote_dict = json.load(json_file)
        else:
            flat_remote_dict = {}

        flat_remote_dict.update(flat_remote_data)

        with open(expanded_json_file_path, "w") as json_file:
            json.dump(flat_remote_dict, json_file, indent=2)

        Flat_remote_dict = flat_remote_dict
        logger.info(f"Added Flatpak cache.")
    else:
        if os.path.exists(expanded_json_file_path):
            with open(expanded_json_file_path, "r") as json_file:
                Flat_remote_dict = json.load(json_file)
        else:
            Flat_remote_dict = {}

    refresh_flatpak_installs()
else:
    logger.info("Flatpak is not installed")
    Flat_remote_dict = {}
    flat_counted = "-"

#print(Flat_remote_dict)