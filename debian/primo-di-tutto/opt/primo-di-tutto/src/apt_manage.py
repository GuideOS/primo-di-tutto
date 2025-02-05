import apt
import os
from os import popen
import subprocess
import time
from logger_config import setup_logger

logger = setup_logger(__name__)

cache = {}
cache_duration = 5  # 5 Sekunden

# Counts installed .DEBs
deb_count = popen("dpkg --list | wc --lines")
deb_counted = deb_count.read()
deb_count.close()
logger.info(f"{deb_counted[:-1]} .deb Packages Installed")


def load_installed_apt_pkgs():
    # List all packages from apt list --installed
    cache = apt.Cache()
    apt_installed_content = []

    for package in cache:
        if package.is_installed:
            apt_installed_content.append(package.name)
    
    logger.debug(apt_installed_content)
    return apt_installed_content

def get_installed_apt_pkgs():
    current_time = time.time()
    if 'result' in cache and (current_time - cache['timestamp']) < cache_duration:
        return cache['result']
    else:
        result = load_installed_apt_pkgs()
        cache['result'] = result
        cache['timestamp'] = current_time
        return result

# Nala Path
nala_path = os.path.exists("/bin/nala")


def get_apt_cache():
    # List all packages from apt-cache
    apt_cache_cmd = "apt-cache pkgnames"
    apt_cache_output = subprocess.check_output(apt_cache_cmd, shell=True)
    apt_cache_packages = apt_cache_output.decode().split("\n")

    apt_cache_content = apt_cache_packages
    for i, s in enumerate(apt_cache_content):
        apt_cache_content[i] = s.strip()

    # print(apt_repo_dict)
    return apt_cache_content
