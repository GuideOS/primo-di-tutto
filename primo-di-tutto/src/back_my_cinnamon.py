import os
import tarfile
import subprocess
from tkinter import messagebox


def backup_cinnamon_settings():
    home = os.path.expanduser("~")
    config_source = os.path.join(home, ".config", "cinnamon")
    share_source = os.path.join(home, ".local", "share", "cinnamon")
    backup_dir = os.path.join(home, ".primo")
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, "my_cinnamon_settings.tar.gz")
    dconf_backup_file = os.path.join(backup_dir, "my_cinnamon_desktop_backup")

    with tarfile.open(backup_file, "w:gz") as tar:
        if os.path.exists(config_source):
            tar.add(config_source, arcname=".config/cinnamon")
        else:
            print(f"Directory {config_source} does not exist!")

        if os.path.exists(share_source):
            tar.add(share_source, arcname=".local/share/cinnamon")
        else:
            print(f"Directory {share_source} does not exist!")

    try:
        with open(dconf_backup_file, "w") as f:
            subprocess.run(["dconf", "dump", "/org/cinnamon/"], stdout=f, check=True)
        print(f"dconf backup saved to: {dconf_backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error saving dconf settings: {e}")

    print(f"Backup saved to: {backup_file}")

    messagebox.showinfo("Backup", "Backup erfolgreich erstellt!")
