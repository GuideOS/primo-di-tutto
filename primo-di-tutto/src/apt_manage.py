import apt
import os
from os import popen
import subprocess
from logger_config import setup_logger

logger = setup_logger(__name__)

# Counts installed .DEBs
deb_count = popen("dpkg --list | wc --lines")
deb_counted = deb_count.read()
deb_count.close()
logger.info(f"{deb_counted[:-1]} .deb Packages Installed")


def get_installed_apt_pkgs():
    # List all packages from apt list --installed
    cache = apt.Cache()
    apt_installed_content = []

    for package in cache:
        if package.is_installed:
            apt_installed_content.append(package.name)
    
    logger.debug(apt_installed_content)
    return apt_installed_content


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
