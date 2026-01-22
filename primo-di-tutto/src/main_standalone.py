#!/usr/bin/env python3
"""
Standalone Launcher für Primo Tabs
Ermöglicht das Öffnen einzelner Tabs als eigenständige Fenster über Kommandozeilen-Flags.

Verwendung:
    python3 main_tabs_standalone.py --tab software
    python3 main_tabs_standalone.py --tab system
    python3 main_tabs_standalone.py -t dash
"""
import os
import sys
import argparse
from pathlib import Path

import gi
gi.require_version('Adap', '1')
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Adap as Adw, Gtk, Gio

from resorcess import application_path
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


# Tab-Registry: Name -> (Class, Display-Name)
TAB_REGISTRY = {
    "welcome": (WelcomeTab, "Willkommen"),
    "dash": (DashTab, "Übersicht"),
    "system": (SystemTab, "Werkzeuge"),
    "devices": (DevicesTab, "Geräte"),
    "admin": (ExpertToolsTab, "Admin"),
    "software": (SoftwareTab, "Software-Empfehlungen"),
    "look": (LookTab, "Erscheinungsbild"),
    "largefolders": (LargeFoldersTab, "Speicherfresser"),
    "links": (LinksTab, "Links"),
    "contrib": (ContribTab, "Mitmachen"),
}


class PrimoTabStandalone(Adw.Application):
    def __init__(self, tab_name):
        super().__init__(
            application_id=f"io.github.guideos.primo.tab.{tab_name}",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.tab_name = tab_name
        
        # Validiere Tab-Name
        if tab_name not in TAB_REGISTRY:
            print(f"Fehler: Tab '{tab_name}' nicht gefunden!")
            print(f"Verfügbare Tabs: {', '.join(TAB_REGISTRY.keys())}")
            sys.exit(1)

    def do_activate(self):
        # Erstelle Fenster
        window = Adw.ApplicationWindow(application=self)
        window.set_icon_name("primo-di-tutto-logo")
        
        # Hole Tab-Klasse und Display-Name
        tab_class, display_name = TAB_REGISTRY[self.tab_name]
        window.set_title(f"Primo | {display_name}")
        
        # Setze vernünftige Mindestgröße basierend auf Tab-Typ
        if self.tab_name in ["software", "largefolders"]:
            window.set_default_size(1100, 750)
        elif self.tab_name in ["dash", "system", "devices"]:
            window.set_default_size(1100, 750)
        elif self.tab_name in ["look", "admin"]:
            window.set_default_size(900, 650)
        else:
            window.set_default_size(850, 600)
        
        # ToolbarView mit HeaderBar
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        header_bar.set_title_widget(Gtk.Label(label=f"Primo | {display_name}"))
        
        # Info-Button in der HeaderBar
        info_btn = Gtk.Button()
        info_btn.set_icon_name("help-about")
        info_btn.set_tooltip_text("Über Primo")
        info_btn.connect("clicked", self.show_about_dialog)
        header_bar.pack_end(info_btn)
        
        toolbar_view.add_top_bar(header_bar)
        
        # Erstelle Tab-Instanz
        try:
            tab_content = tab_class()
            # Kein expand, damit das Fenster sich an den Inhalt anpasst
        except Exception as e:
            print(f"Fehler beim Erstellen des Tabs '{self.tab_name}': {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        # Scrolled Window für Tab (falls nötig)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(tab_content)
        # Kein expand - Fenster passt sich an Inhalt an
        
        toolbar_view.set_content(scrolled)
        window.set_content(toolbar_view)
        window.present()

    def show_about_dialog(self, button):
        about = Adw.AboutDialog.new()
        about.set_application_name("Primo Di Tutto")
        about.set_developer_name("actionschnitzel@guideos.de")
        about.set_copyright("© 2024-2026 GuideOS")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://guideos.de")
        about.set_issue_url("https://github.com/guideos/primo-di-tutto/issues")
        
        about.set_comments(
            "Dein einfacher Einstieg in die Welt von Linux.\n\n"
            "GuideOS ist eine Linux-Distribution, die von Mitgliedern des "
            "Linux Guides Forums ins Leben gerufen wurde.\n\n"
            f"Standalone-Modus: {TAB_REGISTRY[self.tab_name][1]}"
        )
        
        about.set_developers([
            "GuideOS Community\nGuideOS Core Team"
        ])
        
        about.set_application_icon("primo-di-tutto-logo")
        about.present(self.get_active_window())


def main():
    parser = argparse.ArgumentParser(
        description="Primo Tabs Standalone Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Verfügbare Tabs:
{chr(10).join(f"  {name:15} - {display_name}" for name, (_, display_name) in TAB_REGISTRY.items())}

Beispiele:
  %(prog)s --tab software
  %(prog)s -t system
  %(prog)s --tab dash
        """
    )
    
    parser.add_argument(
        "-t", "--tab",
        required=True,
        choices=list(TAB_REGISTRY.keys()),
        help="Name des Tabs, der geöffnet werden soll"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Liste alle verfügbaren Tabs auf"
    )
    
    args = parser.parse_args()
    
    # Liste Tabs auf, falls gewünscht
    if args.list:
        print("Verfügbare Tabs:")
        for name, (_, display_name) in TAB_REGISTRY.items():
            print(f"  {name:15} - {display_name}")
        sys.exit(0)
    
    # Erstelle und starte Standalone-App
    app = PrimoTabStandalone(args.tab)
    sys.exit(app.run(sys.argv[:1]))  # sys.argv[:1] damit argparse-Argumente nicht an Gtk weitergegeben werden


if __name__ == "__main__":
    main()
