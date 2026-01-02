import gi
import os
import subprocess
from datetime import datetime
gi.require_version("Adap", "1")
from gi.repository import Gtk, GLib
from gi.repository import Adap as Adw
from resorcess import application_path

class ExpertToolsTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.append(self.notebook)

        # Quellen-Tab
        self.source_panel = SourcePanel()
        self.notebook.append_page(self.source_panel, Gtk.Label(label="Quellen"))

        # Werkzeuge-Tab
        self.admin_panel = AdminPanel()
        self.notebook.append_page(self.admin_panel, Gtk.Label(label="Werkzeuge"))

        # APT-Werkzeuge-Tab
        self.apt_panel = AptToolsPanel()
        self.notebook.append_page(self.apt_panel, Gtk.Label(label="APT/Flatpak-Werkzeuge"))


class SourcePanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_hexpand(True)
        self.set_vexpand(True)
        frame = Gtk.Frame(label="Eingebundene Repositories")
        frame.set_margin_top(20)
        frame.set_margin_bottom(20)
        frame.set_margin_start(20)
        frame.set_margin_end(20)
        self.append(frame)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        frame.set_child(vbox)

        # TreeView für sources.list.d
        self.store = Gtk.ListStore(str)
        self.treeview = Gtk.TreeView(model=self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.treeview.append_column(column)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.treeview)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        vbox.append(scrolled)
        self._populate_sources()

        # Button zum Öffnen des Ordners
        self.edit_btn = Gtk.Button(label="Quellen bearbeiten (Nur für erfahrene Nutzer!)")
        self.edit_btn.set_margin_top(12)
        self.edit_btn.connect("clicked", self._open_sources_folder)
        vbox.append(self.edit_btn)

    def _populate_sources(self):
        self.store.clear()
        try:
            for file in os.listdir("/etc/apt/sources.list.d"):
                self.store.append([file])
        except Exception as e:
            self.store.append([f"Fehler: {e}"])

    def _open_sources_folder(self, button):
        subprocess.Popen(["pkexec", "nemo", "/etc/apt/sources.list.d"])


class AdminPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        from tabs.system_dict_lib import SoftwareSys

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        scroll.set_child(vbox)

        # Info-Label außerhalb der Scrollbox
        self.info_label = Gtk.Label(label="", wrap=True, xalign=0)
        self.info_label.set_margin_top(10)
        self.info_label.set_margin_bottom(10)
        self.info_label.set_margin_start(10)
        self.info_label.set_margin_end(10)
        self.append(self.info_label)

        def add_tile_grid(parent, title, items, on_click, on_hover, icon_name=None):
            frame = Gtk.Frame()
            if icon_name:
                label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                label_box.set_margin_start(8)
                icon = Gtk.Image.new_from_icon_name(icon_name)
                icon.set_pixel_size(24)
                label_box.append(icon)
                label = Gtk.Label(label=title)
                label_box.append(label)
                frame.set_label_widget(label_box)
            else:
                frame.set_label(title)
            frame.set_margin_bottom(10)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            box.set_margin_top(10)
            box.set_margin_bottom(10)
            box.set_margin_start(10)
            box.set_margin_end(10)
            frame.set_child(box)
            parent.append(frame)
            grid = Gtk.Grid()
            grid.set_column_spacing(24)
            grid.set_row_spacing(24)
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)
            box.append(grid)
            max_columns = 4
            for i, (key, info) in enumerate(items.items()):
                row = i // max_columns
                col = i % max_columns
                tile = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                tile.set_hexpand(True)
                # Icon
                icon_name = info.get("Icon", "dialog-information")
                icon = Gtk.Image.new_from_icon_name(icon_name)
                icon.set_pixel_size(48)
                tile.append(icon)
                # Text
                label = Gtk.Label(label=info["Name"], wrap=True, xalign=0.5)
                tile.append(label)
                # Button
                btn = Gtk.Button()
                btn.set_child(tile)
                btn.set_hexpand(True)
                btn.connect("clicked", lambda b, k=key: on_click(k))
                # Hover-Effekt mit EventControllerMotion
                motion = Gtk.EventControllerMotion()
                motion.connect("enter", lambda c, x, y, k=key: on_hover(k))
                motion.connect("leave", lambda c: self.on_leave())
                btn.add_controller(motion)
                grid.attach(btn, col, row, 1, 1)
            return frame

        # Werkzeuge
        def sys_btn_action(sys_key):
            command = SoftwareSys.sys_dict[sys_key]["Action"]
            os.popen(command)
        def on_hover_sys(key):
            self.info_label.set_label(SoftwareSys.sys_dict[key]["Description"])
        add_tile_grid(vbox, "Werkzeuge", SoftwareSys.sys_dict, sys_btn_action, on_hover_sys, "applications-utilities")

        # Info-Label ist jetzt außerhalb der Scrollbox

    def on_leave(self):
        self.info_label.set_label("")


