import os
import tarfile
import subprocess
import shutil

def restore_cinnamon_settings():
    home = os.path.expanduser("~")
    backup_dir = os.path.join(home, ".primo")
    backup_file = os.path.join(backup_dir, "my_cinnamon_settings.tar.gz")
    dconf_backup_file = os.path.join(backup_dir, "my_cinnamon_desktop_backup")
    
    # Verzeichnisse, die wiederhergestellt werden
    config_dir = os.path.join(home, ".config", "cinnamon")
    share_dir = os.path.join(home, ".local", "share", "cinnamon")
    
    # Überprüfen, ob das Backup-Archiv existiert
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} not found!")
        return
    
    # Löschen der bestehenden Verzeichnisse, falls vorhanden
    if os.path.exists(config_dir):
        print(f"Deleting existing directory: {config_dir}")
        shutil.rmtree(config_dir)
    
    if os.path.exists(share_dir):
        print(f"Deleting existing directory: {share_dir}")
        shutil.rmtree(share_dir)
    
    # Neu anlegen der Verzeichnisse
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(share_dir, exist_ok=True)
    
    print(f"Restoring from {backup_file}")
    
    # Entpacken des Backups
    with tarfile.open(backup_file, "r:gz") as tar:
        # Extrahieren der Dateien in die entsprechenden Verzeichnisse
        tar.extractall(path=home)
        print(f"Backup restored to {home}")
    
    # Wiederherstellen der dconf-Einstellungen
    if os.path.exists(dconf_backup_file):
        try:
            with open(dconf_backup_file, "r") as f:
                subprocess.run(["dconf", "load", "/org/cinnamon/"], stdin=f, check=True)
            print(f"dconf settings restored from: {dconf_backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error restoring dconf settings: {e}")
    else:
        print(f"dconf backup file {dconf_backup_file} not found!")
    
    print("Restore process completed.")

if __name__ == "__main__":
    restore_cinnamon_settings()
