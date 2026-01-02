import gi
from gi.repository import Gtk, GdkPixbuf, GLib, Gio


import gi
import os
import importlib
from gi.repository import Gtk, GdkPixbuf, GLib, Gio
from tabs import software_dict_lib
from software import InstallableAppFactory
from cache import Cache





# Mapping Kategorie -> (dict, Titel)
CATEGORIES = [
    (software_dict_lib.SoftwareCommunication.com_dict, "Web & Chat"),
    (software_dict_lib.SoftwareOffice.office_dict, "Büro"),
    (software_dict_lib.SoftwareAudioVideo.av_dict, "Audio & Video"),
    (software_dict_lib.SoftwareImageEditing.img_dict, "Bildbearbeitung"),
    (software_dict_lib.SoftwareGamingTools.game_tool_dict, "Gaming Tools"),
    (software_dict_lib.SoftwareGame.game_dict, "Native Games"),
    (software_dict_lib.SoftwareBackup.bak_dict, "Backup"),
    (software_dict_lib.SoftwareSafty.saf_dict, "Sicherheit"),
    (software_dict_lib.SoftwareDesktopTools.desk_dict, "Desktop Tools"),
    (software_dict_lib.SoftwareTerminalTools.term_dict, "Terminal Tools"),
    (software_dict_lib.SoftwareGuideOSTools.guideos_dict, "GuideOS Tools"),
]

