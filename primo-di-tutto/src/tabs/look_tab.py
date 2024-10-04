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

        def set_elfi_panel():
            # Erster Befehl: Setze das Panel unten
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'panels-enabled', "['1:0:bottom']"
            ])

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'enabled-applets',
                "['panel1:center:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel1:center:1:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']"
            ])

        def set_classico_panel():
            # Erster Befehl: Setze das Panel unten
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'panels-enabled', "['1:0:bottom']"
            ])

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'enabled-applets',
                "['panel1:left:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel1:left:2:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']"
            ])

        def set_der_teufel_panel():
            # Erster Befehl: Setze das Panel oben und links
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'panels-enabled', "['1:0:top', '2:0:left']"
            ])

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'enabled-applets',
                "['panel2:right:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel2:left:0:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']"
            ])

        def set_upside_down_panel():
            # Erster Befehl: Setze das Panel oben
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'panels-enabled', "['1:0:top']"
            ])

            # Zweiter Befehl: Setze die aktivierten Applets
            subprocess.run([
                'gsettings', 'set', 'org.cinnamon', 'enabled-applets',
                "['panel1:left:0:menu@cinnamon.org:0', 'panel1:left:1:separator@cinnamon.org:1', 'panel1:left:2:grouped-window-list@cinnamon.org:2', 'panel1:right:0:systray@cinnamon.org:3', 'panel1:right:1:xapp-status@cinnamon.org:4', 'panel1:right:2:notifications@cinnamon.org:5', 'panel1:right:3:printers@cinnamon.org:6', 'panel1:right:4:removable-drives@cinnamon.org:7', 'panel1:right:5:keyboard@cinnamon.org:8', 'panel1:right:6:favorites@cinnamon.org:9', 'panel1:right:7:network@cinnamon.org:10', 'panel1:right:8:sound@cinnamon.org:11', 'panel1:right:9:power@cinnamon.org:12', 'panel1:right:10:calendar@cinnamon.org:13', 'panel1:right:11:cornerbar@cinnamon.org:14']"
            ])


        self.desktop_layout_set = ttk.LabelFrame(
            self,
            text="Layout",
            padding=10
        )
        self.desktop_layout_set.pack(pady=20, padx=40, fill="x", anchor="n")
        self.desktop_layout_set.grid_columnconfigure(0, weight=1)
        self.desktop_layout_set.grid_columnconfigure(1, weight=1)
        self.desktop_layout_set.grid_columnconfigure(2, weight=1)
        self.desktop_layout_set.grid_columnconfigure(3, weight=1)

        classico_button = ttk.Button(
            self.desktop_layout_set,
            text="Classico\n(Standard)",
            compound="center",
            image=self.classico_thumb,
            command=set_classico_panel,
            

        )
        classico_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        upside_button = ttk.Button(
            self.desktop_layout_set,
            text="upside down",
            compound="center",
            image=self.upside_thumb,
            command=set_upside_down_panel,
            

        )
        upside_button.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")

        elfi_button = ttk.Button(
            self.desktop_layout_set,
            text="elfi",
            compound="center",
            image=self.elfi_thumb,
            command=set_elfi_panel,
            

        )
        elfi_button.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")


        devil_button = ttk.Button(
            self.desktop_layout_set,
            text=" the devil",
            compound="center",
            image=self.devil_thumb,
            command=set_der_teufel_panel,
            

        )
        devil_button.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")        

        self.pixel_set = ttk.LabelFrame(
            self,
            text="Theme Your Desktop",
            padding=10
        )
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
                if get_desktop_environment() == "xfce":
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xsettings",
                            "-p",
                            "/Net/ThemeName",
                            "-s",
                            selected_theme,
                        ]
                    )
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xfwm4",
                            "-p",
                            "/general/theme",
                            "-s",
                            selected_theme,
                        ]
                    )
                if get_desktop_environment() == "mate":
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.mate.interface",
                            "gtk-theme",
                            selected_theme,
                        ]
                    )
                if get_desktop_environment() == "lxde":
                    update_lxde_theme_config(selected_theme)

                else:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.interface",
                            "gtk-theme",
                            selected_theme,
                        ]
                    )
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.wm.preferences",
                            "theme",
                            selected_theme,
                        ]
                    )
                done_message_0()

        def set_icon():
            selected_icon = icon_combobox.get()

            if selected_icon != "Press Refresh":
                if get_desktop_environment() == "xfce":
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xsettings",
                            "-p",
                            "/Net/IconThemeName",
                            "-s",
                            selected_icon,
                        ]
                    )
                if get_desktop_environment() == "lxde":
                    update_lxde_icons_config(selected_icon)
                else:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.interface",
                            "icon-theme",
                            selected_icon,
                        ]
                    )
            done_message_0()

        def set_cursor():
            selected_cursor = cursor_combobox.get()

            if selected_cursor != "Press Refresh":
                if get_desktop_environment() == "xfce":
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xsettings",
                            "-p",
                            "/Gtk/CursorThemeName",
                            "-s",
                            selected_cursor,
                        ]
                    )
                if get_desktop_environment() == "lxde":
                    update_lxde_cursor_config(selected_cursor)
                else:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.interface",
                            "cursor-theme",
                            selected_cursor,
                        ]
                    )
            done_message_0()

        def open_theme_folder():
            if check_pcmanfm() == True:
                popen("sudo pcmanfm /usr/share/themes")
            else:
                popen(
                    f"{permit} env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY xdg-open /usr/share/themes"
                )

        def open_icon_folder():
            if check_pcmanfm() == True:
                popen("sudo pcmanfm /usr/share/icons")
            else:
                popen(
                    f"{permit} env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY xdg-open /usr/share/icons"
                )

        def open_lxappearance():
            popen("lxappearance")

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
            width=20

        )
        theme_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        icon_button = ttk.Button(
            self.pixel_set,
            text="Set Icon",
            compound="left",
            image=self.icon_folder_icon,
            command=set_icon,
            width=20

        )
        icon_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        cursor_button = ttk.Button(
            self.pixel_set,
            text="Set Cursor",
            compound="left",
            image=self.cursor_folder_icon,
            command=set_cursor,
            width=20

        )
        cursor_button.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        theme_refresh_button = ttk.Button(
            self.pixel_set,
            text="Refresh",
            compound="left",
            image=self.refresh_icon,
            command=update_theme_combobox,
            width=20,
            style="Custom.TButton"
        )
        theme_refresh_button.grid(
            row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        theme_legacy_button = ttk.Button(
            self.pixel_set,
            text="Legacy Theme Bullseye",
            command=open_lxappearance,
            style="Custom.TButton",
            state=DISABLED,
            width=20
        )
        theme_legacy_button.grid(row=4, column=3, padx=10, pady=5, sticky="ewns")

        theme_folder_button = ttk.Button(
            self.pixel_set,
            text="Theme Folder",
            image=self.folder_icon,
            compound="left",
            command=open_theme_folder,
            width=20
        )
        theme_folder_button.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        icon_folder_button = ttk.Button(
            self.pixel_set,
            text="Icon Folder",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20
        )
        icon_folder_button.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        cursor_folder_button = ttk.Button(
            self.pixel_set,
            text="Cursor Folder",
            compound="left",
            image=self.folder_icon,
            command=open_icon_folder,
            width=20
        )
        cursor_folder_button.grid(row=3, column=4, padx=10, pady=5, sticky="ew")



        info_button = tk.Button(
            self.pixel_set,
            text="Why is everthing DISABLED?",
            borderwidth=0,
            highlightthickness=0,
            background=ext_btn,
            foreground=ext_btn_font,
            command=why_message_0,
        )

        def install_papirus():
            # Add the functionality to be executed when the "Install Papirus + Folders" button is clicked
            print("Installing Papirus + Folders...")
            popen(
                "x-terminal-emulator -e 'bash -c \"wget -qO- https://git.io/papirus-icon-theme-install | sh && wget -qO- https://git.io/papirus-folders-install | sh; exec bash\"'"
            )
            self.install_button.config(state=DISABLED)

        def set_icon_theme():
            selected_theme = self.papirus_theme_combobox.get()
            selected_ver = self.papirus_version_combobox.get()
            if selected_theme != "Select a Color":
                print(f"Setting icon theme to: {selected_theme}")
                os.system(
                    f"{permit} papirus-folders -C {selected_theme} --theme {selected_ver}"
                )
                if get_desktop_environment() == "xfce":
                    subprocess.run(
                        [
                            "xfconf-query",
                            "-c",
                            "xsettings",
                            "-p",
                            "/Net/IconThemeName",
                            "-s",
                            selected_ver,
                        ]
                    )
                elif get_desktop_environment() == "lxde-pi" or "lxde":
                    update_lxde_icons_config(selected_ver)
                else:
                    subprocess.run(
                        [
                            "gsettings",
                            "set",
                            "org.gnome.desktop.interface",
                            "icon-theme",
                            selected_ver,
                        ]
                    )
            else:
                print("Please select a valid icon theme.")
            done_message_0()

