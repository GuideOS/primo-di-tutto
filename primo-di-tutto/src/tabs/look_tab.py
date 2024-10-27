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

        def set_elfi_panel():
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )

            # Erster Befehl: Setze das Panel unten
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "panels-enabled", "['1:0:bottom']"]
            )

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.cinnamon",
                    "enabled-applets",
                    "['panel1:center:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel1:center:1:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']",
                ]
            )

        def set_classico_panel():
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            # Transparent Panel
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

            # subprocess.run([
            #    'gsettings', 'set', 'org.cinnamon', 'enabled-extensions', "['opacify@anish.org', 'transparent-panels@germanfr']"
            # ])

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
                "allow-other-notification-handlers": "false",
                "alttab-minimized-aware": "false",
                "alttab-switcher-delay": "100",
                "alttab-switcher-enforce-primary-monitor": "false",
                "alttab-switcher-show-all-workspaces": "false",
                "alttab-switcher-style": "'icons+thumbnails'",
                "alttab-switcher-warp-mouse-pointer": "false",
                "app-menu-icon-name": "'ubuntucinnamon-symbolic'",
                "app-menu-label": "'Menu'",
                "applet-cache-updated": "0",
                "bring-windows-to-current-workspace": "false",
                "center-warped-pointer": "true",
                "cinnamon-settings-advanced": "false",
                "command-history": "@as []",
                "date-format": "'%a, %h %d %Y%l:%M %p'",
                "demands-attention-ignored-wm-classes": "@as []",
                "demands-attention-passthru-wm-classes": "['gnome-screenshot', 'lxterminal', 'xfce4-terminal', 'firefox', 'libreoffice', 'soffice']",
                "desklet-cache-updated": "0",
                "desklet-decorations": "1",
                "desklet-snap": "true",
                "desklet-snap-interval": "25",
                "desktop-effects": "true",
                "desktop-effects-change-size": "true",
                "desktop-effects-close": "'traditional'",
                "desktop-effects-map": "'traditional'",
                "desktop-effects-minimize": "'traditional'",
                "desktop-effects-on-dialogs": "true",
                "desktop-effects-on-menus": "true",
                "desktop-effects-sizechange-effect": "'scale'",
                "desktop-effects-sizechange-time": "100",
                "desktop-effects-sizechange-transition": "'easeInQuad'",
                "desktop-effects-workspace": "true",
                "desktop-layout": "''",
                "development-tools": "true",
                "device-aliases": "@as []",
                "disabled-open-search-providers": "@as []",
                "edge-flip-delay": "1000",
                "enable-app-monitoring": "true",
                "enable-edge-flip": "false",
                "enable-indicators": "false",
                "enable-vfade": "true",
                "enabled-applets": "['panel1:left:0:menu@cinnamon.org:0', 'panel1:left:2:grouped-window-list@cinnamon.org:2', 'panel1:right:2:systray@cinnamon.org:3', 'panel1:right:3:xapp-status@cinnamon.org:4', 'panel1:right:4:notifications@cinnamon.org:5', 'panel1:right:5:printers@cinnamon.org:6', 'panel1:right:6:removable-drives@cinnamon.org:7', 'panel1:right:7:keyboard@cinnamon.org:8', 'panel1:right:8:favorites@cinnamon.org:9', 'panel1:right:9:network@cinnamon.org:10', 'panel1:right:10:sound@cinnamon.org:11', 'panel1:right:11:power@cinnamon.org:12', 'panel2:center:0:calendar@cinnamon.org:13', 'panel1:right:1:trash@cinnamon.org:15', 'panel2:right:1:temperature@fevimu:16', 'panel1:left:1:placesCenter@scollins:17', 'panel1:right:13:sessionManager@scollins:18', 'panel2:center:1:weather@mockturtl:19', 'panel1:right:12:calendar@cinnamon.org:20', 'panel1:right:0:expo@cinnamon.org:22']",
                "enabled-desklets": "@as []",
                "enabled-extensions": "['opacify@anish.org', 'transparent-panels@germanfr']",
                "enabled-search-providers": "@as []",
                "extension-cache-updated": "0",
                "favorite-apps": "['cinnamon-settings.desktop', 'nemo.desktop', 'org.gnome.Software.desktop', 'system-config-printer.desktop', 'org.gnome.DejaDup.desktop']",
                "hotcorner-layout": "['expo:false:0', 'scale:false:0', 'scale:false:0', 'desktop:false:0']",
                "hoverclick-action": "'single'",
                "hoverclick-layout": "'vertical::both'",
                "hoverclick-position": "''",
                "lock-desklets": "false",
                "looking-glass-history": "@as []",
                "next-applet-id": "23",
                "next-desklet-id": "0",
                "no-adjacent-panel-barriers": "false",
                "number-workspaces": "0",
                "overview-corner": "['DEPRECATED']",
                "panel-edit-mode": "false",
                "panel-launchers": "['DEPRECATED']",
                "panel-launchers-draggable": "true",
                "panel-scale-text-icons": "false",
                "panel-zone-icon-sizes": '\'[{"panelId": 1, "left": 0, "center": 0, "right": 22}, {"left": 0, "center": 0, "right": 0, "panelId": 2}]\'',
                "panel-zone-symbolic-icon-sizes": '\'[{"panelId": 1, "left": 22, "center": 28, "right": 18}, {"left": 28, "center": 17, "right": 28, "panelId": 2}]\'',
                "panel-zone-text-sizes": '\'[{"panelId":1,"left":0,"center":0,"right":0},{"left":0,"center":0,"right":0,"panelId":2}]\'',
                "panels-autohide": "['1:false', '2:intel']",
                "panels-enabled": "['1:0:bottom', '2:0:top']",
                "panels-height": "['1:38', '2:21']",
                "panels-hide-delay": "['1:0', '2:0']",
                "panels-show-delay": "['1:0', '2:0']",
                "prevent-focus-stealing": "false",
                "run-dialog-aliases": "['<Super>r']",
                "run-dialog-show-completions": "true",
                "saved-im-presence": "1",
                "saved-session-presence": "0",
                "show-media-keys-osd": "'medium'",
                "show-snap-osd": "true",
                "show-tile-hud": "true",
                "startup-animation": "true",
                "startup-icon-name": "''",
                "system-icon": "''",
                "window-effect-speed": "1",
                "workspace-expo-view-as-grid": "false",
                "workspace-name-overrides": "['DEPRECATED']",
                "workspace-osd-visible": "true",
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

        def set_der_teufel_panel():

            # Transparent Panel
            config_path = os.path.expanduser(
                "~/.config/cinnamon/spices/transparent-panels@germanfr/transparent-panels@germanfr.json"
            )

            with open(config_path, "r") as file:
                config = json.load(file)

            config["transparency-type"]["value"] = "panel-semi-transparent"
            config["panel-top"]["value"] = False
            config["panel-bottom"]["value"] = False
            config["panel-left"]["value"] = False
            config["panel-right"]["value"] = False

            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)

            with open(config_path, "r") as file:
                config = json.load(file)

            # Werte aktualisieren
            config["transparency-type"]["value"] = "panel-semi-transparent"
            config["panel-top"]["value"] = False
            config["panel-bottom"]["value"] = False
            config["panel-left"]["value"] = True
            config["panel-right"]["value"] = False

            # Konfigurationsdatei speichern
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)

            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-desklets", "[]"]
            )

            gsettings_config = {
                "allow-other-notification-handlers": False,
                "alttab-minimized-aware": False,
                "alttab-switcher-delay": 100,
                "alttab-switcher-enforce-primary-monitor": False,
                "alttab-switcher-show-all-workspaces": False,
                "alttab-switcher-style": "icons+thumbnails",
                "alttab-switcher-warp-mouse-pointer": False,
                "app-menu-icon-name": "ubuntucinnamon-symbolic",
                "app-menu-label": "Menu",
                "applet-cache-updated": 0,
                "bring-windows-to-current-workspace": False,
                "center-warped-pointer": True,
                "cinnamon-settings-advanced": False,
                "command-history": [],
                "date-format": "%a, %h %d %Y%l:%M %p",
                "demands-attention-ignored-wm-classes": [],
                "demands-attention-passthru-wm-classes": [
                    "gnome-screenshot", "lxterminal", "xfce4-terminal", "firefox", "libreoffice", "soffice"
                ],
                "desklet-cache-updated": 0,
                "desklet-decorations": 1,
                "desklet-snap": True,
                "desklet-snap-interval": 25,
                "desktop-effects": True,
                "desktop-effects-change-size": True,
                "desktop-effects-close": "traditional",
                "desktop-effects-map": "traditional",
                "desktop-effects-minimize": "traditional",
                "desktop-effects-on-dialogs": True,
                "desktop-effects-on-menus": True,
                "desktop-effects-sizechange-effect": "scale",
                "desktop-effects-sizechange-time": 100,
                "desktop-effects-sizechange-transition": "easeInQuad",
                "desktop-effects-workspace": True,
                "desktop-layout": "",
                "development-tools": True,
                "device-aliases": [],
                "disabled-open-search-providers": [],
                "edge-flip-delay": 1000,
                "enable-app-monitoring": True,
                "enable-edge-flip": False,
                "enable-indicators": False,
                "enable-vfade": True,
                "enabled-applets": [
                    "panel1:left:2:grouped-window-list@cinnamon.org:2", "panel1:right:2:systray@cinnamon.org:3",
                    "panel1:right:3:xapp-status@cinnamon.org:4", "panel2:right:1:notifications@cinnamon.org:5",
                    "panel2:right:5:printers@cinnamon.org:6", "panel2:right:3:removable-drives@cinnamon.org:7",
                    "panel2:right:2:keyboard@cinnamon.org:8", "panel2:right:4:favorites@cinnamon.org:9",
                    "panel2:right:6:network@cinnamon.org:10", "panel2:right:7:sound@cinnamon.org:11",
                    "panel2:right:8:power@cinnamon.org:12", "panel2:center:0:calendar@cinnamon.org:13",
                    "panel2:right:0:temperature@fevimu:16", "panel2:right:9:sessionManager@scollins:18",
                    "panel2:center:2:weather@mockturtl:19", "panel2:center:1:calendar@cinnamon.org:20",
                    "panel2:left:0:expo@cinnamon.org:22", "panel1:right:0:panel-launchers@cinnamon.org:23"
                ],
                "enabled-desklets": [],
                "enabled-extensions": ["opacify@anish.org", "transparent-panels@germanfr"],
                "enabled-search-providers": [],
                "extension-cache-updated": 0,
                "favorite-apps": [
                    "cinnamon-settings.desktop", "nemo.desktop", "org.gnome.Software.desktop",
                    "system-config-printer.desktop", "org.gnome.DejaDup.desktop"
                ],
                "hotcorner-layout": ["expo:false:0", "scale:false:0", "scale:false:0", "desktop:false:0"],
                "hoverclick-action": "single",
                "hoverclick-layout": "vertical::both",
                "hoverclick-position": "",
                "lock-desklets": False,
                "looking-glass-history": [],
                "next-applet-id": 24,
                "next-desklet-id": 0,
                "no-adjacent-panel-barriers": False,
                "number-workspaces": 0,
                "overview-corner": ["DEPRECATED"],
                "panel-edit-mode": False,
                "panel-launchers": ["DEPRECATED"],
                "panel-launchers-draggable": True,
                "panel-scale-text-icons": False,
                "panel-zone-icon-sizes": '[{"panelId": 1, "left": 0, "center": 0, "right": 0}, {"left": 0, "center": 0, "right": 0, "panelId": 2}]',
                "panel-zone-symbolic-icon-sizes": '[{"panelId": 1, "left": 28, "center": 28, "right": 18}, {"left": 28, "center": 17, "right": 28, "panelId": 2}]',
                "panel-zone-text-sizes": '[{"panelId":1,"left":0,"center":0,"right":0},{"left":0,"center":0,"right":0,"panelId":2}]',
                "panels-autohide": ["1:false", "2:false"],
                "panels-enabled": ["1:0:left", "2:0:top"],
                "panels-height": ["1:47", "2:22"],
                "panels-hide-delay": ["1:0", "2:0"],
                "panels-show-delay": ["1:0", "2:0"],
                "prevent-focus-stealing": False,
                "run-dialog-aliases": ["<Super>r"],
                "run-dialog-show-completions": True,
                "saved-im-presence": 1,
                "saved-session-presence": 0,
                "show-media-keys-osd": "medium",
                "show-snap-osd": True,
                "show-tile-hud": True,
                "startup-animation": True,
                "startup-icon-name": "",
                "system-icon": "",
                "window-effect-speed": 1,
                "workspace-expo-view-as-grid": False,
                "workspace-name-overrides": ["DEPRECATED"],
                "workspace-osd-visible": True
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


        def set_upside_down_panel():
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"]
            )
            # Erster Befehl: Setze das Panel oben
            subprocess.run(
                ["gsettings", "set", "org.cinnamon", "panels-enabled", "['1:0:top']"]
            )

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.cinnamon",
                    "enabled-applets",
                    "['panel1:left:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel1:left:2:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']",
                ]
            )

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