class SoftwareTab(Gtk.Box):

    def _refresh_current_category(self):
        # Aktuelles Tab neu bauen
        page_num = self.notebook.get_current_page()
        if page_num < 0:
            return
        cat_dict, cat_title = CATEGORIES[page_num]
        new_page = self._create_category_page(cat_dict, cat_title)
        self.notebook.remove_page(page_num)
        self.notebook.insert_page(new_page, Gtk.Label(label=cat_title), page_num)
        self.notebook.set_current_page(page_num)
        # Lösche Installationsstatus-Cache wie im Original
        Cache.delete("installed_apt_pkgs")
        Cache.delete("flatpak_installs")

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)

        # Info-Box für Beschreibung (global für alle Kategorien)
        self.info_frame = Gtk.Frame()
        self.info_frame.set_margin_top(8)
        self.info_frame.set_margin_bottom(8)
        self.info_frame.set_margin_start(8)
        self.info_frame.set_margin_end(8)
        self.info_frame.set_hexpand(True)
        self.info_frame.set_vexpand(False)
        # Feste Höhe für die Info-Box (z.B. 80px)
        self.info_frame.set_size_request(-1, 80)
        self.info_label = Gtk.Label(label="", xalign=0)
        self.info_label.set_wrap(True)
        self.info_label.set_max_width_chars(80)
        self.info_label.set_margin_top(8)
        self.info_label.set_margin_bottom(8)
        self.info_label.set_margin_start(12)
        self.info_label.set_margin_end(12)
        self.info_frame.set_child(self.info_label)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.append(self.notebook)
        self.append(self.info_frame)

        # Detailansicht vorbereiten (zunächst versteckt)
        self.detail_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.detail_box.set_margin_top(20)
        self.detail_box.set_margin_bottom(20)
        self.detail_box.set_margin_start(20)
        self.detail_box.set_margin_end(20)
        self.detail_box.set_hexpand(True)
        self.detail_box.set_vexpand(True)
        self.detail_box.set_visible(False)
        self.detail_box.set_size_request(900, -1)  # Mindestbreite für Detailansicht
        self.append(self.detail_box)

        # Zurück-Button
        self.back_btn = Gtk.Button(label="Zurück")
        self.back_btn.set_size_request(120, 40)
        self.back_btn.set_halign(Gtk.Align.START)
        self.back_btn.connect("clicked", self._on_back_clicked)
        self.detail_box.append(self.back_btn)

        for cat_dict, cat_title in CATEGORIES:
            page = self._create_category_page(cat_dict, cat_title)
            self.notebook.append_page(page, Gtk.Label(label=cat_title))

    def _create_category_page(self, cat_dict, cat_title):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        scrolled.set_child(vbox)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        def on_tile_hover(app, enter):
            if enter:
                self.info_label.set_text(app.get_description())
            else:
                self.info_label.set_text("")

        for key, info in cat_dict.items():
            app = InstallableAppFactory.create(
                type=info["Package"],
                name=info["Name"],
                icon=info["Icon"],
                description=info["Description"],
                path=info["Path"],
                thumbnail=info["Thumbnail"],
                install_command=info["Install"],
                uninstall_command=info["Uninstall"],
            )
            tile = self._create_app_frame(app, lambda a=app: on_tile_hover(a, True), lambda a=app: on_tile_hover(a, False))
            vbox.append(tile)
        return scrolled

    def _create_app_frame(self, app, on_enter, on_leave):
        frame = Gtk.Frame()
        frame.set_hexpand(True)
        frame.set_margin_top(2)
        frame.set_margin_bottom(2)
        frame.set_margin_start(2)
        frame.set_margin_end(2)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(6)
        hbox.set_margin_bottom(6)
        hbox.set_margin_start(8)
        hbox.set_margin_end(8)

        # Linke Seite: Icon und Name
        try:
            base_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(app.get_icon(), 48, 48)
            icon = Gtk.Picture.new_for_pixbuf(base_pixbuf)
            icon.set_keep_aspect_ratio(True)
            icon.set_content_fit(Gtk.ContentFit.CONTAIN)
            icon.set_halign(Gtk.Align.CENTER)
            icon.set_valign(Gtk.Align.CENTER)
            hbox.append(icon)
        except Exception as e:
            print(f"[DEBUG] Fehler beim Erstellen des App-Icons: {e}")
            hbox.append(Gtk.Picture())

        name = Gtk.Label(label=app.get_name())
        name.set_markup(f'<b>{app.get_name()}</b>')
        name.set_halign(Gtk.Align.START)
        name.set_valign(Gtk.Align.CENTER)
        name.set_max_width_chars(18)
        name.set_ellipsize(3)
        hbox.append(name)

        # Expander für rechtsbündige Ausrichtung
        expander = Gtk.Box()
        expander.set_hexpand(True)
        hbox.append(expander)

        # Rechte Seite: Status, Info-Button, Haken
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        right_box.set_halign(Gtk.Align.END)
        right_box.set_valign(Gtk.Align.CENTER)

        status_label = Gtk.Label()
        if app.is_installed():
            status_label.set_text("Installiert")
            status_label.set_halign(Gtk.Align.END)
            status_label.set_valign(Gtk.Align.CENTER)
            status_label.get_style_context().add_class("success")
        else:
            status_label.set_text("Nicht installiert")
            status_label.set_halign(Gtk.Align.END)
            status_label.set_valign(Gtk.Align.CENTER)
            status_label.get_style_context().add_class("warning")
        right_box.append(status_label)

        info_btn = Gtk.Button(label="Mehr")
        info_btn.set_size_request(60, 32)
        info_btn.set_halign(Gtk.Align.END)
        info_btn.set_valign(Gtk.Align.CENTER)
        info_btn.connect("clicked", lambda *_: self._show_app_details(app))
        right_box.append(info_btn)

        if app.is_installed():
            try:
                check_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../images/icons/pigro_icons/ok_16x16.png"))
                if os.path.exists(check_path):
                    check_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(check_path, 20, 20)
                    check_icon = Gtk.Picture.new_for_pixbuf(check_pixbuf)
                    check_icon.set_halign(Gtk.Align.END)
                    check_icon.set_valign(Gtk.Align.CENTER)
                    right_box.append(check_icon)
            except Exception as e:
                print(f"[DEBUG] Fehler beim Haken-Icon: {e}")

        hbox.append(right_box)

        # Hover-Events für Beschreibung
        enter_ctrl = Gtk.EventControllerMotion()
        enter_ctrl.connect("enter", lambda *_: on_enter(app))
        enter_ctrl.connect("leave", lambda *_: on_leave(app))
        frame.add_controller(enter_ctrl)
        frame.set_child(hbox)
        return frame

    def _make_click_controller(self, callback):
        ctrl = Gtk.GestureClick()
        ctrl.connect("released", lambda gesture, n_press, x, y: callback())
        return ctrl

    def _show_app_details(self, app):
        # Detailansicht im Hauptfenster anzeigen
        self.notebook.set_visible(False)
        self.info_frame.set_visible(False)
        self.detail_box.set_visible(True)

        # Vorherige Detail-Widgets entfernen (außer Zurück-Button)
        child = self.detail_box.get_first_child()
        if child:
            child = child.get_next_sibling()
        while child:
            next_child = child.get_next_sibling()
            self.detail_box.remove(child)
            child = next_child

        # Oberer Bereich: Icon, Name, Typ, Button
        top_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        top_hbox.set_hexpand(True)
        top_hbox.set_halign(Gtk.Align.FILL)

        # Icon (wie bei App-Tiles: Pixbuf mit fester Größe, robust gegen Fehler)
        print(f"[DEBUG] Detailansicht Icon-Pfad: {app.get_icon()}")
        if app.get_icon() and os.path.exists(app.get_icon()):
            try:
                from gi.repository import GdkPixbuf
                print(f"[DEBUG] Icon existiert: {app.get_icon()}")
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(app.get_icon(), 64, 64)
                icon_picture = Gtk.Picture.new_for_pixbuf(pixbuf)
                icon_picture.set_keep_aspect_ratio(True)
                icon_picture.set_content_fit(Gtk.ContentFit.CONTAIN)
                icon_picture.set_halign(Gtk.Align.CENTER)
                icon_picture.set_valign(Gtk.Align.CENTER)
                top_hbox.append(icon_picture)
            except Exception as e:
                print(f"[DEBUG] Fehler beim Icon-Laden: {e}")
                icon_picture = Gtk.Picture()
                icon_picture.set_size_request(64, 64)
                icon_picture.set_halign(Gtk.Align.CENTER)
                icon_picture.set_valign(Gtk.Align.CENTER)
                top_hbox.append(icon_picture)
        else:
            print(f"[DEBUG] Icon existiert NICHT: {app.get_icon()}")
            # Fallback falls kein Icon vorhanden
            icon_picture = Gtk.Picture()
            icon_picture.set_size_request(64, 64)
            icon_picture.set_halign(Gtk.Align.CENTER)
            icon_picture.set_valign(Gtk.Align.CENTER)
            top_hbox.append(icon_picture)

        # Name und Typ (vertikal)
        name_typ_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        name = Gtk.Label(label=app.get_name())
        name.set_markup(f'<span size="18000" weight="bold">{app.get_name()}</span>')
        name.set_halign(Gtk.Align.START)
        name.set_valign(Gtk.Align.CENTER)
        typ = Gtk.Label()
        typ.set_markup(f'<span foreground="#3399ff" weight="bold">{app.get_type()}</span>')
        typ.set_halign(Gtk.Align.START)
        typ.set_valign(Gtk.Align.CENTER)
        name_typ_box.append(name)
        name_typ_box.append(typ)
        top_hbox.append(name_typ_box)

        # Expander für rechtsbündige Ausrichtung
        expander = Gtk.Box()
        expander.set_hexpand(True)
        top_hbox.append(expander)

        # Install/Deinstall-Button
        self.detail_btn = Gtk.Button()
        self.detail_btn.set_size_request(120, 40)
        self._update_button(self.detail_btn, app)
        self.detail_btn.connect("clicked", self._on_install_clicked_with_progress, app, self.detail_btn)
        self.detail_btn.set_halign(Gtk.Align.END)
        self.detail_btn.set_valign(Gtk.Align.CENTER)
        top_hbox.append(self.detail_btn)
        # ProgressBar direkt unter dem Button
        vbox_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox_top.append(top_hbox)
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_show_text(True)
        self.progressbar.set_visible(False)
        vbox_top.append(self.progressbar)
        self.detail_box.append(vbox_top)
        # Beschreibung
        desc = Gtk.Label(label=app.get_description())
        desc.set_wrap(True)
        desc.set_max_width_chars(60)
        desc.set_halign(Gtk.Align.FILL)
        self.detail_box.append(desc)
        # Optional: Screenshot/Thumbnail als skaliertes Bild (700px Breite, wie im Original)
        if app.get_thumbnail() and os.path.exists(app.get_thumbnail()):
            try:
                from gi.repository import GdkPixbuf
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(app.get_thumbnail())
                width = 600
                scale = width / pixbuf.get_width() if pixbuf.get_width() > 0 else 1.0
                height = int(pixbuf.get_height() * scale)
                scaled_pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
                picture = Gtk.Picture.new_for_pixbuf(scaled_pixbuf)
                picture.set_keep_aspect_ratio(True)
                picture.set_can_shrink(False)
                scrolled_window = Gtk.ScrolledWindow()
                scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
                scrolled_window.set_child(picture)
                scrolled_window.set_halign(Gtk.Align.FILL)
                scrolled_window.set_hexpand(True)
                scrolled_window.set_vexpand(True)
                scrolled_window.set_min_content_width(700)
                scrolled_window.set_min_content_height(180)
                self.detail_box.append(scrolled_window)
            except Exception as e:
                print(f"[DEBUG] Fehler beim Thumbnail: {e}")

    def _on_install_clicked_with_progress(self, button, app, btn):
        # Zeige Progressbar
        if hasattr(self, 'progressbar'):
            self.progressbar.set_visible(True)
            self.progressbar.set_fraction(0.0)
            self.progressbar.set_text("Installation läuft ..." if not app.is_installed() else "Deinstallation läuft ...")
        def progress_pulse():
            if hasattr(self, 'progressbar') and self.progressbar.get_visible():
                self.progressbar.pulse()
                return True
            return False
        self._progress_pulse_id = GLib.timeout_add(100, progress_pulse)
        def on_done():
            if hasattr(self, 'progressbar'):
                self.progressbar.set_fraction(1.0)
                self.progressbar.set_text("Fertig!")
                GLib.timeout_add(1000, lambda: self.progressbar.set_visible(False))
            if hasattr(self, '_progress_pulse_id') and self._progress_pulse_id:
                try:
                    GLib.source_remove(self._progress_pulse_id)
                    self._progress_pulse_id = None
                except:
                    pass  # Source wurde bereits entfernt
            # App-Objekt neu erzeugen, damit is_installed() den aktuellen Status liefert
            from tabs import software_dict_lib
            info = None
            # Finde das Info-Objekt für die aktuelle App anhand des Namens
            for cat_dict, _ in CATEGORIES:
                for key, i in cat_dict.items():
                    if i["Name"] == app.get_name():
                        info = i
                        break
                if info:
                    break
            if info:
                from software import InstallableAppFactory
                new_app = InstallableAppFactory.create(
                    type=info["Package"],
                    name=info["Name"],
                    icon=info["Icon"],
                    description=info["Description"],
                    path=info["Path"],
                    thumbnail=info["Thumbnail"],
                    install_command=info["Install"],
                    uninstall_command=info["Uninstall"],
                )
                # Button im Detailbereich explizit aktualisieren wie im Original
                if hasattr(self, 'detail_btn'):
                    self._update_button(self.detail_btn, new_app)
                    # Signal neu setzen, damit die Aktion stimmt
                    for handler_id in getattr(self, '_detail_btn_handler_ids', []):
                        self.detail_btn.disconnect(handler_id)
                    self._detail_btn_handler_ids = [
                        self.detail_btn.connect("clicked", self._on_install_clicked_with_progress, new_app, self.detail_btn)
                    ]
            self._refresh_current_category()
        if app.is_installed():
            self._run_command(app.get_uninstall_command(), on_done)
        else:
            self._run_command(app.get_install_command(), on_done)

    def _on_back_clicked(self, button):
        self.detail_box.set_visible(False)
        self.notebook.set_visible(True)
        self.info_frame.set_visible(True)

    def _create_app_row(self, app):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        # ...existing code...
        # Install/Deinstall-Button
        btn = Gtk.Button()
        btn.set_size_request(120, 40)
        self._update_button(btn, app)
        btn.connect("clicked", self._on_install_clicked, app, btn)
        row.append(btn)
        return row

    def _update_button(self, btn, app):
        if app.is_installed():
            btn.set_label("Deinstallieren")
            btn.get_style_context().add_class("destructive-action")
        else:
            btn.set_label("Installieren")
            btn.get_style_context().remove_class("destructive-action")

    def _on_install_clicked(self, button, app, btn):
        if app.is_installed():
            self._run_command(app.get_uninstall_command(), self._refresh_current_category)
        else:
            self._run_command(app.get_install_command(), self._refresh_current_category)
        # Status sofort prüfen und UI updaten
        self._refresh_current_category()

    def _run_command(self, command, callback):
        import subprocess
        import threading
        def worker():
            try:
                # Start the process and wait for it to finish
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.communicate()
            except Exception as e:
                print(f"[DEBUG] Fehler beim Ausführen des Kommandos: {e}")
            GLib.idle_add(callback)
        threading.Thread(target=worker, daemon=True).start()
