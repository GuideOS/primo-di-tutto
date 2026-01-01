#!/usr/bin/env python3
import gi
gi.require_version("Adap", "1")
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
# from gi.repository import Adw, Gtk, Gio, Gdk
from gi.repository import Adap as Adw, Gtk, Gio, Gdk
from tabs.software_tab_gtk import SoftwareTab
from tabs.contrib_tab_gtk import ContribTab
from tabs.links_tab_gtk import LinksTab
from tabs.devices_tab_gtk import DevicesTab
from tabs.system_tab_gtk import SystemTab
from tabs.large_folders_tab_gtk import LargeFoldersTab
from tabs.dash_tab_gtk import DashTab
from tabs.welcome_tab_gtk import WelcomeTab

from tabs.expert_tools_gtk import ExpertToolsTab
from tabs.look_tab_gtk import LookTab


# Dummy Tab Widgets (Platzhalter für spätere Portierung)


from pathlib import Path
import os
import subprocess



class ExpertTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.append(Gtk.Label(label="Admin"))


class PrimoGTK(Adw.Application):
    def __init__(self):
        super().__init__(application_id="Primo")

    def do_activate(self):
        window = Adw.ApplicationWindow(application=self)
       # window.set_title("Primo | GuideOS Einstellungen (Adw)")
        window.set_default_size(1200, 750)
        window.set_size_request(1200, 750)  # Mindestgröße für das ganze Fenster
       
        # HeaderBar
        # Keine set_titlebar() bei Adw.ApplicationWindow! HeaderBar ggf. als Teil des Inhalts verwenden

        # Adwaita-Pattern: NavigationSplitView
        split_view = Adw.NavigationSplitView()
        # Sidebar-Stack
        sidebar = Gtk.StackSidebar()
        sidebar.set_vexpand(True)
        sidebar.set_hexpand(False)
        sidebar.set_size_request(160, -1)
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(300)
        stack.set_vexpand(True)
        stack.set_hexpand(True)
        # Tabs hinzufügen
        stack.add_titled(WelcomeTab(), "willkommen", "Willkommen")
        stack.add_titled(DashTab(), "dash", "Übersicht")
        stack.add_titled(SoftwareTab(), "software", "Software-\nEmpfehlungen")
        stack.add_titled(SystemTab(), "system", "Werkzeuge")
        stack.add_titled(DevicesTab(), "devices", "Geräte")
        stack.add_titled(ExpertToolsTab(), "admin", "Admin")
        stack.add_titled(LookTab(), "look", "Erscheinungsbild")
        stack.add_titled(LargeFoldersTab(), "largefolders", "Speicherfresser")
        stack.add_titled(LinksTab(), "links", "Links")
        stack.add_titled(ContribTab(), "contrib", "Mitmachen")
        sidebar.set_stack(stack)
        # Sidebar-Page mit ToolbarView und HeaderBar
        sidebar_toolbar = Adw.ToolbarView()
        sidebar_header = Adw.HeaderBar()
        sidebar_header.set_title_widget(Gtk.Label(label="Primo"))
        sidebar_toolbar.add_top_bar(sidebar_header)
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.append(sidebar)
        sidebar_toolbar.set_content(sidebar_box)
        sidebar_page = Adw.NavigationPage.new(sidebar_toolbar, title="Navigation")

        # Content-Page mit ToolbarView und HeaderBar
        content_toolbar = Adw.ToolbarView()
        content_header = Adw.HeaderBar()
        content_header.set_title_widget(Gtk.Label(label="GuideOS Einstellungen"))
        content_toolbar.add_top_bar(content_header)
        content_toolbar.set_content(stack)
        content_page = Adw.NavigationPage.new(content_toolbar, title="Inhalt")

        split_view.set_sidebar(sidebar_page)
        split_view.set_content(content_page)

        # ToolbarView entfällt, SplitView direkt ins Fenster
        # Kein eigenes CSS für Sidebar
        window.set_content(split_view)
        window.present()


if __name__ == "__main__":
    import sys
    app = PrimoGTK()
    sys.exit(app.run(sys.argv))

# Hinweis: Markup-Fehler (z.B. & → &amp;) müssen in den jeweiligen Tab-Implementierungen korrigiert werden.
