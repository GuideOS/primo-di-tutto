import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
from resorcess import *
from apt_manage import *
import subprocess
from flatpak_alias_list import *
from tabs.pop_ups import *
import json
import shutil
from logger_config import setup_logger
from back_my_cinnamon import *
from restore_my_cinnamon import *

logger = setup_logger(__name__)


class LookTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.classico_thumb_light = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/classico_thumb_light.png"
        )
        self.upside_thumb_light = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/upside_thumb_light.png"
        )
        self.elfi_thumb_light = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/elfi_thumb_light.png"
        )
        self.devil_thumb_light = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/devil_thumb_light.png"
        )
        self.classico_thumb_dark = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/classico_thumb_dark.png"
        )
        self.upside_thumb_dark = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/upside_thumb_dark.png"
        )
        self.elfi_thumb_dark = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/elfi_thumb_dark.png"
        )
        self.devil_thumb_dark = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/devil_thumb_dark.png"
        )

        def notebook_styler():
            # Notebook Theming
            global noteStyler
            noteStyler = ttk.Style(self)
            noteStyler.configure(
                "TNotebook",
                borderwidth=0,
                tabposition="w",
                highlightthickness=0,
            )
            noteStyler.configure(
                "TNotebook.Tab",
                borderwidth=0,
                font=font_10,
                width=18,
                highlightthickness=0,
            )

            noteStyler.configure("TButton", justify="left", anchor="w")

            noteStyler.configure("Custom.TButton", justify="center", anchor="center")
            noteStyler.configure(
                "Accent2.TButton", justify="center", anchor="center", font=font_12
            )

        def backup_grouped_config():
            # Backup the Cinnamon grouped-window-list configuration JSON file
            # Returns True if successful, False otherwise

            # Directory containing the JSON configuration file
            config_dir = os.path.expanduser(
                "~/.config/cinnamon/spices/grouped-window-list@cinnamon.org"
            )

            # Check if the directory exists
            if not os.path.exists(config_dir):
                logger.error(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Find the file matching the pattern
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

            # Path to the original file
            file_path = os.path.join(config_dir, json_file)
            # Path to the backup file
            backup_file_path = os.path.join(config_dir, "69.bak")

            try:
                # Copy the file
                shutil.copy(file_path, backup_file_path)
                logger.info(f"Backup erfolgreich erstellt: {backup_file_path}")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Erstellen des Backups: {e}")
                return False

        # Funktion aufrufen
        backup_grouped_config()

        def restore_cinnamon_config(file_number, c_dir):
            # Restore the Cinnamon grouped-window-list configuration from backup
            # file_number: target JSON file number
            # c_dir: config directory
            # Returns True if successful, False otherwise

            # Directory containing the JSON configuration file
            config_dir = os.path.expanduser(c_dir)

            # Check if the directory exists
            if not os.path.exists(config_dir):
                logger.error(f"Das Verzeichnis {config_dir} wurde nicht gefunden.")
                return False

            # Path to the backup file
            backup_file_path = os.path.join(config_dir, "69.bak")

            # Check if the backup file exists
            if not os.path.exists(backup_file_path):
                logger.error(f"Das Backup {backup_file_path} wurde nicht gefunden.")
                return False

            # Target JSON filename based on the number
            restored_file_name = f"{file_number}.json"
            restored_file_path = os.path.join(config_dir, restored_file_name)

            try:
                # Restore the backup
                shutil.copy(backup_file_path, restored_file_path)
                logger.info(
                    f"Backup erfolgreich wiederhergestellt als: {restored_file_path}"
                )
                return True
            except Exception as e:
                logger.error(f"Fehler beim Wiederherstellen des Backups: {e}")
                return False

        def check_plank_autostart():
            # Remove plank.desktop from autostart if it exists

            # Path to the file
            path = os.path.expanduser("~/.config/autostart/plank.desktop")

            # Check if the file exists
            if os.path.exists(path):
                try:
                    # Delete the file
                    os.remove(path)
                    logger.info(f"Die Datei {path} wurde gelöscht.")
                except Exception as e:
                    logger.error(f"Fehler beim Löschen der Datei: {e}")
            else:
                logger.warning(f"Die Datei {path} existiert nicht.")

        def copy_dockitems():
            # Copy all .dockitem files from the application scripts directory to Plank's launchers directory

            # Define source and destination directories
            src = f"{application_path}/scripts/"
            dest = os.path.expanduser("~/.config/plank/dock1/launchers")

            # Check if the source directory exists
            if not os.path.exists(src):
                logger.warning(f"Quellverzeichnis {src} existiert nicht.")
                return

            # Create the destination directory if it does not exist
            if not os.path.exists(dest):
                os.makedirs(dest)
                logger.info(f"Zielverzeichnis {dest} wurde erstellt.")

            # Copy all .dockitem files
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
            # Write predefined values to dconf for Plank dock configuration

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

            # Source and destination paths
            source_path = f"{application_path}/scripts/plank.desktop"
            destination_path = os.path.expanduser("~/.config/autostart/plank.desktop")

            # Funktion aufrufen
            copy_file(source_path, destination_path)

        def copy_file(source, destination):
            # Copy a file from source to destination, creating the destination directory if needed

            try:
                # Ensure the destination directory exists
                destination_dir = os.path.dirname(destination)
                os.makedirs(destination_dir, exist_ok=True)

                # Datei kopieren
                shutil.copy2(source, destination)
                logger.info(f"Datei erfolgreich kopiert: {source} -> {destination}")
            except Exception as e:
                logger.error(f"Fehler beim Kopieren der Datei: {e}")

        def copy_guide_menu(application_path):
            # Copy guide_menu.json to the Cinnamon menu spices directory as 0.json

            """
            Copies the guide_menu.json file to the Cinnamon menu directory

            Args:
                application_path (str): Der Pfad zum Hauptverzeichnis der Anwendung.
            """
            source_file = f"{application_path}/scripts/guide_menu.json"
            destination_directory = os.path.expanduser(
                "~/.config/cinnamon/spices/menu@cinnamon.org"
            )
            destination_file = os.path.join(destination_directory, "0.json")

            # Create the destination directory if it does not exist
            os.makedirs(destination_directory, exist_ok=True)

            # Copy the file
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
            # Set up the Elfi panel layout

            popen("killall plank")
            check_plank_autostart()

            copy_guide_menu(application_path)

            # subprocess.run(["gsettings", "set", "org.cinnamon", key, f"{value}"])
            subprocess.run(
                f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_elf",
                shell=True,
                check=True,
            )

            # Source and destination paths
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
            # Set up the Classico panel layout

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
            # Set up the Der Teufel panel layout

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
            # Set up the Upside Down panel layout

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

        def layout_icon_conf_light():
            classico_button.configure(image=self.classico_thumb_light)
            upside_button.configure(image=self.upside_thumb_light)
            elfi_button.configure(image=self.elfi_thumb_light)
            devil_button.configure(image=self.devil_thumb_light)

        def layout_icon_conf_dark():
            classico_button.configure(image=self.classico_thumb_dark)
            upside_button.configure(image=self.upside_thumb_dark)
            elfi_button.configure(image=self.elfi_thumb_dark)
            devil_button.configure(image=self.devil_thumb_dark)

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
            image=self.classico_thumb_light,
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
            image=self.upside_thumb_light,
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
            image=self.elfi_thumb_light,
            command=set_elfi_panel,
        )
        elfi_button.grid(row=1, column=2, padx=5, pady=5, sticky="nesw")

        elfi_label = ttk.Label(self.desktop_layout_set, text="11", anchor="center")
        elfi_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        devil_button = ttk.Button(
            self.desktop_layout_set,
            compound="center",
            image=self.devil_thumb_light,
            command=set_der_teufel_panel,
        )
        devil_button.grid(row=1, column=3, padx=5, pady=5, sticky="nesw")

        devil_label = ttk.Label(
            self.desktop_layout_set, text="Ubuntu-Like", anchor="center"
        )
        devil_label.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        if "dark" in theme_name or "Dark" in theme_name:
            layout_icon_conf_dark()
        else:
            layout_icon_conf_light()

        save_layout = ttk.Button(
            self.desktop_layout_set,
            text="Mein Layout speichern",
            style="Custom.TButton",
            compound="left",
            command=backup_cinnamon_settings,
        )
        save_layout.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nesw")

        load_layout = ttk.Button(
            self.desktop_layout_set,
            text="Mein Layout laden",
            style="Custom.TButton",
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
            # Update the theme, icon, and cursor comboboxes with available options

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
                        "Mist",
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
                icons = [
                    x
                    for x in icons
                    if x
                    not in [
                        "ContrastHigh",
                        "default",
                        "desktop-base",
                        "gnome",
                        "hicolor",
                        "HighContrast",
                        "locolor",
                        "mate",
                        "mate-black",
                        "menta",
                        "mozc",
                        "vendor",
                        "zbar.ico",
                    ]
                ]
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

        def set_theme():
            # Set the selected theme in GSettings and update the UI accordingly

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
                        self.tk.call("set_theme", "dark")
                        notebook_styler()
                        layout_icon_conf_dark()

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
                        self.tk.call("set_theme", "light")
                        notebook_styler()
                        layout_icon_conf_light()

                # Für jeden Schlüssel den Wert setzen
                for schema, key in settings_keys:
                    set_gsettings_value(schema, key, selected_theme)
                    logger.info(f"{schema}.{key} wurde auf {selected_theme} gesetzt.")
                done_message_0()

        def set_icon():
            # Set the selected icon theme in GSettings

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
            # Set the selected cursor theme in GSettings

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
            # Open the system theme directory in a file manager

            popen("pkexec nemo /usr/share/themes")

        def open_icon_folder():
            # Open the system icon directory in a file manager

            popen("pkexec nemo /usr/share/icons")

        def apply_cursor_size():
            # Apply the selected cursor size in GSettings

            selected_size = cursor_size_combobox.get()
            if not selected_size.isdigit():
                messagebox.showerror("Fehler", "Bitte eine gültige Größe wählen.")
                return

            try:
                subprocess.run(
                    [
                        "gsettings",
                        "set",
                        "org.cinnamon.desktop.interface",
                        "cursor-size",
                        selected_size,
                    ],
                    check=True,
                )
                messagebox.showinfo(
                    "Erfolg", f"Cursorgröße auf {selected_size}px gesetzt."
                )
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
        cursor_size_combobox["values"] = cursor_sizes
        cursor_size_combobox.grid(
            row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ewsn"
        )
        cursor_size_combobox.set("Cursor-Größe wählen")

        theme_button = ttk.Button(
            self.pixel_set,
            text="Theme anwenden",
            compound="left",
            command=set_theme,
            width=20,
        )
        theme_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        icon_button = ttk.Button(
            self.pixel_set,
            text="Symbole anwenden",
            compound="left",
            command=set_icon,
            width=20,
        )
        icon_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        cursor_button = ttk.Button(
            self.pixel_set,
            text="Cursor anwenden",
            compound="left",
            command=set_cursor,
            width=20,
        )
        cursor_button.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        cursor_size_button = ttk.Button(
            self.pixel_set,
            compound="left",
            text="Cursorgröße anwenden",
            command=apply_cursor_size,
        )
        cursor_size_button.grid(
            row=4, column=3, columnspan=2, padx=10, pady=5, sticky="ew"
        )

        theme_refresh_button = ttk.Button(
            self.pixel_set,
            text="Aktualisieren",
            compound="left",
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
            compound="left",
            command=open_theme_folder,
            width=20,
        )
        theme_folder_button.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        icon_folder_button = ttk.Button(
            self.pixel_set,
            text="Symbol-Ordner",
            compound="left",
            command=open_icon_folder,
            width=20,
        )
        icon_folder_button.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        cursor_folder_button = ttk.Button(
            self.pixel_set,
            text="Cursor-Ordner",
            compound="left",
            command=open_icon_folder,
            width=20,
        )
        cursor_folder_button.grid(row=3, column=4, padx=10, pady=5, sticky="ew")

        update_theme_combobox()
