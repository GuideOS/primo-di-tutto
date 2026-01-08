import gi
import os
import subprocess
from datetime import datetime
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, GObject
from gi.repository import Adw
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
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Hauptlayout: Links Liste, Rechts Buttons
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.append(main_box)

        # Linke Seite: Repository-Liste
        left_frame = Gtk.Frame(label="Software-Quellen")
        left_frame.set_hexpand(True)
        left_frame.set_vexpand(True)
        main_box.append(left_frame)

        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        left_vbox.set_margin_top(12)
        left_vbox.set_margin_bottom(12)
        left_vbox.set_margin_start(12)
        left_vbox.set_margin_end(12)
        left_frame.set_child(left_vbox)

        # TreeView: [Aktiv, Typ, URI, Distribution, Komponenten, Datei]
        self.store = Gtk.ListStore(bool, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_headers_visible(True)
        
        # Spalte: Aktiv (Toggle)
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self._on_source_toggled)
        column_active = Gtk.TreeViewColumn("Aktiv", renderer_toggle, active=0)
        column_active.set_resizable(False)
        column_active.set_fixed_width(60)
        self.treeview.append_column(column_active)
        
        # Spalte: Typ
        renderer_text = Gtk.CellRendererText()
        column_type = Gtk.TreeViewColumn("Typ", renderer_text, text=1)
        column_type.set_resizable(True)
        column_type.set_min_width(60)
        self.treeview.append_column(column_type)
        
        # Spalte: URI
        renderer_uri = Gtk.CellRendererText()
        column_uri = Gtk.TreeViewColumn("URI", renderer_uri, text=2)
        column_uri.set_resizable(True)
        column_uri.set_expand(True)
        self.treeview.append_column(column_uri)
        
        # Spalte: Distribution
        renderer_dist = Gtk.CellRendererText()
        column_dist = Gtk.TreeViewColumn("Distribution", renderer_dist, text=3)
        column_dist.set_resizable(True)
        column_dist.set_min_width(100)
        self.treeview.append_column(column_dist)
        
        # Spalte: Komponenten
        renderer_comps = Gtk.CellRendererText()
        column_comps = Gtk.TreeViewColumn("Komponenten", renderer_comps, text=4)
        column_comps.set_resizable(True)
        column_comps.set_expand(True)
        self.treeview.append_column(column_comps)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.treeview)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        left_vbox.append(scrolled)

        # Rechte Seite: Buttons
        right_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        right_vbox.set_vexpand(True)
        main_box.append(right_vbox)

        # Bearbeiten-Button
        self.edit_btn = Gtk.Button(label="Bearbeiten")
        self.edit_btn.set_sensitive(False)
        self.edit_btn.connect("clicked", self._on_edit_clicked)
        right_vbox.append(self.edit_btn)

        # Entfernen-Button
        self.remove_btn = Gtk.Button(label="Entfernen")
        self.remove_btn.set_sensitive(False)
        self.remove_btn.connect("clicked", self._on_remove_clicked)
        right_vbox.append(self.remove_btn)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        right_vbox.append(spacer)

        # Aktualisieren-Button
        self.refresh_btn = Gtk.Button(label="Aktualisieren")
        self.refresh_btn.connect("clicked", lambda b: self._populate_sources())
        right_vbox.append(self.refresh_btn)

        # Selection ändern -> Buttons aktivieren/deaktivieren
        selection = self.treeview.get_selection()
        selection.connect("changed", self._on_selection_changed)

        self._populate_sources()

    def _populate_sources(self):
        """Liest alle APT-Quellen aus /etc/apt/sources.list und sources.list.d/"""
        self.store.clear()
        sources = []
        
        # Lese /etc/apt/sources.list (traditionelles Format)
        try:
            with open("/etc/apt/sources.list", "r") as f:
                for line in f:
                    sources.append((line.strip(), "/etc/apt/sources.list", "traditional"))
        except:
            pass
        
        # Lese /etc/apt/sources.list.d/
        sources_dir = "/etc/apt/sources.list.d"
        try:
            for filename in sorted(os.listdir(sources_dir)):
                filepath = os.path.join(sources_dir, filename)
                
                # .list Dateien (traditionelles Format)
                if filename.endswith(".list"):
                    try:
                        with open(filepath, "r") as f:
                            for line in f:
                                sources.append((line.strip(), filepath, "traditional"))
                    except:
                        pass
                
                # .sources Dateien (DEB822 Format)
                elif filename.endswith(".sources"):
                    try:
                        with open(filepath, "r") as f:
                            content = f.read()
                            # Parse DEB822 Format
                            for entry in self._parse_deb822(content, filepath):
                                sources.append(entry)
                    except:
                        pass
        except:
            pass
        
        # Parse und füge zur Liste hinzu
        for entry in sources:
            if len(entry) == 3:
                line, filepath, format_type = entry
                
                if format_type == "traditional":
                    if not line:
                        continue
                    
                    # Prüfe ob deaktiviert (kommentiert)
                    enabled = not line.strip().startswith("#")
                    
                    # Entferne Kommentar für Parsing
                    clean_line = line.strip()
                    if clean_line.startswith("#"):
                        clean_line = clean_line[1:].strip()
                    
                    parts = clean_line.split()
                    if len(parts) < 4:
                        continue
                    
                    # Parse: deb [optionen] uri distribution komponenten
                    source_type = parts[0]
                    
                    # Prüfe ob es eine gültige Quellenzeile ist (muss mit deb/deb-src beginnen)
                    if source_type not in ["deb", "deb-src"]:
                        continue
                    
                    idx = 1
                    
                    # Überspringe Optionen in eckigen Klammern
                    while idx < len(parts) and parts[idx].startswith('['):
                        # Finde Ende der Optionen (kann mehrere Tokens sein)
                        while idx < len(parts) and not parts[idx].endswith(']'):
                            idx += 1
                        idx += 1  # Überspringe das schließende ']'
                    
                    if idx >= len(parts) or idx + 2 >= len(parts):
                        continue
                    
                    uri = parts[idx]
                    distribution = parts[idx + 1]
                    components = " ".join(parts[idx + 2:]) if idx + 2 < len(parts) else ""
                    
                    # Kürze Dateiname
                    short_file = os.path.basename(filepath)
                    
                    self.store.append([enabled, source_type, uri, distribution, components, short_file, line])
            
            elif len(entry) == 7:
                # DEB822 Entry bereits geparsed
                enabled, source_type, uri, distribution, components, short_file, raw_data = entry
                self.store.append([enabled, source_type, uri, distribution, components, short_file, raw_data])

    def _parse_deb822(self, content, filepath):
        """Parsed DEB822-Format (.sources Dateien)"""
        entries = []
        current_entry = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Leere Zeile = Ende eines Eintrags
            if not line:
                if current_entry:
                    entries.extend(self._deb822_to_entries(current_entry, filepath))
                    current_entry = {}
                continue
            
            # Kommentare ignorieren
            if line.startswith('#'):
                continue
            
            # Key: Value Format
            if ':' in line:
                key, value = line.split(':', 1)
                current_entry[key.strip()] = value.strip()
        
        # Letzter Eintrag
        if current_entry:
            entries.extend(self._deb822_to_entries(current_entry, filepath))
        
        return entries

    def _deb822_to_entries(self, entry, filepath):
        """Konvertiert einen DEB822-Eintrag in traditionelle Format-Einträge"""
        results = []
        
        # Extrahiere Felder
        enabled = entry.get('Enabled', 'yes').lower() == 'yes'
        types = entry.get('Types', 'deb').split()
        uris = entry.get('URIs', '').split()
        suites = entry.get('Suites', '').split()
        components = entry.get('Components', '')
        
        short_file = os.path.basename(filepath)
        
        # Erstelle für jede Kombination einen Eintrag
        for source_type in types:
            for uri in uris:
                for suite in suites:
                    # Format: [enabled, type, uri, suite, components, filename, raw_data]
                    raw_data = f"DEB822: {source_type} {uri} {suite} {components}"
                    results.append((enabled, source_type, uri, suite, components, short_file, raw_data))
        
        return results

    def _on_source_toggled(self, widget, path):
        """Aktiviert/Deaktiviert eine Quelle"""
        iter = self.store.get_iter(path)
        current_state = self.store[iter][0]
        new_state = not current_state
        
        # Hole die Zeile und Datei
        original_line = self.store[iter][6]
        filename = self.store[iter][5]
        filepath = self._get_filepath_from_filename(filename)
        
        # Prüfe ob es eine DEB822-Datei ist
        if filepath.endswith(".sources"):
            # DEB822-Format: Ändere Enabled-Feld
            self._modify_deb822_enabled(filepath, new_state)
            # Aktualisiere komplette Liste
            self._populate_sources()
        else:
            # Traditionelles Format: Kommentiere Zeile
            if new_state:
                # Aktivieren: Entferne #
                new_line = original_line.lstrip("#").lstrip()
            else:
                # Deaktivieren: Füge # hinzu
                new_line = "# " + original_line.lstrip("#").lstrip()
            
            # Schreibe Änderung
            self._modify_source_file(filepath, original_line, new_line)
            
            # Aktualisiere Store
            self.store[iter][0] = new_state
            self.store[iter][6] = new_line

    def _on_selection_changed(self, selection):
        """Aktiviert/Deaktiviert Buttons basierend auf Auswahl"""
        model, iter = selection.get_selected()
        has_selection = iter is not None
        
        # Bearbeiten nur für .list-Dateien aktivieren
        if has_selection:
            filename = model[iter][5]
            filepath = self._get_filepath_from_filename(filename)
            can_edit = not filepath.endswith(".sources")
            self.edit_btn.set_sensitive(can_edit)
        else:
            self.edit_btn.set_sensitive(False)
        
        self.remove_btn.set_sensitive(has_selection)

    def _on_edit_clicked(self, button):
        """Zeigt Dialog zum Bearbeiten einer Quelle"""
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if not iter:
            return
        
        filename = model[iter][5]
        filepath = self._get_filepath_from_filename(filename)
        
        # .sources-Dateien können nicht bearbeitet werden (zu komplex)
        if filepath.endswith(".sources"):
            dialog = Adw.AlertDialog.new(
                "Bearbeiten nicht möglich",
                "DEB822-Format (.sources) Dateien können nicht direkt bearbeitet werden.\n\n"
                "Sie können die Quelle aktivieren/deaktivieren oder entfernen."
            )
            dialog.add_response("ok", "OK")
            dialog.set_default_response("ok")
            dialog.present(self.get_root())
            return
        
        # Hole aktuelle Werte
        enabled = model[iter][0]
        source_type = model[iter][1]
        uri = model[iter][2]
        distribution = model[iter][3]
        components = model[iter][4]
        original_line = model[iter][6]
        
        dialog = EditSourceDialog(self.get_root(), source_type, uri, distribution, components, enabled)
        dialog.connect("response", self._on_edit_dialog_response, iter, filename, original_line)
        dialog.present()

    def _on_edit_dialog_response(self, dialog, response, iter, filename, original_line):
        if response == "save":
            new_line = dialog.get_source_line()
            if new_line:
                filepath = self._get_filepath_from_filename(filename)
                self._modify_source_file(filepath, original_line, new_line)
                self._populate_sources()
        dialog.destroy()

    def _on_remove_clicked(self, button):
        """Entfernt eine Quelle"""
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if not iter:
            return
        
        source_type = model[iter][1]
        uri = model[iter][2]
        distribution = model[iter][3]
        filename = model[iter][5]
        original_line = model[iter][6]
        
        # Warndialog
        dialog = Adw.AlertDialog.new(
            "Warnung: Quelle entfernen",
            f"Sie sollten genau wissen, was Sie gerade entfernen!\n\n"
            f"Typ: {source_type}\n"
            f"URI: {uri}\n"
            f"Distribution: {distribution}\n"
            f"Datei: {filename}\n\n"
            f"Möchten Sie diese Quelle wirklich entfernen?"
        )
        dialog.add_response("no", "Nein")
        dialog.add_response("yes", "Ja, entfernen")
        dialog.set_response_appearance("yes", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("no")
        dialog.set_close_response("no")
        dialog.connect("response", self._on_remove_confirmed, filename, original_line)
        dialog.present(self.get_root())

    def _on_remove_confirmed(self, dialog, response, filename, original_line):
        if response == "yes":
            filepath = self._get_filepath_from_filename(filename)
            
            # Bei .sources-Dateien: Komplette Datei löschen
            if filepath.endswith(".sources"):
                try:
                    os.system(f"pkexec rm {filepath}")
                except Exception as e:
                    print(f"Fehler beim Löschen der Datei: {e}")
            else:
                # Bei .list-Dateien: Zeile entfernen
                self._remove_source_line(filepath, original_line)
            
            self._populate_sources()

    def _get_filepath_from_filename(self, filename):
        """Gibt vollständigen Pfad zurück"""
        if filename == "sources.list":
            return "/etc/apt/sources.list"
        else:
            return os.path.join("/etc/apt/sources.list.d", filename)

    def _add_source_line(self, line):
        """Fügt eine neue Zeile zu sources.list.d hinzu"""
        # Erstelle neue Datei in sources.list.d
        filename = f"primo-custom-{os.urandom(4).hex()}.list"
        filepath = os.path.join("/etc/apt/sources.list.d", filename)
        
        command = f"echo '{line}' | pkexec tee {filepath} > /dev/null"
        os.system(command)

    def _modify_source_file(self, filepath, old_line, new_line):
        """Ändert eine Zeile in einer Datei"""
        try:
            with open(filepath, "r") as f:
                content = f.read()
            
            new_content = content.replace(old_line, new_line)
            
            # Schreibe mit pkexec
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.list') as tmp:
                tmp.write(new_content)
                tmp_path = tmp.name
            
            os.system(f"pkexec cp {tmp_path} {filepath}")
            os.unlink(tmp_path)
        except Exception as e:
            print(f"Fehler beim Ändern: {e}")

    def _modify_deb822_enabled(self, filepath, enabled):
        """Ändert das Enabled-Feld in einer DEB822-Datei"""
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
            
            new_lines = []
            enabled_found = False
            
            for line in lines:
                if line.strip().startswith("Enabled:"):
                    # Ändere Enabled-Feld
                    new_lines.append(f"Enabled: {'yes' if enabled else 'no'}\n")
                    enabled_found = True
                else:
                    new_lines.append(line)
            
            # Falls kein Enabled-Feld existiert, füge es am Anfang hinzu
            if not enabled_found:
                # Finde erste nicht-leere, nicht-Kommentar Zeile
                insert_index = 0
                for i, line in enumerate(new_lines):
                    if line.strip() and not line.strip().startswith('#'):
                        insert_index = i
                        break
                new_lines.insert(insert_index, f"Enabled: {'yes' if enabled else 'no'}\n")
            
            # Schreibe mit pkexec
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sources') as tmp:
                tmp.writelines(new_lines)
                tmp_path = tmp.name
            
            os.system(f"pkexec cp {tmp_path} {filepath}")
            os.unlink(tmp_path)
        except Exception as e:
            print(f"Fehler beim Ändern der DEB822-Datei: {e}")

    def _remove_source_line(self, filepath, line):
        """Entfernt eine Zeile aus einer Datei"""
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
            
            # Entferne die Zeile (auch wenn sie kommentiert ist)
            line_stripped = line.strip()
            # Entferne auch das # falls vorhanden für Vergleich
            line_clean = line_stripped.lstrip("#").strip()
            
            new_lines = []
            for l in lines:
                l_stripped = l.strip()
                l_clean = l_stripped.lstrip("#").strip()
                # Überspringe die Zeile, wenn sie übereinstimmt (egal ob kommentiert oder nicht)
                if l_stripped != line_stripped and l_clean != line_clean:
                    new_lines.append(l)
            
            # Schreibe mit pkexec
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.list') as tmp:
                tmp.writelines(new_lines)
                tmp_path = tmp.name
            
            os.system(f"pkexec cp {tmp_path} {filepath}")
            os.unlink(tmp_path)
        except Exception as e:
            print(f"Fehler beim Entfernen: {e}")


class AddSourceDialog(Adw.Dialog):
    """Dialog zum Hinzufügen einer neuen Quelle"""
    
    __gsignals__ = {
        'response': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }
    
    def __init__(self, parent):
        super().__init__()
        self.set_title("Quelle hinzufügen")
        
        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        toolbar_view.set_content(content)
        
        # Beispiel-Label
        example_label = Gtk.Label(label="Beispiel:\ndeb http://archive.ubuntu.com/ubuntu jammy main restricted")
        example_label.set_xalign(0)
        example_label.add_css_class("dim-label")
        content.append(example_label)
        
        # APT-Zeile Entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("deb URI Distribution Komponenten")
        self.entry.connect("changed", self._on_entry_changed)
        content.append(self.entry)
        
        # Button-Box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_margin_top(12)
        content.append(button_box)
        
        cancel_btn = Gtk.Button(label="Abbrechen")
        cancel_btn.connect("clicked", lambda b: self.emit("response", "cancel"))
        button_box.append(cancel_btn)
        
        self.add_btn = Gtk.Button(label="Hinzufügen")
        self.add_btn.add_css_class("suggested-action")
        self.add_btn.set_sensitive(False)
        self.add_btn.connect("clicked", lambda b: self.emit("response", "add"))
        button_box.append(self.add_btn)
        
        self.set_default_size(500, -1)

    def _on_entry_changed(self, entry):
        text = entry.get_text().strip()
        # Einfache Validierung: muss mit deb/deb-src beginnen
        valid = text.startswith("deb ") or text.startswith("deb-src ")
        self.add_btn.set_sensitive(valid)

    def get_source_line(self):
        return self.entry.get_text().strip()


class AddPPADialog(Adw.Dialog):
    """Dialog zum Hinzufügen eines PPAs"""
    
    __gsignals__ = {
        'response': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }
    
    def __init__(self, parent):
        super().__init__()
        self.set_title("PPA hinzufügen")
        
        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        toolbar_view.set_content(content)
        
        # Beispiel-Label
        example_label = Gtk.Label(label="Beispiel: user/ppa-name")
        example_label.set_xalign(0)
        example_label.add_css_class("dim-label")
        content.append(example_label)
        
        # PPA Entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("user/ppa-name")
        self.entry.connect("changed", self._on_entry_changed)
        content.append(self.entry)
        
        # Button-Box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_margin_top(12)
        content.append(button_box)
        
        cancel_btn = Gtk.Button(label="Abbrechen")
        cancel_btn.connect("clicked", lambda b: self.emit("response", "cancel"))
        button_box.append(cancel_btn)
        
        self.add_btn = Gtk.Button(label="Hinzufügen")
        self.add_btn.add_css_class("suggested-action")
        self.add_btn.set_sensitive(False)
        self.add_btn.connect("clicked", lambda b: self.emit("response", "add"))
        button_box.append(self.add_btn)
        
        self.set_default_size(400, -1)

    def _on_entry_changed(self, entry):
        text = entry.get_text().strip()
        # Einfache Validierung: muss user/ppa Format haben
        valid = "/" in text and len(text) > 3
        self.add_btn.set_sensitive(valid)

    def get_ppa(self):
        return self.entry.get_text().strip()


class EditSourceDialog(Adw.Dialog):
    """Dialog zum Bearbeiten einer Quelle"""
    
    __gsignals__ = {
        'response': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }
    
    def __init__(self, parent, source_type, uri, distribution, components, enabled):
        super().__init__()
        self.set_title("Quelle bearbeiten")
        
        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        toolbar_view.set_content(content)
        
        # Aktiviert Checkbox
        self.enabled_check = Gtk.CheckButton(label="Quelle aktiviert")
        self.enabled_check.set_active(enabled)
        content.append(self.enabled_check)
        
        # Typ Dropdown
        type_label = Gtk.Label(label="Typ:", xalign=0)
        content.append(type_label)
        
        self.type_dropdown = Gtk.DropDown.new_from_strings(["deb", "deb-src"])
        self.type_dropdown.set_selected(0 if source_type == "deb" else 1)
        content.append(self.type_dropdown)
        
        # URI Entry
        uri_label = Gtk.Label(label="URI:", xalign=0)
        content.append(uri_label)
        
        self.uri_entry = Gtk.Entry()
        self.uri_entry.set_text(uri)
        content.append(self.uri_entry)
        
        # Distribution Entry
        dist_label = Gtk.Label(label="Distribution:", xalign=0)
        content.append(dist_label)
        
        self.dist_entry = Gtk.Entry()
        self.dist_entry.set_text(distribution)
        content.append(self.dist_entry)
        
        # Komponenten Entry
        comp_label = Gtk.Label(label="Komponenten:", xalign=0)
        content.append(comp_label)
        
        self.comp_entry = Gtk.Entry()
        self.comp_entry.set_text(components)
        content.append(self.comp_entry)
        
        # Button-Box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_margin_top(12)
        content.append(button_box)
        
        cancel_btn = Gtk.Button(label="Abbrechen")
        cancel_btn.connect("clicked", lambda b: self.emit("response", "cancel"))
        button_box.append(cancel_btn)
        
        save_btn = Gtk.Button(label="Speichern")
        save_btn.add_css_class("suggested-action")
        save_btn.connect("clicked", lambda b: self.emit("response", "save"))
        button_box.append(save_btn)

    def get_source_line(self):
        """Erstellt die APT-Zeile aus den Eingaben"""
        prefix = "" if self.enabled_check.get_active() else "# "
        type_str = "deb" if self.type_dropdown.get_selected() == 0 else "deb-src"
        uri = self.uri_entry.get_text().strip()
        dist = self.dist_entry.get_text().strip()
        comps = self.comp_entry.get_text().strip()
        
        return f"{prefix}{type_str} {uri} {dist} {comps}"


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
