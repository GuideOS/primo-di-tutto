import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from resorcess import *
from apt_manage import *
import subprocess
from flatpak_alias_list import *
from tabs.pop_ups import *
from tabs.system_tab_check import *
import json
from tabs.system_tab_check import check_papirus
import shutil


class LookTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        if "dark" in theme_name or "Dark" in theme_name:
            self.folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/folder_s.png"
            )
            self.icon_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/start_here_s.png"
            )
            self.cursor_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/cursor_s.png"
            )
            self.theme_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/theme_s.png"
            )
            self.refresh_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/fresh_s.png"
            )
            self.classico_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/classico_thumb.png"
            )
            self.upside_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/upside_thumb.png"
            )
            self.elfi_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/elfi_thumb.png"
            )
            self.devil_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/devil_thumb.png"
            )
        else:
            self.folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/folder_s_light.png"
            )
            self.icon_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/start_here_s_light.png"
            )
            self.cursor_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/cursor_s_light.png"
            )
            self.theme_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/theme_s_light.png"
            )
            self.refresh_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/fresh_s_light.png"
            )
            self.classico_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/classico_thumb_light.png"
            )
            self.upside_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/upside_thumb_light.png"
            )
            self.elfi_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/elfi_thumb_light.png"
            )
            self.devil_thumb = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/devil_thumb_light.png"
            )

        def backup_grouped_config():
            # Verzeichnis mit der JSON-Datei
            config_dir = os.path.expanduser("~/.config/cinnamon/spices/grouped-window-list@cinnamon.org")
            
            # Prüfen, ob das Verzeichnis existiert
            if not os.path.exists(config_dir):
                print(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Datei mit dem Suchmuster finden
            try:
                json_file = next(
                    (f for f in os.listdir(config_dir) if f.endswith(".json")),
                    None
                )
            except Exception as e:
                print(f"Fehler beim Lesen des Verzeichnisses: {e}")
                return False

            if not json_file:
                print("Keine JSON-Datei gefunden.")
                return False
            
            # Pfad zur Originaldatei
            file_path = os.path.join(config_dir, json_file)
            # Backup-Dateipfad
            backup_file_path = os.path.join(config_dir, "69.bak")
            
            try:
                # Datei kopieren
                shutil.copy(file_path, backup_file_path)
                print(f"Backup erfolgreich erstellt: {backup_file_path}")
                return True
            except Exception as e:
                print(f"Fehler beim Erstellen des Backups: {e}")
                return False

        # Funktion aufrufen
        backup_grouped_config()
        def restore_cinnamon_config(file_number):
            # Verzeichnis mit der JSON-Datei
            config_dir = os.path.expanduser("~/.config/cinnamon/spices/grouped-window-list@cinnamon.org")
            
            # Prüfen, ob das Verzeichnis existiert
            if not os.path.exists(config_dir):
                print(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Pfad zur Backup-Datei
            backup_file_path = os.path.join(config_dir, "69.bak")
            
            # Prüfen, ob die Backup-Datei existiert
            if not os.path.exists(backup_file_path):
                print(f"Das Backup {backup_file_path} wurde nicht gefunden.")
                return False

            # Ziel-JSON-Dateiname basierend auf der Zahl
            restored_file_name = f"{file_number}.json"
            restored_file_path = os.path.join(config_dir, restored_file_name)
            
            try:
                # Backup zurückkopieren
                shutil.copy(backup_file_path, restored_file_path)
                print(f"Backup erfolgreich wiederhergestellt als: {restored_file_path}")
                return True
            except Exception as e:
                print(f"Fehler beim Wiederherstellen des Backups: {e}")
                return False



        def check_plank_autostart():
            # Pfad zur Datei
            path = os.path.expanduser("~/.config/autostart/plank.desktop")

            # Prüfen, ob die Datei existiert
            if os.path.exists(path):
                try:
                    # Datei löschen
                    os.remove(path)
                    print(f"Die Datei {path} wurde gelöscht.")
                except Exception as e:
                    print(f"Fehler beim Löschen der Datei: {e}")
            else:
                print(f"Die Datei {path} existiert nicht.")

        def copy_dockitems():
            # Definiere Quell- und Zielverzeichnisse
            src = f"{application_path}/scripts/"
            dest = os.path.expanduser("~/.config/plank/dock1/launchers")

            # Prüfe, ob das Quellverzeichnis existiert
            if not os.path.exists(src):
                print(f"Quellverzeichnis {src} existiert nicht.")
                return

            # Erstelle das Zielverzeichnis, falls es nicht existiert
            if not os.path.exists(dest):
                os.makedirs(dest)
                print(f"Zielverzeichnis {dest} wurde erstellt.")

            # Kopiere alle .dockitem-Dateien
            for file_name in os.listdir(src):
                if file_name.endswith(".dockitem"):
                    src_file = os.path.join(src, file_name)
                    dest_file = os.path.join(dest, file_name)
                    try:
                        shutil.copy2(src_file, dest_file)
                        print(f"{src_file} wurde nach {dest_file} kopiert.")
                    except Exception as e:
                        print(f"Fehler beim Kopieren von {src_file}: {e}")

        # Funktion ausführen

        def plank_values():
            """Schreibt vorgegebene Werte in dconf."""
            dconf_data = {
                "/net/launchpad/plank/docks/dock1/alignment": "'fill'",
                "/net/launchpad/plank/docks/dock1/dock-items": "['gos-menu.dockitem', 'nemo.dockitem','firefox.dockitem']",
                "/net/launchpad/plank/docks/dock1/hide-mode": "'none'",
                "/net/launchpad/plank/docks/dock1/offset": "100",
                "/net/launchpad/plank/docks/dock1/position": "'left'",
                "/net/launchpad/plank/docks/dock1/theme": "'Transparent'",
            }

            for path, value in dconf_data.items():
                try:
                    subprocess.run(["dconf", "write", path, value], check=True)
                    print(f"Erfolgreich geschrieben: {path} -> {value}")
                except subprocess.CalledProcessError as e:
                    print(f"Fehler beim Schreiben: {path} -> {value}")
                    print(e)

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/plank.desktop"
            destination_path = os.path.expanduser("~/.config/autostart/plank.desktop")

            # Funktion aufrufen
            copy_file(source_path, destination_path)

        def copy_file(source, destination):
            try:
                # Sicherstellen, dass das Zielverzeichnis existiert
                destination_dir = os.path.dirname(destination)
                os.makedirs(destination_dir, exist_ok=True)

                # Datei kopieren
                shutil.copy2(source, destination)
                print(f"Datei erfolgreich kopiert: {source} -> {destination}")
            except Exception as e:
                print(f"Fehler beim Kopieren der Datei: {e}")

        def copy_guide_menu(application_path):
            """
            Kopiert die Datei guide_menu.json in das Cinnamon Menü Verzeichnis.

            Args:
                application_path (str): Der Pfad zum Hauptverzeichnis der Anwendung.
            """
            source_file = f"{application_path}/scripts/guide_menu.json"
            destination_directory = os.path.expanduser(
                "~/.config/cinnamon/spices/menu@cinnamon.org"
            )
            destination_file = os.path.join(destination_directory, "0.json")

            # Erstelle das Zielverzeichnis, falls es nicht existiert
            os.makedirs(destination_directory, exist_ok=True)

            # Kopiere die Datei
            try:
                # Datei auslesen
                with open(source_file, "r") as src:
                    content = src.read()

                # Datei im Zielverzeichnis erstellen und Inhalt schreiben
                with open(destination_file, "w") as dst:
                    dst.write(content)

                print(f"Datei erfolgreich nach {destination_file} kopiert.")
            except Exception as e:
                print(f"Fehler beim Kopieren der Datei: {e}")

        def copy_guide_menu_up(application_path):
            """
            Kopiert die Datei guide_menu.json in das Cinnamon Menü Verzeichnis.

            Args:
                application_path (str): Der Pfad zum Hauptverzeichnis der Anwendung.
            """
            source_file = f"{application_path}/scripts/guide_menu_up.json"
            destination_directory = os.path.expanduser(
                "~/.config/cinnamon/spices/menu@cinnamon.org"
            )
            destination_file = os.path.join(destination_directory, "0.json")

            # Erstelle das Zielverzeichnis, falls es nicht existiert
            os.makedirs(destination_directory, exist_ok=True)

            # Kopiere die Datei
            try:
                # Datei auslesen
                with open(source_file, "r") as src:
                    content = src.read()

                # Datei im Zielverzeichnis erstellen und Inhalt schreiben
                with open(destination_file, "w") as dst:
                    dst.write(content)

                print(f"Datei erfolgreich nach {destination_file} kopiert.")
            except Exception as e:
                print(f"Fehler beim Kopieren der Datei: {e}")

        def set_elfi_panel():
            popen("killall plank")
            check_plank_autostart()
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            copy_guide_menu(application_path)
            gsettings_11_config = {
                "app-menu-icon-name": "ubuntucinnamon-symbolic",
                "app-menu-label": "Menu",
                "date-format": "'%a, %h %d %Y%l:%M %p'",
                "desktop-layout": "",
                "enabled-applets": [
                    "panel1:center:0:menu@cinnamon.org:0",
                    "panel1:center:2:grouped-window-list@cinnamon.org:69",
                    "panel1:right:1:systray@cinnamon.org:3",
                    "panel1:right:2:xapp-status@cinnamon.org:4",
                    "panel1:right:3:notifications@cinnamon.org:5",
                    "panel1:right:4:printers@cinnamon.org:6",
                    "panel1:right:5:removable-drives@cinnamon.org:7",
                    "panel1:right:6:keyboard@cinnamon.org:8",
                    "panel1:right:7:favorites@cinnamon.org:9",
                    "panel1:right:8:network@cinnamon.org:10",
                    "panel1:right:12:sound@cinnamon.org:11",
                    "panel1:right:9:power@cinnamon.org:12",
                    "panel1:right:13:calendar@cinnamon.org:13",
                    "panel1:right:11:trash@cinnamon.org:15",
                    "panel1:left:0:weather@mockturtl:19",
                    "panel1:right:0:expo@cinnamon.org:22",
                ],
                "enabled-desklets": [],
                "enabled-extensions": [
                    "opacify@anish.org",
                    "transparent-panels@germanfr",
                ],
                "favorite-apps": [
                    "cinnamon-settings.desktop",
                    "nemo.desktop",
                    "org.gnome.Software.desktop",
                    "system-config-printer.desktop",
                    "org.gnome.DejaDup.desktop",
                ],
                "panel-zone-icon-sizes": '[{"panelId":1,"left":0,"center":0,"right":22}]',
                "panel-zone-symbolic-icon-sizes": '[{"panelId":1,"left":22,"center":28,"right":18}]',
                "panel-zone-text-sizes": '[{"panelId":1,"left":0,"center":0,"right":0}]',
                "panels-autohide": ["1:false"],
                "panels-enabled": ["1:0:bottom"],
                "panels-height": ["1:38", "2:21"],
                "panels-hide-delay": ["1:0", "2:0"],
                "panels-show-delay": ["1:0", "2:0"],
            }

            # Schleife durch jedes Schlüssel-Wert-Paar im Dictionary
            for key, value in gsettings_11_config.items():
                # Wenn der Wert eine Liste oder ein Dictionary ist, in eine Zeichenkette umwandeln
                if isinstance(value, (list, dict)):
                    value = str(value).replace(
                        "'", '"'
                    )  # Ersetze einfache Anführungszeichen mit doppelten
                # Führe den gsettings-Befehl aus
                subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
            destination_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/13.json"
            )

            # Funktion aufrufen
            copy_file(source_path, destination_path)
            restore_cinnamon_config(69)

        def set_classico_panel():
            popen("killall plank")
            check_plank_autostart()
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            copy_guide_menu(application_path)
            config_path = os.path.expanduser(
                "~/.config/cinnamon/spices/transparent-panels@germanfr/transparent-panels@germanfr.json"
            )

            with open(config_path, "r") as file:
                config = json.load(file)

            config["transparency-type"]["value"] = "panel-semi-transparent"
            config["transparency-type"]["value"] = "panel-semi-transparent"
            config["panel-top"]["value"] = True
            config["panel-bottom"]["value"] = False
            config["panel-left"]["value"] = False
            config["panel-right"]["value"] = False

            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)

            with open(config_path, "r") as file:
                config = json.load(file)

            # Opacity
            opacify_config_path = os.path.expanduser(
                "~/.config/cinnamon/spices/opacify@anish.org/opacify@anish.org.json"
            )

            with open(opacify_config_path, "r") as opacify_file:
                opacify_config = json.load(opacify_file)

            opacify_config["opacity"]["value"] = "240"

            with open(opacify_config_path, "w") as opacify_file:
                json.dump(opacify_config, opacify_file, indent=4)

            # Dictionary mit den GSettings-Konfigurationen
            gsettings_config = {
                "app-menu-icon-name": "ubuntucinnamon-symbolic",
                "app-menu-label": "'Menu'",
                "date-format": "'%a, %h %d %Y%l:%M %p'",
                "enabled-applets": [
                    "panel1:left:0:menu@cinnamon.org:0",
                    "panel1:left:2:grouped-window-list@cinnamon.org:69",
                    "panel1:right:2:systray@cinnamon.org:3",
                    "panel1:right:3:xapp-status@cinnamon.org:4",
                    "panel1:right:4:notifications@cinnamon.org:5",
                    "panel1:right:5:printers@cinnamon.org:6",
                    "panel1:right:6:removable-drives@cinnamon.org:7",
                    "panel1:right:7:keyboard@cinnamon.org:8",
                    "panel1:right:8:favorites@cinnamon.org:9",
                    "panel1:right:9:network@cinnamon.org:10",
                    "panel1:right:10:sound@cinnamon.org:11",
                    "panel1:right:11:power@cinnamon.org:12",
                    "panel2:center:0:calendar@cinnamon.org:13",
                    "panel1:right:1:trash@cinnamon.org:15",
                    "panel2:right:1:temperature@fevimu:16",
                    "panel1:left:1:placesCenter@scollins:17",
                    "panel1:right:13:sessionManager@scollins:18",
                    "panel2:center:1:weather@mockturtl:19",
                    "panel1:right:0:expo@cinnamon.org:22",
                ],
                "enabled-extensions": "['opacify@anish.org', 'transparent-panels@germanfr']",
                "panel-zone-icon-sizes": '\'[{"panelId": 1, "left": 0, "center": 0, "right": 22}, {"left": 0, "center": 0, "right": 0, "panelId": 2}]\'',
                "panel-zone-symbolic-icon-sizes": '\'[{"panelId": 1, "left": 22, "center": 28, "right": 18}, {"left": 28, "center": 17, "right": 28, "panelId": 2}]\'',
                "panel-zone-text-sizes": '\'[{"panelId":1,"left":0,"center":0,"right":0},{"left":0,"center":0,"right":0,"panelId":2}]\'',
                "panels-autohide": "['1:false', '2:intel']",
                "panels-enabled": "['1:0:bottom', '2:0:top']",
                "panels-height": "['1:38', '2:21']",
                "panels-hide-delay": "['1:0', '2:0']",
                "panels-show-delay": "['1:0', '2:0']",
            }

            # Schleife durch jedes Schlüssel-Wert-Paar im Dictionary
            for key, value in gsettings_config.items():
                # Wenn der Wert eine Liste oder ein Dictionary ist, in eine Zeichenkette umwandeln
                if isinstance(value, (list, dict)):
                    value = str(value).replace(
                        "'", '"'
                    )  # Ersetze einfache Anführungszeichen mit doppelten
                # Führe den gsettings-Befehl aus
                subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
            destination_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/13.json"
            )

            # Funktion aufrufen
            copy_file(source_path, destination_path)
            restore_cinnamon_config(69)

        def set_der_teufel_panel():
            popen("plank")
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            gsettings_config = {
                "app-menu-icon-name": "ubuntucinnamon-symbolic",
                "app-menu-label": "Menu",
                "date-format": "%a, %h %d %Y %l:%M %p",
                "enabled-applets": [
                    "panel1:right:2:systray@cinnamon.org:3",
                    "panel1:right:3:xapp-status@cinnamon.org:4",
                    "panel1:right:4:notifications@cinnamon.org:5",
                    "panel1:right:5:printers@cinnamon.org:6",
                    "panel1:right:6:removable-drives@cinnamon.org:7",
                    "panel1:right:7:keyboard@cinnamon.org:8",
                    "panel1:right:8:favorites@cinnamon.org:9",
                    "panel1:right:9:network@cinnamon.org:10",
                    "panel1:right:15:sound@cinnamon.org:11",
                    "panel1:right:10:power@cinnamon.org:12",
                    "panel1:right:14:trash@cinnamon.org:15",
                    "panel2:right:1:temperature@fevimu:16",
                    "panel1:left:1:placesCenter@scollins:17",
                    "panel1:right:16:sessionManager@scollins:18",
                    "panel1:center:1:weather@mockturtl:19",
                    "panel1:center:0:calendar@cinnamon.org:20",
                    "panel1:right:0:expo@cinnamon.org:22",
                ],
                "enabled-desklets": [],
                "enabled-extensions": [],
                "enabled-search-providers": [],
                "extension-cache-updated": 0,
                "favorite-apps": [
                    "cinnamon-settings.desktop",
                    "nemo.desktop",
                    "org.gnome.Software.desktop",
                    "system-config-printer.desktop",
                    "org.gnome.DejaDup.desktop",
                ],
                "panel-zone-icon-sizes": '[{"panelId":1,"left":0,"center":0,"right":22}]',
                "panel-zone-symbolic-icon-sizes": '[{"panelId":1,"left":22,"center":28,"right":18}]',
                "panel-zone-text-sizes": '[{"panelId":1,"left":0,"center":0,"right":0}]',
                "panels-autohide": ["1:false", "2:intel"],
                "panels-enabled": ["1:0:top"],
                "panels-height": ["1:38", "2:21"],
                "panels-hide-delay": ["1:0", "2:0"],
                "panels-show-delay": ["1:0", "2:0"],
            }

            # Schleife durch jedes Schlüssel-Wert-Paar im Dictionary
            for key, value in gsettings_config.items():
                # Wenn der Wert eine Liste oder ein Dictionary ist, in eine Zeichenkette umwandeln
                if isinstance(value, (list, dict)):
                    value = str(value).replace(
                        "'", '"'
                    )  # Ersetze einfache Anführungszeichen mit doppelten
                # Führe den gsettings-Befehl aus
                subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
            destination_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/20.json"
            )
            # Funktion aufrufen
            copy_file(source_path, destination_path)

            plank_values()
            copy_dockitems()

        def set_upside_down_panel():
            check_plank_autostart()
            popen("killall plank")
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            gsettings_config = {
                "app-menu-icon-name": "ubuntucinnamon-symbolic",
                "app-menu-label": "Menu",
                "date-format": "%a, %h %d %Y %l:%M %p",
                "enabled-applets": [
                    "panel1:left:0:menu@cinnamon.org:0",
                    "panel1:left:2:grouped-window-list@cinnamon.org:69",
                    "panel1:right:2:systray@cinnamon.org:3",
                    "panel1:right:3:xapp-status@cinnamon.org:4",
                    "panel1:right:4:notifications@cinnamon.org:5",
                    "panel1:right:5:printers@cinnamon.org:6",
                    "panel1:right:6:removable-drives@cinnamon.org:7",
                    "panel1:right:7:keyboard@cinnamon.org:8",
                    "panel1:right:8:favorites@cinnamon.org:9",
                    "panel1:right:9:network@cinnamon.org:10",
                    "panel1:right:15:sound@cinnamon.org:11",
                    "panel1:right:10:power@cinnamon.org:12",
                    "panel1:right:14:trash@cinnamon.org:15",
                    "panel2:right:1:temperature@fevimu:16",
                    "panel1:left:1:placesCenter@scollins:17",
                    "panel1:right:16:sessionManager@scollins:18",
                    "panel1:right:12:weather@mockturtl:19",
                    "panel1:right:13:calendar@cinnamon.org:20",
                    "panel1:right:0:expo@cinnamon.org:22",
                ],
                "enabled-desklets": [],
                "enabled-extensions": [],
                "enabled-search-providers": [],
                "extension-cache-updated": 0,
                "favorite-apps": [
                    "cinnamon-settings.desktop",
                    "nemo.desktop",
                    "org.gnome.Software.desktop",
                    "system-config-printer.desktop",
                    "org.gnome.DejaDup.desktop",
                ],
                "panel-zone-icon-sizes": '[{"panelId":1,"left":0,"center":0,"right":22}]',
                "panel-zone-symbolic-icon-sizes": '[{"panelId":1,"left":22,"center":28,"right":18}]',
                "panel-zone-text-sizes": '[{"panelId":1,"left":0,"center":0,"right":0}]',
                "panels-autohide": ["1:false", "2:intel"],
                "panels-enabled": ["1:0:top"],
                "panels-height": ["1:38", "2:21"],
                "panels-hide-delay": ["1:0", "2:0"],
                "panels-show-delay": ["1:0", "2:0"],
            }

            # Schleife durch jedes Schlüssel-Wert-Paar im Dictionary
            for key, value in gsettings_config.items():
                # Wenn der Wert eine Liste oder ein Dictionary ist, in eine Zeichenkette umwandeln
                if isinstance(value, (list, dict)):
                    value = str(value).replace(
                        "'", '"'
                    )  # Ersetze einfache Anführungszeichen mit doppelten
                # Führe den gsettings-Befehl aus
                subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
            destination_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/13.json"
            )

            # Funktion aufrufen
            copy_file(source_path, destination_path)
            restore_cinnamon_config(69)

        self.desktop_layout_set = ttk.LabelFrame(self, text="Layout", padding=10)
        self.desktop_layout_set.pack(pady=20, padx=40, fill="x", anchor="n")
        self.desktop_layout_set.grid_columnconfigure(0, weight=1)
        self.desktop_layout_set.grid_columnconfigure(1, weight=1)
        self.desktop_layout_set.grid_columnconfigure(2, weight=1)
        self.desktop_layout_set.grid_columnconfigure(3, weight=1)

        classico_button = ttk.Button(
            self.desktop_layout_set,
            # text="Classico\n(Standard)",
            compound="center",
            image=self.classico_thumb,
            command=set_classico_panel,
        )
        classico_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        classico_label = ttk.Label(
            self.desktop_layout_set, text="Standard", anchor="center"
        )
        classico_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        upside_button = ttk.Button(
            self.desktop_layout_set,
            # text="upside down",
            compound="center",
            image=self.upside_thumb,
            command=set_upside_down_panel,
        )
        upside_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        upside_label = ttk.Label(
            self.desktop_layout_set, text="Spiegel", anchor="center"
        )
        upside_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        elfi_button = ttk.Button(
            self.desktop_layout_set,
            # text="elfi",
            compound="center",
            image=self.elfi_thumb,
            command=set_elfi_panel,
        )
        elfi_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        elfi_label = ttk.Label(self.desktop_layout_set, text="11", anchor="center")
        elfi_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        devil_button = ttk.Button(
            self.desktop_layout_set,
            # text=" the devil",
            compound="center",
            image=self.devil_thumb,
            command=set_der_teufel_panel,
        )
        devil_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        devil_label = ttk.Label(
            self.desktop_layout_set, text="Ubuntu-Like", anchor="center"
        )
        devil_label.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        self.pixel_set = ttk.LabelFrame(self, text="Farben und Formen", padding=10)
        self.pixel_set.pack(pady=20, padx=40, fill="x", anchor="n")
        self.pixel_set.columnconfigure(0, weight=1)
        self.pixel_set.rowconfigure(0, weight=1)

        def done_message_0():
            d_mass = Done_(self)
            d_mass.grab_set()

        def why_message_0():
            y_mass = Look_Disabled(self)
            y_mass.grab_set()

        def update_theme_combobox():
            try:
                themes = [
                    d
                    for d in os.listdir("/usr/share/themes")
                    if os.path.isdir(os.path.join("/usr/share/themes", d))
                ]
                themes.sort()
                theme_combobox["values"] = themes
                theme_combobox.set("Select Theme")
            except Exception as e:
                theme_combobox.set("Error: " + str(e))

            try:
                icons = [
                    d
                    for d in os.listdir("/usr/share/icons")
                    if os.path.isdir(os.path.join("/usr/share/icons", d))
                    and "cursors" not in os.listdir(os.path.join("/usr/share/icons", d))
                ]
                icons.sort()
                icon_combobox["values"] = icons
                icon_combobox.set("Select Icons")
            except Exception as e:
                icon_combobox.set("Error: " + str(e))

            try:
                icons = [
                    d
                    for d in os.listdir("/usr/share/icons")
                    if os.path.isdir(os.path.join("/usr/share/icons", d))
                ]

                # Separate cursor themes from regular icon themes
                icons.sort()
                cursor_themes = [
                    icon
                    for icon in icons
                    if "cursors" in os.listdir(os.path.join("/usr/share/icons", icon))
                ]

                cursor_combobox["values"] = cursor_themes
                cursor_combobox.set("Select Cursor")
            except Exception as e:
                cursor_combobox.set("Error: " + str(e))

        def update_lxde_theme_config(selected_theme):
            config_file_path = os.path.expanduser(
                "~/.config/lxsession/LXDE-pi/desktop.conf"
            )

            with open(config_file_path, "r") as file:
                lines = file.readlines()

            found = False
            for i, line in enumerate(lines):
                if "sNet/ThemeName=" in line:
                    lines[i] = f"sNet/ThemeName={selected_theme}\n"
                    found = True
                    break

            if not found:
                lines.append(f"sNet/ThemeName={selected_theme}\n")

            with open(config_file_path, "w") as file:
                file.writelines(lines)

        def update_lxde_icons_config(selected_icon):
            config_file_path = os.path.expanduser(
                "~/.config/lxsession/LXDE-pi/desktop.conf"
            )

            with open(config_file_path, "r") as file:
                lines = file.readlines()

            found = False
            for i, line in enumerate(lines):
                if "sNet/IconThemeName" in line:
                    lines[i] = f"sNet/IconThemeName={selected_icon}\n"
                    found = True
                    break

            if not found:
                lines.append(f"sNet/IconThemeName={selected_icon}\n")

            with open(config_file_path, "w") as file:
                file.writelines(lines)

        def update_lxde_cursor_config(selected_cursor):
            config_file_path = os.path.expanduser(
                "~/.config/lxsession/LXDE-pi/desktop.conf"
            )

            with open(config_file_path, "r") as file:
                lines = file.readlines()

            found = False
            for i, line in enumerate(lines):
                if "sGtk/CursorThemeName" in line:
                    lines[i] = f"sGtk/CursorThemeName={selected_cursor}\n"
                    found = True
                    break

            if not found:
                lines.append(f"sGtk/CursorThemeName={selected_cursor}\n")

            with open(config_file_path, "w") as file:
                file.writelines(lines)

        def set_theme():
            selected_theme = theme_combobox.get()

            if selected_theme != "Press Refresh":
                # Liste der GSettings-Schlüssel und deren Pfade
                settings_keys = [
                    ("org.gnome.desktop.interface", "gtk-theme"),
                    ("org.cinnamon.desktop.wm.preferences", "theme"),
                    ("org.gnome.desktop.wm.preferences", "theme"),
                    ("org.cinnamon.desktop.interface", "gtk-theme"),
                    ("org.cinnamon.theme", "name"),
                ]

                # Funktion zum Setzen eines GSettings-Werts
                def set_gsettings_value(schema, key, value):
                    subprocess.run(["gsettings", "set", schema, key, value], check=True)

                # Für jeden Schlüssel den Wert setzen
                for schema, key in settings_keys:
                    set_gsettings_value(schema, key, selected_theme)
                    print(f"{schema}.{key} wurde auf {selected_theme} gesetzt.")
                done_message_0()

        def set_icon():
            selected_icon = icon_combobox.get()

            if selected_icon != "Press Refresh":
                subprocess.run(
                    [
                        "gsettings",
                        "set",
                        "org.cinnamon.desktop.interface",
                        "icon-theme",
                        selected_icon,
                    ]
                )
            done_message_0()

        def set_cursor():
            selected_cursor = cursor_combobox.get()

            if selected_cursor != "Press Refresh":
                subprocess.run(
                    [
                        "gsettings",
                        "set",
                        "org.cinnamon.desktop.interface",
                        "cursor-theme",
                        selected_cursor,
                    ]
                )
            done_message_0()

        def open_theme_folder():
            popen("pkexec nemo /usr/share/themes")

        def open_icon_folder():
            popen("pkexec nemo /usr/share/icons")

        theme_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        theme_combobox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        theme_combobox.set("Press Refresh")

        icon_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        icon_combobox.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        icon_combobox.set("Press Refresh")

        cursor_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        cursor_combobox.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        cursor_combobox.set("Press Refresh")

        theme_button = ttk.Button(
            self.pixel_set,
            text="Set Theme",
            compound="left",
            image=self.theme_folder_icon,
            command=set_theme,
            width=20,
        )
        theme_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        icon_button = ttk.Button(
            self.pixel_set,
            text="Set Icon",
            compound="left",
            image=self.icon_folder_icon,
            command=set_icon,
            width=20,
        )
        icon_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        cursor_button = ttk.Button(
            self.pixel_set,
            text="Set Cursor",
            compound="left",
            image=self.cursor_folder_icon,
            command=set_cursor,
            width=20,
        )
        cursor_button.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        theme_refresh_button = ttk.Button(
            self.pixel_set,
            text="Refresh",
            compound="left",
            image=self.refresh_icon,
            command=update_theme_combobox,
            width=20,
            style="Custom.TButton",
        )
        theme_refresh_button.grid(
            row=4, column=0, columnspan=5, padx=10, pady=5, sticky="ew"
        )

        theme_folder_button = ttk.Button(
            self.pixel_set,
            text="Theme Folder",
            image=self.folder_icon,
            compound="left",
            command=open_theme_folder,
            width=20,
        )
        theme_folder_button.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        icon_folder_button = ttk.Button(
            self.pixel_set,
            text="Icon Folder",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20,
        )
        icon_folder_button.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        cursor_folder_button = ttk.Button(
            self.pixel_set,
            text="Cursor Folder",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20,
        )
        cursor_folder_button.grid(row=3, column=4, padx=10, pady=5, sticky="ew")
