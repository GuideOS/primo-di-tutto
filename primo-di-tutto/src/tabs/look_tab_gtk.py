import gi
import os
import subprocess
import json
gi.require_version("Adap", "1")
from gi.repository import Gtk, GdkPixbuf, GLib
from gi.repository import Adap as Adw
from resorcess import application_path

class LookTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Layout-Vorlagen
        layout_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("preferences-desktop-theme")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Layout-Vorlagen")
        label_box.append(label)
        layout_frame.set_label_widget(label_box)
        layout_frame.set_margin_bottom(4)
        self.append(layout_frame)
        layout_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        layout_box.set_margin_top(12)
        layout_box.set_margin_bottom(12)
        layout_box.set_margin_start(12)
        layout_box.set_margin_end(12)
        layout_frame.set_child(layout_box)

        layout_label = Gtk.Label(label="Wähle ein Layout aus und passe es an. Du kannst ein Backup davon erstellen und es zu einem späteren Zeitpunkt wiederherstellen.")
        layout_label.set_wrap(True)
        layout_label.set_xalign(0)
        layout_box.append(layout_label)

        grid = Gtk.Grid()
        grid.set_column_spacing(16)
        grid.set_row_spacing(8)
        layout_box.append(grid)

        # Thumbnails (placeholder icons for now)
        thumb_size = 128

        # Layout-Buttons mit dynamischer Icon-Umschaltung
        self.layout_buttons = []
        self.layout_labels = ["Standard", "Spiegel", "11", "Ubuntu-Like"]
        self.layout_icon_basenames = ["classico_thumb", "upside_thumb", "elfi_thumb", "devil_thumb"]
        self.layout_callbacks = [self.set_classico_panel, self.set_upside_down_panel, self.set_elfi_panel, self.set_der_teufel_panel]
        for i in range(4):
            btn = Gtk.Button()
            btn.set_hexpand(True)
            btn.set_vexpand(True)
            btn.connect("clicked", self.layout_callbacks[i])
            self.layout_buttons.append(btn)
            grid.attach(btn, i, 0, 1, 1)
            lbl = Gtk.Label(label=self.layout_labels[i])
            lbl.set_xalign(0.5)
            grid.attach(lbl, i, 1, 1, 1)
        self.update_layout_icons()

        # Mein Layout sichern/laden
        backup_btn = Gtk.Button(label="Mein Layout sichern/laden")
        backup_btn.set_margin_top(8)
        backup_btn.connect("clicked", self.start_restore_my_cinnamon)
        layout_box.append(backup_btn)

        # Theme selection
        theme_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        theme_icon = Gtk.Image.new_from_icon_name("preferences-desktop-theme")
        theme_icon.set_pixel_size(24)
        label_box.append(theme_icon)
        theme_label = Gtk.Label(label="Desktop-Theme")
        label_box.append(theme_label)
        theme_frame.set_label_widget(label_box)
        theme_frame.set_margin_bottom(8)
        self.append(theme_frame)
        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        theme_box.set_margin_top(16)
        theme_box.set_margin_bottom(16)
        theme_box.set_margin_start(16)
        theme_box.set_margin_end(16)
        theme_frame.set_child(theme_box)
        self.theme_combo = Gtk.ComboBoxText()
        self.theme_combo.set_hexpand(True)
        theme_box.append(self.theme_combo)
        theme_apply = Gtk.Button(label="Theme anwenden")
        theme_apply.set_size_request(180, -1)
        theme_apply.connect("clicked", self.set_theme)
        theme_box.append(theme_apply)
        theme_folder = Gtk.Button(label="Theme-Ordner")
        theme_folder.set_size_request(150, -1)
        theme_folder.connect("clicked", self.open_theme_folder)
        theme_box.append(theme_folder)

        # Icon selection
        icon_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon_icon = Gtk.Image.new_from_icon_name("preferences-desktop-icons")
        icon_icon.set_pixel_size(24)
        label_box.append(icon_icon)
        icon_label = Gtk.Label(label="Symbole")
        label_box.append(icon_label)
        icon_frame.set_label_widget(label_box)
        icon_frame.set_margin_bottom(8)
        self.append(icon_frame)
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon_box.set_margin_top(16)
        icon_box.set_margin_bottom(16)
        icon_box.set_margin_start(16)
        icon_box.set_margin_end(16)
        icon_frame.set_child(icon_box)
        self.icon_combo = Gtk.ComboBoxText()
        self.icon_combo.set_hexpand(True)
        icon_box.append(self.icon_combo)
        icon_apply = Gtk.Button(label="Symbole anwenden")
        icon_apply.set_size_request(180, -1)
        icon_apply.connect("clicked", self.set_icon)
        icon_box.append(icon_apply)
        icon_folder = Gtk.Button(label="Symbol-Ordner")
        icon_folder.set_size_request(150, -1)
        icon_folder.connect("clicked", self.open_icon_folder)
        icon_box.append(icon_folder)

        # Cursor selection
        cursor_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        cursor_icon = Gtk.Image.new_from_icon_name("input-mouse")
        cursor_icon.set_pixel_size(24)
        label_box.append(cursor_icon)
        cursor_label = Gtk.Label(label="Cursor")
        label_box.append(cursor_label)
        cursor_frame.set_label_widget(label_box)
        self.append(cursor_frame)
        cursor_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cursor_vbox.set_margin_top(16)
        cursor_vbox.set_margin_bottom(16)
        cursor_vbox.set_margin_start(16)
        cursor_vbox.set_margin_end(16)
        cursor_frame.set_child(cursor_vbox)
        
        # Cursor theme row
        cursor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cursor_vbox.append(cursor_box)
        self.cursor_combo = Gtk.ComboBoxText()
        self.cursor_combo.set_hexpand(True)
        cursor_box.append(self.cursor_combo)
        cursor_apply = Gtk.Button(label="Cursor anwenden")
        cursor_apply.set_size_request(180, -1)
        cursor_apply.connect("clicked", self.set_cursor)
        cursor_box.append(cursor_apply)
        cursor_folder = Gtk.Button(label="Cursor-Ordner")
        cursor_folder.set_size_request(150, -1)
        cursor_folder.connect("clicked", self.open_icon_folder)
        cursor_box.append(cursor_folder)
        
        # Cursor size row
        cursor_size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cursor_vbox.append(cursor_size_box)
        self.cursor_size_combo = Gtk.ComboBoxText()
        self.cursor_size_combo.set_hexpand(True)
        for size in ["16", "24", "32", "48", "64", "96", "128"]:
            self.cursor_size_combo.append_text(size)
        cursor_size_box.append(self.cursor_size_combo)
        cursor_size_apply = Gtk.Button(label="Cursorgröße anwenden")
        cursor_size_apply.set_size_request(338, -1)
        cursor_size_apply.connect("clicked", self.apply_cursor_size)
        cursor_size_box.append(cursor_size_apply)

        # Index aktualisieren
        refresh_btn = Gtk.Button(label="Index aktualisieren")
        refresh_btn.set_margin_top(8)
        refresh_btn.connect("clicked", self.update_theme_combobox)
        self.append(refresh_btn)

        self.update_theme_combobox()

    def load_thumb(self, path):
        thumb_size = 200
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, thumb_size, thumb_size, True)
            return Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception:
            return Gtk.Image.new_from_icon_name("applications-system")

    def update_layout_icons(self):
        import subprocess
        try:
            theme = subprocess.run([
                "gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"
            ], capture_output=True, text=True, check=True).stdout.strip().strip("'\"")
        except Exception:
            theme = ""
        is_dark = "dark" in theme.lower()
        variant = "dark" if is_dark else "light"
        for i, btn in enumerate(self.layout_buttons):
            icon_file = f"{application_path}/images/icons/pigro_icons/{self.layout_icon_basenames[i]}_{variant}.svg"
            img = self.load_thumb(icon_file)
            btn.set_child(img)

    # --- Callbacks and logic ---
    def set_classico_panel(self, btn):
        # Classico-Layout anwenden
        self._killall("plank")
        self._check_plank_autostart()
        subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"])
        self._copy_guide_menu(application_path)
        config_path = os.path.expanduser("~/.config/cinnamon/spices/transparent-panels@germanfr/transparent-panels@germanfr.json")
        try:
            import json
            with open(config_path, "r") as file:
                config = json.load(file)
            config["transparency-type"]["value"] = "panel-semi-transparent"
            config["panel-top"]["value"] = True
            config["panel-bottom"]["value"] = False
            config["panel-left"]["value"] = False
            config["panel-right"]["value"] = False
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Fehler beim Schreiben von transparent-panels: {e}")
        opacify_config_path = os.path.expanduser("~/.config/cinnamon/spices/opacify@anish.org/opacify@anish.org.json")
        try:
            with open(opacify_config_path, "r") as opacify_file:
                opacify_config = json.load(opacify_file)
            opacify_config["opacity"]["value"] = "240"
            with open(opacify_config_path, "w") as opacify_file:
                json.dump(opacify_config, opacify_file, indent=4)
        except Exception as e:
            print(f"Fehler beim Schreiben von opacify: {e}")
        subprocess.run(f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_classico", shell=True, check=True)
        calendar_bak = f"{application_path}/scripts/calendar@cinnamon.org.json"
        calendar_path = os.path.expanduser("~/.config/cinnamon/spices/calendar@cinnamon.org/66.json")
        self._copy_file(calendar_bak, calendar_path)
        grouped_win = os.path.expanduser("~/.config/cinnamon/spices/grouped-window-list@cinnamon.org")
        self._restore_cinnamon_config(69, grouped_win)
        workspace_bak = f"{application_path}/scripts/67.json"
        workspace_path = os.path.expanduser("~/.config/cinnamon/spices/workspace-switcher@cinnamon.org/67.json")
        self._copy_file(workspace_bak, workspace_path)
        menu_bak = f"{application_path}/scripts/0.json"
        menu_path = os.path.expanduser("~/.config/cinnamon/spices/menu@cinnamon.org/0.json")
        self._copy_file(menu_bak, menu_path)

    def set_upside_down_panel(self, btn):
        self._check_plank_autostart()
        self._killall("plank")
        subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"])
        subprocess.run(f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_spiegel", shell=True, check=True)
        source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
        destination_path = os.path.expanduser("~/.config/cinnamon/spices/calendar@cinnamon.org/13.json")
        self._copy_file(source_path, destination_path)
        grouped_win = os.path.expanduser("~/.config/cinnamon/spices/grouped-window-list@cinnamon.org")
        self._restore_cinnamon_config(69, grouped_win)
        menu_bak = f"{application_path}/scripts/0.json"
        menu_path = os.path.expanduser("~/.config/cinnamon/spices/menu@cinnamon.org/0.json")
        self._copy_file(menu_bak, menu_path)

    def set_elfi_panel(self, btn):
        self._killall("plank")
        self._check_plank_autostart()
        self._copy_guide_menu(application_path)
        subprocess.run(f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_elf", shell=True, check=True)
        calendar_bak = f"{application_path}/scripts/calendar@cinnamon.org.json"
        calendar_path = os.path.expanduser("~/.config/cinnamon/spices/calendar@cinnamon.org/13.json")
        self._copy_file(calendar_bak, calendar_path)
        grouped_win = os.path.expanduser("~/.config/cinnamon/spices/grouped-window-list@cinnamon.org")
        self._restore_cinnamon_config(69, grouped_win)
        self._create_cinnamenu_conf(application_path)

    def set_der_teufel_panel(self, btn):
        subprocess.Popen(["plank"])
        subprocess.run(["gsettings", "set", "org.cinnamon", "enabled-extensions", "[]"])
        subprocess.run(f"dconf load /org/cinnamon/ < {application_path}/scripts/cinnamon_desktop_ubuntu", shell=True, check=True)
        source_path = f"{application_path}/scripts/calendar@cinnamon.org.json"
        destination_path = os.path.expanduser("~/.config/cinnamon/spices/calendar@cinnamon.org/20.json")
        self._copy_file(source_path, destination_path)
        self._plank_values(application_path)
        self._copy_dockitems(application_path)

    # Hilfsfunktionen
    def _killall(self, proc):
        subprocess.run(["killall", proc])

    def _check_plank_autostart(self):
        path = os.path.expanduser("~/.config/autostart/plank.desktop")
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Fehler beim Löschen von {path}: {e}")

    def _copy_guide_menu(self, application_path):
        source_file = f"{application_path}/scripts/guide_menu.json"
        destination_directory = os.path.expanduser("~/.config/cinnamon/spices/menu@cinnamon.org")
        destination_file = os.path.join(destination_directory, "0.json")
        os.makedirs(destination_directory, exist_ok=True)
        try:
            with open(source_file, "r") as src:
                content = src.read()
            with open(destination_file, "w") as dst:
                dst.write(content)
        except Exception as e:
            print(f"Fehler beim Kopieren von guide_menu.json: {e}")

    def _copy_file(self, source, destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        try:
            import shutil
            shutil.copy2(source, destination)
        except Exception as e:
            print(f"Fehler beim Kopieren von {source}: {e}")

    def _restore_cinnamon_config(self, file_number, c_dir):
        config_dir = os.path.expanduser(c_dir)
        backup_file_path = os.path.join(config_dir, "69.bak")
        if not os.path.exists(backup_file_path):
            print(f"Backup {backup_file_path} nicht gefunden.")
            return
        restored_file_name = f"{file_number}.json"
        restored_file_path = os.path.join(config_dir, restored_file_name)
        try:
            import shutil
            shutil.copy(backup_file_path, restored_file_path)
        except Exception as e:
            print(f"Fehler beim Wiederherstellen von {backup_file_path}: {e}")

    def _create_cinnamenu_conf(self, application_path):
        """
        Kopiert die Datei 68.json vom application_path/scripts-Pfad
        zum Zielpfad des Nutzers ~/.config/cinnamon/spices/Cinnamenu@json/68.json
        """
        source_path = os.path.join(application_path, "scripts", "68.json")
        target_dir = os.path.expanduser("~/.config/cinnamon/spices/Cinnamenu@json")
        target_path = os.path.join(target_dir, "68.json")
        
        os.makedirs(target_dir, exist_ok=True)
        
        try:
            import shutil
            shutil.copy(source_path, target_path)
            print(f"Datei wurde erfolgreich nach {target_path} kopiert.")
        except FileNotFoundError:
            print(f"Die Datei {source_path} wurde nicht gefunden.")
        except PermissionError:
            print(f"Zugriffsrechte fehlen, um die Datei zu kopieren.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

    def _plank_values(self, application_path):
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
            except Exception as e:
                print(f"Fehler beim Schreiben von dconf {path}: {e}")
        source_path = f"{application_path}/scripts/plank.desktop"
        destination_path = os.path.expanduser("~/.config/autostart/plank.desktop")
        self._copy_file(source_path, destination_path)

    def _copy_dockitems(self, application_path):
        src = f"{application_path}/scripts/"
        dest = os.path.expanduser("~/.config/plank/dock1/launchers")
        if not os.path.exists(src):
            print(f"Quellverzeichnis {src} existiert nicht.")
            return
        os.makedirs(dest, exist_ok=True)
        for file_name in os.listdir(src):
            if file_name.endswith(".dockitem"):
                src_file = os.path.join(src, file_name)
                dest_file = os.path.join(dest, file_name)
                try:
                    import shutil
                    shutil.copy2(src_file, dest_file)
                except Exception as e:
                    print(f"Fehler beim Kopieren von {src_file}: {e}")
    
    def start_restore_my_cinnamon(self, btn):
        subprocess.Popen(["guideos-layout-sicherung"])
    
    def set_theme(self, btn):
        selected_theme = self.theme_combo.get_active_text()
        if not selected_theme or selected_theme == "Bitte aktualisieren":
            return
        settings_keys = [
            ("org.cinnamon.desktop.wm.preferences", "theme"),
            ("org.cinnamon.desktop.interface", "gtk-theme"),
            ("org.cinnamon.theme", "name"),
        ]
        for schema, key in settings_keys:
            subprocess.run(["gsettings", "set", schema, key, selected_theme], check=True)
        # Dark/Light detection
        if "dark" in selected_theme.lower():
            subprocess.run(["dconf", "write", "/org/gnome/desktop/interface/color-scheme", "'prefer-dark'"], check=True)
        else:
            subprocess.run(["dconf", "write", "/org/gnome/desktop/interface/color-scheme", "'prefer-light'"], check=True)
        self.update_theme_combobox()
        self.update_layout_icons()
        self.show_confirmation_dialog("Theme angewendet", f"Das Theme '{selected_theme}' wurde erfolgreich angewendet.")

    def set_icon(self, btn):
        selected_icon = self.icon_combo.get_active_text()
        if not selected_icon or selected_icon == "Bitte aktualisieren":
            return
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "icon-theme", selected_icon], check=True)
        self.update_theme_combobox()
        self.show_confirmation_dialog("Icons angewendet", f"Das Icon-Theme '{selected_icon}' wurde erfolgreich angewendet.")

    def set_cursor(self, btn):
        selected_cursor = self.cursor_combo.get_active_text()
        if not selected_cursor or selected_cursor == "Bitte aktualisieren":
            return
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "cursor-theme", selected_cursor], check=True)
        self.update_theme_combobox()
        self.show_confirmation_dialog("Cursor angewendet", f"Das Cursor-Theme '{selected_cursor}' wurde erfolgreich angewendet.")

    def apply_cursor_size(self, btn):
        selected_size = self.cursor_size_combo.get_active_text()
        if not selected_size or not selected_size.isdigit():
            return
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "cursor-size", selected_size], check=True)
        self.update_theme_combobox()
        self.show_confirmation_dialog("Cursorgröße angewendet", f"Die Cursorgröße '{selected_size}' wurde erfolgreich angewendet.")

    def show_confirmation_dialog(self, title, message):
        dialog = Adw.AlertDialog.new(title, message)
        dialog.add_response("ok", "OK")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("ok")
        dialog.present(self.get_root())

    def open_theme_folder(self, btn):
        subprocess.Popen(["pkexec", "nemo", "/usr/share/themes"])

    def open_icon_folder(self, btn):
        subprocess.Popen(["pkexec", "nemo", "/usr/share/icons"])

    def update_theme_combobox(self, btn=None):
        import os
        self.theme_combo.remove_all()
        self.icon_combo.remove_all()
        self.cursor_combo.remove_all()
        # Themes
        try:
            themes = [d for d in os.listdir("/usr/share/themes") if os.path.isdir(os.path.join("/usr/share/themes", d))]
            themes.sort()
            # Filter wie im Original
            blacklist = [
                "BlackMATE", "BlueMenta", "Blue-Submarine", "Clearlooks", "ContrastHigh", "Crux", "Default", "Emacs", "GreenLaguna", "Green-Submarine", "HighContrast", "HighContrastInverse", "Industrial", "Menta", "Raleigh", "Redmond", "Shiny", "ThinIce", "TraditionalGreen", "TraditionalOk", "WhiteSur-Dark", "WhiteSur-Dark-hdpi", "WhiteSur-Dark-solid-hdpi", "WhiteSur-Dark-solid-xhdpi", "WhiteSur-Dark-xhdpi", "WhiteSur-Light", "WhiteSur-Light-hdpi", "WhiteSur-Light-solid-hdpi", "WhiteSur-Light-solid-xhdpi", "WhiteSur-Light-xhdpi", "YaruOk", "Yaru-xhdpi", "Yaru", "YaruGreen", "Yaru-dark-hdpi", "Yaru-dark-xhdpi", "Yaru-hdpi", "Yaru-xhdpi", "Mist"
            ]
            themes = [x for x in themes if x not in blacklist]
            for t in themes:
                self.theme_combo.append_text(t)
        except Exception as e:
            self.theme_combo.append_text(f"Error: {e}")
        # Aktuelles Theme
        try:
            current_theme = subprocess.run(["gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"], capture_output=True, text=True, check=True).stdout.strip().strip("'\"")
            if current_theme in themes:
                self.theme_combo.set_active(themes.index(current_theme))
            else:
                self.theme_combo.set_active(0)
        except Exception:
            self.theme_combo.set_active(0)
        # Icons
        try:
            icons = [d for d in os.listdir("/usr/share/icons") if os.path.isdir(os.path.join("/usr/share/icons", d)) and "cursors" not in os.listdir(os.path.join("/usr/share/icons", d))]
            icons.sort()
            icon_blacklist = ["ContrastHigh", "default", "desktop-base", "gnome", "hicolor", "HighContrast", "locolor", "mate", "mate-black", "menta", "mozc", "vendor", "zbar.ico"]
            icons = [x for x in icons if x not in icon_blacklist]
            for i in icons:
                self.icon_combo.append_text(i)
        except Exception as e:
            self.icon_combo.append_text(f"Error: {e}")
        # Aktuelles Icon
        try:
            current_icon = subprocess.run(["gsettings", "get", "org.cinnamon.desktop.interface", "icon-theme"], capture_output=True, text=True, check=True).stdout.strip().strip("'\"")
            if current_icon in icons:
                self.icon_combo.set_active(icons.index(current_icon))
            else:
                self.icon_combo.set_active(0)
        except Exception:
            self.icon_combo.set_active(0)
        # Cursor-Themes
        try:
            all_icons = [d for d in os.listdir("/usr/share/icons") if os.path.isdir(os.path.join("/usr/share/icons", d))]
            all_icons.sort()
            cursor_themes = [icon for icon in all_icons if "cursors" in os.listdir(os.path.join("/usr/share/icons", icon))]
            for c in cursor_themes:
                self.cursor_combo.append_text(c)
        except Exception as e:
            self.cursor_combo.append_text(f"Error: {e}")
        # Aktuelles Cursor-Theme
        try:
            current_cursor = subprocess.run(["gsettings", "get", "org.cinnamon.desktop.interface", "cursor-theme"], capture_output=True, text=True, check=True).stdout.strip().strip("'\"")
            if current_cursor in cursor_themes:
                self.cursor_combo.set_active(cursor_themes.index(current_cursor))
            else:
                self.cursor_combo.set_active(0)
        except Exception:
            self.cursor_combo.set_active(0)
        # Cursor-Größe
        try:
            current_cursor_size = subprocess.run(["gsettings", "get", "org.cinnamon.desktop.interface", "cursor-size"], capture_output=True, text=True, check=True).stdout.strip()
            sizes = ["16", "24", "32", "48", "64", "96", "128"]
            if current_cursor_size in sizes:
                self.cursor_size_combo.set_active(sizes.index(current_cursor_size))
            else:
                self.cursor_size_combo.set_active(2)
        except Exception:
            self.cursor_size_combo.set_active(2)
