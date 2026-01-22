import gi
import os
import subprocess
import threading

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

class LargeFoldersTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        my_home = os.path.expanduser("~")
        self.my_home = my_home
        self.path_nodes = {}  # Pfad: TreeIter
        self.node_paths = {}  # TreeIter: Pfad

        # Scan-Button hinzufügen
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        button_box.set_halign(Gtk.Align.START)
        self.scan_button = Gtk.Button(label="Ordner scannen")
        self.scan_button.add_css_class("suggested-action")
        self.scan_button.connect("clicked", self.on_scan_clicked)
        button_box.append(self.scan_button)
        
        self.status_label = Gtk.Label(label="Klicken Sie auf 'Ordner scannen', um große Ordner zu finden")
        self.status_label.set_xalign(0)
        button_box.append(self.status_label)
        
        self.spinner = Gtk.Spinner()
        self.spinner.set_margin_start(8)
        button_box.append(self.spinner)
        
        self.append(button_box)

        # TreeView und Model
        self.store = Gtk.TreeStore(str, str)  # Pfad, Größe
        self.tree = Gtk.TreeView(model=self.store)
        renderer_text = Gtk.CellRendererText()
        col_path = Gtk.TreeViewColumn("Pfad", renderer_text, text=0)
        col_size = Gtk.TreeViewColumn("Größe", renderer_text, text=1)
        self.tree.append_column(col_path)
        self.tree.append_column(col_size)
        self.tree.set_hexpand(True)
        self.tree.set_vexpand(True)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.tree)
        scrolled.set_vexpand(True)
        self.append(scrolled)

        # Doppelklick-Event
        self.tree.connect("row-activated", self.on_row_activated)

    def on_scan_clicked(self, button):
        # Button deaktivieren während des Scannens
        self.scan_button.set_sensitive(False)
        self.status_label.set_text("Scanne Verzeichnisse... Bitte warten...")
        self.spinner.start()
        
        # Store leeren für neuen Scan
        self.store.clear()
        self.path_nodes.clear()
        self.node_paths.clear()
        
        # Scan in separatem Thread ausführen
        thread = threading.Thread(target=self._scan_thread)
        thread.daemon = True
        thread.start()
    
    def _scan_thread(self):
        # Daten einlesen
        du_data = self.get_du_output(self.my_home)
        
        # UI-Updates thread-safe über GLib.idle_add
        GLib.idle_add(self._populate_tree, du_data)
    
    def _populate_tree(self, du_data):
        # Daten in TreeView einfügen
        for path, size in du_data:
            self.insert_path(path, size, self.my_home)
        
        # Button wieder aktivieren
        self.spinner.stop()
        self.scan_button.set_sensitive(True)
        self.status_label.set_text(f"Scan abgeschlossen: {len(du_data)} Ordner gefunden")
        return False  # Wichtig: False zurückgeben, damit idle_add nur einmal aufgerufen wird

    def get_du_output(self, home):
        result = subprocess.run([
            "du", "-h", "--max-depth=10", f"{home}/"
        ], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        output = []
        for line in lines:
            try:
                size, path = line.strip().split(None, 1)
                output.append((path, size))
            except ValueError:
                continue
        return output

    def insert_path(self, path, size, home):
        rel_path = os.path.relpath(path, home)
        parts = rel_path.split(os.sep)
        current_parent = None
        full_path = ""
        for part in parts:
            if not part:
                continue
            full_path = os.path.join(full_path, part)
            if full_path not in self.path_nodes:
                node_iter = self.store.append(current_parent, [part, ""])
                self.path_nodes[full_path] = node_iter
                self.node_paths[self.store.get_path(node_iter).to_string()] = os.path.join(home, full_path)
                current_parent = node_iter
            else:
                current_parent = self.path_nodes[full_path]
        self.store.set_value(self.path_nodes[full_path], 1, size)

    def on_row_activated(self, tree, path, column):
        node_iter = self.store.get_iter(path)
        if node_iter:
            abs_path = self.node_paths.get(path.to_string())
            if abs_path:
                try:
                    subprocess.Popen(["nemo", abs_path])
                except FileNotFoundError:
                    print("Nemo nicht gefunden. Stelle sicher, dass Nemo installiert ist.")
