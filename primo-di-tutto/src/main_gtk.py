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

class PrimoGTK(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.github.guideos.primo")

    def check_firstrun(self):
        """Prüft ob firstrun=yes in der Config-Datei steht und erstellt Autostart-Datei."""
        config_file = Path(os.path.expanduser("~/.primo/primo.conf"))
        is_firstrun = True
        
        if config_file.exists():
            with open(config_file, "r") as f:
                for line in f:
                    if line.startswith("firstrun="):
                        is_firstrun = line.strip() == "firstrun=yes"
                        break
        
        # Wenn firstrun=yes, erstelle Autostart-Datei mit enabled=true
        if is_firstrun:
            self.create_autostart_file(enabled=True)
        
        return is_firstrun
    
    def create_autostart_file(self, enabled=True):
        """Erstellt oder aktualisiert die Autostart-Desktop-Datei."""
        autostart_file = Path(os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop"))
        autostart_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Exec=python3 /opt/primo-di-tutto/src/main.py\n"
            f"X-GNOME-Autostart-enabled={'true' if enabled else 'false'}\n"
            "NoDisplay=false\n"
            "Hidden=false\n"
            "Name[de_DE]=primo-di-tutto.desktop\n"
            "Comment[de_DE]=Keine Beschreibung\n"
            "X-GNOME-Autostart-Delay=0\n"
        )
        with open(autostart_file, "w") as f:
            f.write(content)

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
        
        # Welcome Tab nur anzeigen wenn firstrun=yes oder Config nicht existiert
        show_welcome = self.check_firstrun()
        
        # Tabs hinzufügen
        if show_welcome:
            stack.add_titled(WelcomeTab(), "willkommen", "Willkommen")
        stack.add_titled(DashTab(), "dash", "Übersicht")
        stack.add_titled(SystemTab(), "system", "Werkzeuge")
        stack.add_titled(DevicesTab(), "devices", "Geräte")
        stack.add_titled(ExpertToolsTab(), "admin", "Admin")
        stack.add_titled(SoftwareTab(), "software", "Software-Empfehlungen")
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