class AptToolsPanel(Gtk.Box):

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_hexpand(True)
        self.set_vexpand(True)
        # Add extra margin only to the APT tools panel
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Hauptlayout: horizontal
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.append(hbox)

        # Linker Frame: Buttons
        btn_frame = Gtk.Frame(label="APT/Flatpak Tools")
        btn_frame.set_hexpand(False)
        btn_frame.set_vexpand(True)
        hbox.append(btn_frame)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        btn_box.set_margin_top(12)
        btn_box.set_margin_bottom(12)
        btn_box.set_margin_start(12)
        btn_box.set_margin_end(12)
        btn_frame.set_child(btn_box)

        # Rechter Frame: Terminalausgabe + Beenden
        term_frame = Gtk.Frame(label="Prozess-Ausgabe")
        term_frame.set_hexpand(True)
        term_frame.set_vexpand(True)
        hbox.append(term_frame)
        term_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        term_vbox.set_margin_top(12)
        term_vbox.set_margin_bottom(12)
        term_vbox.set_margin_start(12)
        term_vbox.set_margin_end(12)
        term_frame.set_child(term_vbox)

        # Terminal-Ausgabe
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_monospace(True)
        self.textbuffer = self.textview.get_buffer()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.textview)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        term_vbox.append(scrolled)

        # Beenden-Button
        self.quit_btn = Gtk.Button(label="Beenden")
        self.quit_btn.connect("clicked", self._show_quit_dialog)
        self.quit_btn.set_visible(False)  # Initial ausgeblendet
        term_vbox.append(self.quit_btn)

        # Button-Definitionen (Label, Shell-Command)
        commands = [
            ("Alles aktualisieren", f"pkexec {application_path}/scripts/all_up"),
            ("apt update", f"pkexec {application_path}/scripts/nala_update_wrap"),
            ("apt upgrade", f"pkexec {application_path}/scripts/nala_upgrade_wrap"),
            ("apt list --upgradable", f"{application_path}/scripts/apt_list_upgradeble_wrap"),
            ("apt autoremove", f"pkexec {application_path}/scripts/nala_autopurge_wrap"),
            ("apt --fix-broken install", f"pkexec {application_path}/scripts/apt_fix_broken_wrap"),
            ("apt --fix-missing install", f"pkexec {application_path}/scripts/apt_fix_missing_wrap"),
            ("dpkg --configure -a", f"pkexec {application_path}/scripts/conf-a_wrap"),
            ("flatpak update", f"{application_path}/scripts/flatpak_update_wrap"),
            ("flatpak uninstall --unused", f"{application_path}/scripts/flatpak_clean_wrap"),
        ]
        self.command_buttons = []  # Liste zum Speichern aller Command-Buttons
        for label, cmd in commands:
            btn_label = Gtk.Label(label=label)
            btn_label.set_xalign(0)  # Links ausrichten
            btn = Gtk.Button()
            btn.set_child(btn_label)
            btn.connect("clicked", self._on_command_clicked, cmd)
            btn_box.append(btn)
            self.command_buttons.append(btn)  # Button zur Liste hinzufügen

        self.proc = None

    def _on_command_clicked(self, button, command):
        if self.proc:
            self.textbuffer.set_text("Bitte zuerst laufenden Prozess beenden!")
            return
        self.textbuffer.set_text("")
        # Alle Command-Buttons deaktivieren
        for btn in self.command_buttons:
            btn.set_sensitive(False)
        import threading
        def run():
            self.proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in self.proc.stdout:
                GLib.idle_add(self._append_text, line)
            self.proc.wait()
            self.proc = None
            # Button anzeigen nachdem Prozess beendet ist
            GLib.idle_add(self.quit_btn.set_visible, True)
        threading.Thread(target=run, daemon=True).start()

    def _append_text(self, text):
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, text)

    def _show_quit_dialog(self, button):
        dialog = Adw.AlertDialog.new("Verlauf", "Möchtest du den Verlauf speichern?\nDu findest das Protokoll anschließend im Ordner 'Dokumente'.")
        dialog.add_response("cancel", "Abbrechen")
        dialog.add_response("discard", "Verwerfen")
        dialog.add_response("save", "Speichern")
        dialog.set_response_appearance("discard", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("save")
        dialog.set_close_response("cancel")
        dialog.connect("response", self._on_dialog_response)
        dialog.present(self.get_root())
    
    def _on_dialog_response(self, dialog, response):
        if response == "save":
            self._save_history()
            self._clear_output()
        elif response == "discard":
            self._clear_output()
        # Bei "cancel" passiert nichts
    
    def _save_history(self):
        # Verlauf als TXT speichern
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start_iter, end_iter, False)
        
        # Zeitstempel im Format YYYY-MM-DD-HH-MM-SS
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        
        # Pfad zu ~/Dokumente
        docs_path = os.path.expanduser("~/Dokumente")
        os.makedirs(docs_path, exist_ok=True)
        
        filename = f"primo-verlauf-{timestamp}.txt"
        filepath = os.path.join(docs_path, filename)
        
        try:
            with open(filepath, "w") as f:
                f.write(text)
            print(f"Verlauf gespeichert: {filepath}")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
    
    def _clear_output(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None
        self.textbuffer.set_text("")
        self.quit_btn.set_visible(False)
        # Alle Command-Buttons wieder aktivieren
        for btn in self.command_buttons:
            btn.set_sensitive(True)
