import os
import subprocess
from logger_config import setup_logger

logger = setup_logger(__name__)


def is_snap_installed():
    return os.path.exists("/bin/snap")


def count_installed_snap_packages():
    try:
        output = subprocess.check_output(["snap", "list"]).decode("utf-8")
        packages = output.strip().split("\n")[1:]  # Skip the header line
        return len(packages)
    except subprocess.CalledProcessError:
        return -1


# Lazy init
snap_package_count = None


def get_snap_package_count():
    global snap_package_count
    if snap_package_count is None:
        if is_snap_installed():
            snap_package_count = count_installed_snap_packages()
            if snap_package_count != -1:
                logger.info(
                    f"Snap is installed, and there are {snap_package_count} packages installed."
                )
            else:
                logger.warning("Failed to list installed packages using Snap.")
                snap_package_count = "-"
        else:
            logger.info("Snap is not installed on your system.")
            snap_package_count = "-"
    return snap_package_count


import subprocess


def get_installed_snaps():
    snap_names = [""]

    # print(snap_names)
    return snap_names


get_installed_snaps()
