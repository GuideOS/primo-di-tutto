#!/usr/bin/python3

import gi
import logging
from resorcess import *
from apt_manage import *
from tabs.welcome_tab import WelcomeTab
from tabs.dash_tab import DashTab
from tabs.update_tab import UpdateTab
from tabs.system_tab import SystemTab
from tabs.look_tab import LookTab
from tabs.software_tab import *
from contrib_tab import ContribTab
from links_tab import LinksTab
from tabs.expert_tools import ExpertTab
from tabs.links_tab import LinksTab
from tabs.large_folders_tab import LargeFoldersTab
from logger_config import setup_logger

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

logger = setup_logger(__name__)

class MainApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.guideos.primo")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        window = Gtk.ApplicationWindow(application=app)
        window.set_title("Primo | GuideOS Einstellungen")
        window.set_default_size(1200, 750)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        window.set_child(box)

        # ListBox für die Navigation
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        listbox.set_size_request(200, -1)  # Mindestbreite der ListBox
        box.append(listbox)

        # Stack für die Inhalte
        stack = Gtk.Stack()
        stack.set_vexpand(True)
        stack.set_hexpand(True)
        box.append(stack)

        # Bereiche als Platzhalter
        sections = [
            ("Willkommen", Gtk.Label(label="Willkommen-Bereich")),
            ("Übersicht", Gtk.Label(label="Übersicht-Bereich")),
            ("Aktualisierungen", Gtk.Label(label="Aktualisierungen-Bereich")),
            ("Software-\nEmpfehlungen", Gtk.Label(label="Software-Empfehlungen-Bereich")),
            ("Werkzeuge", Gtk.Label(label="Werkzeuge-Bereich")),
            ("Admin", Gtk.Label(label="Admin-Bereich")),
            ("Erscheinungsbild", Gtk.Label(label="Erscheinungsbild-Bereich")),
            ("Speicherfresser", Gtk.Label(label="Speicherfresser-Bereich")),
            ("Links", LinksTab()),
            ("Mitmachen", ContribTab()),
        ]

        # Nur "Willkommen" bei erstem Start
        for name, widget in sections:
            if name == "Willkommen" and get_first_run() != "yes":
                continue
            label = Gtk.Label(label=name)
            label.set_margin_top(16)    # Mehr Abstand oben
            label.set_margin_bottom(16) # Mehr Abstand unten
            label.set_margin_start(12)  # Mehr Abstand links
            label.set_margin_end(12)    # Mehr Abstand rechts
            label.set_xalign(0.0)       # Links ausrichten
            row = Gtk.ListBoxRow()
            row.set_child(label)
            listbox.append(row)
            stack.add_titled(widget, name, name)

        def on_row_selected(listbox, row):
            if row:
                label = row.get_child().get_text()
                stack.set_visible_child_name(label)

        listbox.connect("row-selected", on_row_selected)
        # Standard: erstes Element anzeigen
        listbox.select_row(listbox.get_row_at_index(0))

        window.present()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
