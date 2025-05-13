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
from logger_config import setup_logger
from back_my_cinnamon import *
from restore_my_cinnamon import *

logger = setup_logger(__name__)


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
            self.cursor_size_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/cursorsize_s.png"
            )
            self.theme_folder_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/theme_s.png"
            )
            self.refresh_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/fresh_s.png"
            )
            self.save_layout_icon = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/document-save-light_24x24.png"
            )
            self.load_layout_icon = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/draw-star_light_24x24.png"
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
            self.cursor_size_icon = PhotoImage(
                file=f"{application_path}/images/icons/pigro_icons/cursorsize_s_light.png"
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
            self.save_layout_icon = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/document-save.png"
            )
            self.load_layout_icon = PhotoImage(
                file=f"{application_path}/images/icons/nav_bar/draw-star_dark_24x24.png"
            )

        def backup_grouped_config():
            # Verzeichnis mit der JSON-Datei
            config_dir = os.path.expanduser(
                "~/.config/cinnamon/spices/grouped-window-list@cinnamon.org"
            )

            # Prüfen, ob das Verzeichnis existiert
            if not os.path.exists(config_dir):
                logger.error(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Datei mit dem Suchmuster finden
            try:
                json_file = next(
                    (f for f in os.listdir(config_dir) if f.endswith(".json")), None
                )
            except Exception as e:
                logger.error(f"Fehler beim Lesen des Verzeichnisses: {e}")
                return False

            if not json_file:
                logger.error("Keine JSON-Datei gefunden.")
                return False

            # Pfad zur Originaldatei
            file_path = os.path.join(config_dir, json_file)
            # Backup-Dateipfad
            backup_file_path = os.path.join(config_dir, "69.bak")

            try:
                # Datei kopieren
                shutil.copy(file_path, backup_file_path)
                logger.info(f"Backup erfolgreich erstellt: {backup_file_path}")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Erstellen des Backups: {e}")
                return False

        # Funktion aufrufen
        backup_grouped_config()

        def restore_cinnamon_config(file_number, c_dir):
            # Verzeichnis mit der JSON-Datei
            config_dir = os.path.expanduser(c_dir)

            # Prüfen, ob das Verzeichnis existiert
            if not os.path.exists(config_dir):
                logger.error(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Pfad zur Backup-Datei
            backup_file_path = os.path.join(config_dir, "69.bak")

            # Prüfen, ob die Backup-Datei existiert
            if not os.path.exists(backup_file_path):
                logger.error(f"Das Backup {backup_file_path} wurde nicht gefunden.")
                return False

            # Ziel-JSON-Dateiname basierend auf der Zahl
            restored_file_name = f"{file_number}.json"
            restored_file_path = os.path.join(config_dir, restored_file_name)

            try:
                # Backup zurückkopieren
                shutil.copy(backup_file_path, restored_file_path)
                logger.info(
                    f"Backup erfolgreich wiederhergestellt als: {restored_file_path}"
                )
                return True
            except Exception as e:
                logger.error(f"Fehler beim Wiederherstellen des Backups: {e}")
                return False

        def check_plank_autostart():
            # Pfad zur Datei
            path = os.path.expanduser("~/.config/autostart/plank.desktop")

            # Prüfen, ob die Datei existiert
            if os.path.exists(path):
                try:
                    # Datei löschen
                    os.remove(path)
                    logger.info(f"Die Datei {path} wurde gelöscht.")
                except Exception as e:
                    logger.error(f"Fehler beim Löschen der Datei: {e}")
            else:
                logger.warning(f"Die Datei {path} existiert nicht.")

        def copy_dockitems():
            # Definiere Quell- und Zielverzeichnisse
            src = f"{application_path}/scripts/"
            dest = os.path.expanduser("~/.config/plank/dock1/launchers")

            # Prüfe, ob das Quellverzeichnis existiert
            if not os.path.exists(src):
                logger.warning(f"Quellverzeichnis {src} existiert nicht.")
                return

            # Erstelle das Zielverzeichnis, falls es nicht existiert
            if not os.path.exists(dest):
                os.makedirs(dest)
                logger.info(f"Zielverzeichnis {dest} wurde erstellt.")

            # Kopiere alle .dockitem-Dateien
            for file_name in os.listdir(src):
                if file_name.endswith(".dockitem"):
                    src_file = os.path.join(src, file_name)
                    dest_file = os.path.join(dest, file_name)
                    try:
                        shutil.copy2(src_file, dest_file)
                        logger.info(f"{src_file} wurde nach {dest_file} kopiert.")
                    except Exception as e:
                        logger.error(f"Fehler beim Kopieren von {src_file}: {e}")

        # Funktion ausführen

        def plank_values():
            """Schreibt vorgegebene Werte in dconf."""
            dconf_data = {
                "/net/launchpad/plank/docks/dock1/alignment": "'fill'",
                "/net/launchpad/plank/docks/dock1/dock-items": "['gos-menu.dockitem', 'nemo.dockitem', 'org.gnome.Software.dockitem', 'firefox.dockitem', 'thunderbird-1.dockitem', 'libreoffice-writer.dockitem']",
                "/net/launchpad/plank/docks/dock1/hide-mode": "'none'",
                "/net/launchpad/plank/docks/dock1/offset": "100",
                "/net/launchpad/plank/docks/dock1/position": "'left'",
                "/net/launchpad/plank/docks/dock1/theme": "'Transparent'",
            }

            for path, value in dconf_data.items():
                try:
                    subprocess.run(["dconf", "write", path, value], check=True)
                    logger.info(f"Erfolgreich geschrieben: {path} -> {value}")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Fehler beim Schreiben: {path} -> {value}")
                    logger.error(e)

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
                logger.info(f"Datei erfolgreich kopiert: {source} -> {destination}")
            except Exception as e:
                logger.error(f"Fehler beim Kopieren der Datei: {e}")

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

                logger.info(f"Datei erfolgreich nach {destination_file} kopiert.")
            except Exception as e:
                logger.error(f"Fehler beim Kopieren der Datei: {e}")

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

                logger.info(f"Datei erfolgreich nach {destination_file} kopiert.")
            except Exception as e:
                logger.error(f"Fehler beim Kopieren der Datei: {e}")

        # Beispielaufruf der Funktion
        def create_cinnamenu_conf():
            """
            Kopiert die Datei 68.json vom application_path/scripts-Pfad
            zum Zielpfad des Nutzers ~/.config/cinnamon/spices/Cinnamenu@json/68.json

            :param application_path: Der Pfad zur Anwendung.
            :param user: Der Benutzername oder der Benutzerpfad.
            """
            source_path = os.path.join(application_path, "scripts", "68.json")
            target_dir = os.path.expanduser("~/.config/cinnamon/spices/Cinnamenu@json")
            target_path = os.path.join(target_dir, "68.json")

            # Sicherstellen, dass das Zielverzeichnis existiert
            os.makedirs(target_dir, exist_ok=True)

            try:
                # Datei kopieren
                shutil.copy(source_path, target_path)
                logger.info(f"Datei wurde erfolgreich nach {target_path} kopiert.")
            except FileNotFoundError:
                logger.error(f"Die Datei {source_path} wurde nicht gefunden.")
            except PermissionError:
                logger.error(f"Zugriffsrechte fehlen, um die Datei zu kopieren.")
            except Exception as e:
                logger.error(f"Ein Fehler ist aufgetreten: {e}")

        def set_elfi_panel():
            popen("killall plank")
            check_plank_autostart()

            copy_guide_menu(application_path)

            # subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])
            subprocess.run(
                f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_elf",
                shell=True,
                check=True,
            )

            # Quell- und Zielpfade
            calendar_bak = f"{application_path}/scripts/calendar@cinnamon.org.json"
            calendar_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/13.json"
            )

            # create_cinnamenu_conf()
            # Funktion aufrufen
            copy_file(calendar_bak, calendar_path)

            grouped_win = "~/.config/cinnamon/spices/grouped-window-list@cinnamon.org"

            restore_cinnamon_config(69, grouped_win)
            create_cinnamenu_conf()

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

            subprocess.run(
                f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_classico",
                shell=True,
                check=True,
            )

            calendar_bak = f"{application_path}/scripts/calendar@cinnamon.org.json"
            calendar_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/66.json"
            )

            # create_cinnamenu_conf()
            # Funktion aufrufen
            copy_file(calendar_bak, calendar_path)

            grouped_win = "~/.config/cinnamon/spices/grouped-window-list@cinnamon.org"
            restore_cinnamon_config(69, grouped_win)

            workspace_bak = f"{application_path}/scripts/67.json"
            workspace_path = os.path.expanduser(
                "~/.config/cinnamon/spices/workspace-switcher@cinnamon.org/67.json"
            )
            copy_file(workspace_bak, workspace_path)

            menu_bak = f"{application_path}/scripts/0.json"
            menu_path = os.path.expanduser(
                "~/.config/cinnamon/spices/menu@cinnamon.org/0.json"
            )
            copy_file(menu_bak, menu_path)

        def set_der_teufel_panel():
            popen("plank")
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            subprocess.run(
                f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_ubuntu",
                shell=True,
                check=True,
            )
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
            subprocess.run(
                f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_spiegel",
                shell=True,
                check=True,
            )

            # Quell- und Zielpfade
            source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
            destination_path = os.path.expanduser(
                "~/.config/cinnamon/spices/calendar@cinnamon.org/13.json"
            )

            # Funktion aufrufen
            copy_file(source_path, destination_path)
            grouped_win = "~/.config/cinnamon/spices/grouped-window-list@cinnamon.org"
            restore_cinnamon_config(69, grouped_win)

            menu_bak = f"{application_path}/scripts/0.json"
            menu_path = os.path.expanduser(
                "~/.config/cinnamon/spices/menu@cinnamon.org/0.json"
            )
            copy_file(menu_bak, menu_path)

        self.desktop_layout_set = ttk.LabelFrame(
            self, text="Layout-Vorlagen", padding=10
        )
        self.desktop_layout_set.pack(pady=20, padx=40, fill="x", anchor="n")
        self.desktop_layout_set.grid_columnconfigure(0, weight=1)
        self.desktop_layout_set.grid_columnconfigure(1, weight=1)
        self.desktop_layout_set.grid_columnconfigure(2, weight=1)
        self.desktop_layout_set.grid_columnconfigure(3, weight=1)

        layout_label = ttk.Label(
            self.desktop_layout_set,
            text="Wähle ein Layout aus und passe es an. Du kannst ein Backup davon erstellen und es zu einen späteren Zeitpunkt wiederherstellen.",
            anchor="w",
        )
        layout_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        classico_button = ttk.Button(
            self.desktop_layout_set,
            compound="center",
            image=self.classico_thumb,
            command=set_classico_panel,
        )
        classico_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        classico_label = ttk.Label(
            self.desktop_layout_set, text="Standard", anchor="center"
        )
        classico_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        upside_button = ttk.Button(
            self.desktop_layout_set,
            compound="center",
            image=self.upside_thumb,
            command=set_upside_down_panel,
        )
        upside_button.grid(row=1, column=1, padx=5, pady=5, sticky="nesw")

        upside_label = ttk.Label(
            self.desktop_layout_set, text="Spiegel", anchor="center"
        )
        upside_label.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        elfi_button = ttk.Button(
            self.desktop_layout_set,
            compound="center",
            image=self.elfi_thumb,
            command=set_elfi_panel,
        )
        elfi_button.grid(row=1, column=2, padx=5, pady=5, sticky="nesw")

        elfi_label = ttk.Label(self.desktop_layout_set, text="11", anchor="center")
        elfi_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        devil_button = ttk.Button(
            self.desktop_layout_set,
            compound="center",
            image=self.devil_thumb,
            command=set_der_teufel_panel,
        )
        devil_button.grid(row=1, column=3, padx=5, pady=5, sticky="nesw")

        devil_label = ttk.Label(
            self.desktop_layout_set, text="Ubuntu-Like", anchor="center"
        )
        devil_label.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        save_layout = ttk.Button(
            self.desktop_layout_set,
            text="Mein Layout speichern",
            style="Custom.TButton",
            image=self.save_layout_icon,
            compound="left",
            command=backup_cinnamon_settings,
        )
        save_layout.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nesw")

        load_layout = ttk.Button(
            self.desktop_layout_set,
            text="Mein Layout laden",
            style="Custom.TButton",
            image=self.load_layout_icon,
            compound="left",
            command=restore_cinnamon_settings,
        )
        load_layout.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="nesw")

        self.pixel_set = ttk.LabelFrame(self, text="Farben und Formen", padding=10)
        self.pixel_set.pack(pady=20, padx=40, fill="x", anchor="n")
        self.pixel_set.columnconfigure(0, weight=1)
        self.pixel_set.rowconfigure(0, weight=1)

        def done_message_0():
            d_mass = Done_(self)
            d_mass.grab_set()

        def update_theme_combobox():
            try:
                themes = [
                    d
                    for d in os.listdir("/usr/share/themes")
                    if os.path.isdir(os.path.join("/usr/share/themes", d))
                ]
                themes.sort()
                themes = [
                    x
                    for x in themes
                    if x
                    not in [
                        "BlackMATE",
                        "BlueMenta",
                        "Blue-Submarine",
                        "Clearlooks",
                        "ContrastHigh",
                        "Crux",
                        "Default",
                        "Emacs",
                        "GreenLaguna",
                        "Green-Submarine",
                        "HighContrast",
                        "HighContrastInverse",
                        "Industrial",
                        "Menta",
                        "Raleigh",
                        "Redmond",
                        "Shiny",
                        "ThinIce",
                        "TraditionalGreen",
                        "TraditionalOk",
                        "WhiteSur-Dark",
                        "WhiteSur-Dark-hdpi",
                        "WhiteSur-Dark-solid-hdpi",
                        "WhiteSur-Dark-solid-xhdpi",
                        "WhiteSur-Dark-xhdpi",
                        "WhiteSur-Light",
                        "WhiteSur-Light-hdpi",
                        "WhiteSur-Light-solid-hdpi",
                        "WhiteSur-Light-solid-xhdpi",
                        "WhiteSur-Light-xhdpi",
                        "YaruOk",
                        "Yaru-xhdpi",
                        "Yaru",
                        "YaruGreen",
                        "Yaru-dark-hdpi", 
                        "Yaru-dark-xhdpi", 
                        "Yaru-hdpi",
                        "Yaru-xhdpi",
                        "Mist"
                    ]
                ]

                theme_combobox["values"] = themes
                theme_combobox.set("Theme wählen")
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
                icon_combobox.set("Symbole wählen")
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
                cursor_combobox.set("Cursor wählen")
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

            if selected_theme != "Bitte aktualisieren":
                # Liste der GSettings-Schlüssel und deren Pfade
                settings_keys = [
                    # ("org.gnome.desktop.interface", "gtk-theme"),
                    ("org.cinnamon.desktop.wm.preferences", "theme"),
                    # ("org.gnome.desktop.wm.preferences", "theme"),
                    ("org.cinnamon.desktop.interface", "gtk-theme"),
                    ("org.cinnamon.theme", "name"),
                ]

                # Funktion zum Setzen eines GSettings-Werts
                def set_gsettings_value(schema, key, value):
                    subprocess.run(["gsettings", "set", schema, key, value], check=True)

                    if "dark" in value or "Dark" in value:
                        # /org/gnome/desktop/interface/color-scheme
                        subprocess.Popen(
                            [
                                "gsettings",
                                "set",
                                "org.gnome.desktop.interface",
                                "color-scheme",
                                "'prefer-dark'",
                            ]
                        )
                        # os.system("gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'")

                    else:
                        subprocess.Popen(
                            [
                                "gsettings",
                                "set",
                                "org.gnome.desktop.interface",
                                "color-scheme",
                                "'prefer-light'",
                            ]
                        )
                        # os.system("gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'")

                # Für jeden Schlüssel den Wert setzen
                for schema, key in settings_keys:
                    set_gsettings_value(schema, key, selected_theme)
                    logger.info(f"{schema}.{key} wurde auf {selected_theme} gesetzt.")
                done_message_0()

        def set_icon():
            selected_icon = icon_combobox.get()

            if selected_icon != "Bitte aktualisieren":
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

            if selected_cursor != "Bitte aktualisieren":
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

        def apply_cursor_size():
            selected_size = cursor_size_combobox.get()
            if not selected_size.isdigit():
                messagebox.showerror("Fehler", "Bitte eine gültige Größe wählen.")
                return

            try:
                subprocess.run([
                    "gsettings",
                    "set",
                    "org.cinnamon.desktop.interface",
                    "cursor-size",
                    selected_size
                ], check=True)
                messagebox.showinfo("Erfolg", f"Cursorgröße auf {selected_size}px gesetzt.")
            except subprocess.CalledProcessError:
                print("Fehler beim Setzen der Cursorgröße.")


        theme_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        theme_combobox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        theme_combobox.set("Bitte aktualisieren")

        icon_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        icon_combobox.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        icon_combobox.set("Bitte aktualisieren")

        cursor_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        cursor_combobox.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        cursor_combobox.set("Bitte aktualisieren")

        cursor_sizes = ["16", "24", "32", "48", "64", "96", "128"]
        cursor_size_combobox = ttk.Combobox(self.pixel_set, state="readonly")
        cursor_size_combobox['values'] = cursor_sizes
        cursor_size_combobox.grid(
            row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        cursor_size_combobox.set("Cursor-Größe wählen")


        theme_button = ttk.Button(
            self.pixel_set,
            text="Theme anwenden",
            compound="left",
            image=self.theme_folder_icon,
            command=set_theme,
            width=20,
        )
        theme_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        icon_button = ttk.Button(
            self.pixel_set,
            text="Symbole anwenden",
            compound="left",
            image=self.icon_folder_icon,
            command=set_icon,
            width=20,
        )
        icon_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        cursor_button = ttk.Button(
            self.pixel_set,
            text="Cursor anwenden",
            compound="left",
            image=self.cursor_folder_icon,
            command=set_cursor,
            width=20,
        )
        cursor_button.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        cursor_size_button = ttk.Button(self.pixel_set, compound="left", text="Cursorgröße anwenden", image=self.cursor_size_icon, command=apply_cursor_size)
        cursor_size_button.grid(row=4, column=3,columnspan=2, padx=10, pady=5, sticky="ew")

        theme_refresh_button = ttk.Button(
            self.pixel_set,
            text="Aktualisieren",
            compound="left",
            image=self.refresh_icon,
            command=update_theme_combobox,
            width=20,
            style="Custom.TButton",
        )
        theme_refresh_button.grid(
            row=5, column=0, columnspan=5, padx=10, pady=5, sticky="ew"
        )

        theme_folder_button = ttk.Button(
            self.pixel_set,
            text="Theme-Ordner",
            image=self.folder_icon,
            compound="left",
            command=open_theme_folder,
            width=20,
        )
        theme_folder_button.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        icon_folder_button = ttk.Button(
            self.pixel_set,
            text="Symbol-Ordner",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20,
        )
        icon_folder_button.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        cursor_folder_button = ttk.Button(
            self.pixel_set,
            text="Cursor-Ordner",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20,
        )
        cursor_folder_button.grid(row=3, column=4, padx=10, pady=5, sticky="ew")

        update_theme_combobox()
