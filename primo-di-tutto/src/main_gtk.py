#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import traceback

# Erstelle Log-Verzeichnis, falls es nicht existiert
log_dir = Path(os.path.expanduser('~/.primo'))
log_dir.mkdir(parents=True, exist_ok=True)

# Logging-Setup für Debug-Ausgaben
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_dir / 'primo.log')
    ]
)
logger = logging.getLogger('primo')

logger.info("=" * 80)
logger.info("PRIMO-DI-TUTTO STARTET")
logger.info(f"Python Version: {sys.version}")
logger.info(f"Arbeitsverzeichnis: {os.getcwd()}")
logger.info("=" * 80)

try:
    logger.info("Importiere gi...")
    import gi
    logger.info("gi erfolgreich importiert")
    
    logger.info("Setze Version für Adap...")
    gi.require_version('Adap', '1')
    logger.info("Setze Version für Gtk...")
    gi.require_version("Gtk", "4.0")
    logger.info("Setze Version für Gdk...")
    gi.require_version("Gdk", "4.0")
    
    logger.info("Importiere GTK-Bibliotheken...")
    from gi.repository import Adap as Adw, Gtk, Gio, Gdk
    logger.info("GTK-Bibliotheken erfolgreich importiert")
    
except Exception as e:
    logger.error("FEHLER beim Import der GTK-Bibliotheken!")
    logger.error(f"Fehlermeldung: {e}")
    logger.error(traceback.format_exc())
    print("\n" + "=" * 80, file=sys.stderr)
    print("FEHLER: GTK4/Adwaita-Bibliotheken konnten nicht geladen werden!", file=sys.stderr)
    print(f"Fehlermeldung: {e}", file=sys.stderr)
    print("\nBitte installieren Sie die folgenden Pakete:", file=sys.stderr)
    print("  - python3-gi", file=sys.stderr)
    print("  - gir1.2-gtk-4.0", file=sys.stderr)
    print("  - gir1.2-adw-1", file=sys.stderr)
    print("=" * 80 + "\n", file=sys.stderr)
    sys.exit(1)

try:
    logger.info("Importiere resorcess...")
    from resorcess import application_path
    logger.info("Importiere Tab-Module...")
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
    logger.info("Alle Module erfolgreich importiert")
except Exception as e:
    logger.error("FEHLER beim Import der Anwendungsmodule!")
    logger.error(f"Fehlermeldung: {e}")
    logger.error(traceback.format_exc())
    print("\n" + "=" * 80, file=sys.stderr)
    print("FEHLER: Primo-Module konnten nicht geladen werden!", file=sys.stderr)
    print(f"Fehlermeldung: {e}", file=sys.stderr)
    print(f"\nStellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden:", file=sys.stderr)
    print(f"  Aktuell: {os.getcwd()}", file=sys.stderr)
    print("=" * 80 + "\n", file=sys.stderr)
    sys.exit(1)


class PrimoGTK(Adw.Application):
    def __init__(self):
        logger.info("Initialisiere PrimoGTK Application...")
        try:
            super().__init__(
                application_id="io.github.guideos.primo",
                flags=Gio.ApplicationFlags.FLAGS_NONE
            )
            # Verbinde das activate-Signal explizit
            self.connect('activate', self.on_activate)
            logger.info("PrimoGTK Application erfolgreich initialisiert")
        except Exception as e:
            logger.error(f"FEHLER bei Application-Initialisierung: {e}")
            logger.error(traceback.format_exc())
            raise

    def check_firstrun(self):
        """Prüft ob firstrun=yes in der Config-Datei steht und erstellt Autostart-Datei."""
        logger.info("Prüfe firstrun-Status...")
        config_file = Path(os.path.expanduser("~/.primo/primo.conf"))
        is_firstrun = True
        
        try:
            if config_file.exists():
                logger.info(f"Config-Datei gefunden: {config_file}")
                with open(config_file, "r") as f:
                    for line in f:
                        if line.startswith("firstrun="):
                            is_firstrun = line.strip() == "firstrun=yes"
                            logger.info(f"firstrun-Status: {is_firstrun}")
                            break
            else:
                logger.info("Keine Config-Datei gefunden, ist firstrun")
            
            # Wenn firstrun=yes, erstelle Autostart-Datei mit enabled=true
            if is_firstrun:
                logger.info("Erstelle Autostart-Datei...")
                self.create_autostart_file(enabled=True)
            
            return is_firstrun
        except Exception as e:
            logger.error(f"FEHLER bei firstrun-Prüfung: {e}")
            logger.error(traceback.format_exc())
            return True  # Im Fehlerfall firstrun annehmen
    
    def create_autostart_file(self, enabled=True):
        """Erstellt oder aktualisiert die Autostart-Desktop-Datei."""
        try:
            logger.info("Erstelle/Aktualisiere Autostart-Datei...")
            autostart_file = Path(os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop"))
            autostart_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = (
                "[Desktop Entry]\n"
                "Type=Application\n"
                "Exec=primo-di-tutto\n"
                f"X-GNOME-Autostart-enabled={'true' if enabled else 'false'}\n"
                "NoDisplay=false\n"
                "Hidden=false\n"
                "Name[de_DE]=primo-di-tutto.desktop\n"
                "Comment[de_DE]=Keine Beschreibung\n"
                "X-GNOME-Autostart-Delay=0\n"
            )
            with open(autostart_file, "w") as f:
                f.write(content)
            logger.info(f"Autostart-Datei erstellt: {autostart_file}")
        except Exception as e:
            logger.error(f"FEHLER beim Erstellen der Autostart-Datei: {e}")
            logger.error(traceback.format_exc())

    def on_activate(self, app):
        """Wird aufgerufen, wenn die Anwendung aktiviert wird."""
        logger.info("on_activate() wurde aufgerufen...")
        # Verhindere mehrfaches Erstellen des Fensters
        if not self.get_active_window():
            self.create_window()
        else:
            logger.info("Fenster existiert bereits, bringe es in den Vordergrund")
            self.get_active_window().present()
    
    def create_window(self):
        """Erstellt das Hauptfenster."""
        logger.info("create_window() wurde aufgerufen...")
        try:
            logger.info("Erstelle ApplicationWindow...")
            window = Adw.ApplicationWindow(application=self)
            window.set_icon_name("primo-di-tutto-logo")
           # window.set_title("Primo | GuideOS Einstellungen (Adw)")
            window.set_default_size(500, 750)
            window.set_resizable(True)  # Explizit auf skalierbar setzen
            logger.info("ApplicationWindow erstellt")
           
            # HeaderBar
            # Keine set_titlebar() bei Adw.ApplicationWindow! HeaderBar ggf. als Teil des Inhalts verwenden

            # Adwaita-Pattern: NavigationSplitView
            logger.info("Erstelle NavigationSplitView...")
            split_view = Adw.NavigationSplitView()
            
            # Stack für Content
            stack = Gtk.Stack()
            stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
            stack.set_transition_duration(300)
            stack.set_vexpand(True)
            stack.set_hexpand(True)
            logger.info("NavigationSplitView erstellt")
            
            # Welcome Tab nur anzeigen wenn firstrun=yes oder Config nicht existiert
            logger.info("Prüfe ob Welcome-Tab angezeigt werden soll...")
            show_welcome = self.check_firstrun()
            
            # Tabs hinzufügen
            logger.info("Füge Tabs hinzu...")
            tab_info = []
            if show_welcome:
                logger.info("  - Welcome Tab")
                stack.add_named(WelcomeTab(), "willkommen")
                tab_info.append(("willkommen", "Willkommen"))
            logger.info("  - Dash Tab")
            stack.add_named(DashTab(), "dash")
            tab_info.append(("dash", "Übersicht"))
            logger.info("  - System Tab")
            stack.add_named(SystemTab(), "system")
            tab_info.append(("system", "Werkzeuge"))
            logger.info("  - Devices Tab")
            stack.add_named(DevicesTab(), "devices")
            tab_info.append(("devices", "Geräte"))
            logger.info("  - Expert Tools Tab")
            stack.add_named(ExpertToolsTab(), "admin")
            tab_info.append(("admin", "Admin"))
            logger.info("  - Software Tab")
            stack.add_named(SoftwareTab(), "software")
            tab_info.append(("software", "Software-Empfehlungen"))
            logger.info("  - Look Tab")
            stack.add_named(LookTab(), "look")
            tab_info.append(("look", "Erscheinungsbild"))
            logger.info("  - Large Folders Tab")
            stack.add_named(LargeFoldersTab(), "largefolders")
            tab_info.append(("largefolders", "Speicherfresser"))
            logger.info("  - Links Tab")
            stack.add_named(LinksTab(), "links")
            tab_info.append(("links", "Links"))
            logger.info("  - Contrib Tab")
            stack.add_named(ContribTab(), "contrib")
            tab_info.append(("contrib", "Mitmachen"))
            logger.info("Alle Tabs hinzugefügt")
            
            # Manuelle Sidebar mit Buttons statt StackSidebar
            logger.info("Erstelle Sidebar...")
            sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            sidebar_box.set_margin_top(10)
            sidebar_box.set_margin_bottom(10)
            sidebar_box.set_margin_start(10)
            sidebar_box.set_margin_end(10)
            
            # Buttons für jeden Tab erstellen
            self.sidebar_buttons = []
            for tab_name, tab_label in tab_info:
                btn = Gtk.Button(label=tab_label)
                btn.set_hexpand(True)
                btn.get_child().set_xalign(0)  # Text linksbündig
                btn.set_name(f"sidebar-btn-{tab_name}")
                btn.connect("clicked", lambda b, name=tab_name: self.switch_tab(stack, name, b))
                self.sidebar_buttons.append((tab_name, btn))
                sidebar_box.append(btn)
            
            # Ersten Button als aktiv markieren
            if self.sidebar_buttons:
                self.sidebar_buttons[0][1].add_css_class("active-tab")
            
            sidebar_toolbar = Adw.ToolbarView()
            sidebar_header = Adw.HeaderBar()
            sidebar_header.set_title_widget(Gtk.Label(label="Primo"))
            
            # Über-Button in der Sidebar-HeaderBar
            about_btn = Gtk.Button()
            about_btn.set_icon_name("help-about")
            about_btn.set_tooltip_text("Über Primo")
            about_btn.connect("clicked", self.show_about_dialog)
            sidebar_header.pack_end(about_btn)
            
            sidebar_toolbar.add_top_bar(sidebar_header)
            sidebar_scroll = Gtk.ScrolledWindow()
            sidebar_scroll.set_name("sidebar_scroll")
            sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            sidebar_scroll.set_child(sidebar_box)
            sidebar_toolbar.set_content(sidebar_scroll)
            sidebar_page = Adw.NavigationPage.new(sidebar_toolbar, title="Navigation")
            logger.info("Sidebar erstellt")

            # Content-Page mit ToolbarView und HeaderBar
            logger.info("Erstelle Content-Bereich...")
            content_toolbar = Adw.ToolbarView()
            content_header = Adw.HeaderBar()
            content_header.set_title_widget(Gtk.Label(label="GuideOS Einstellungen"))
            content_toolbar.add_top_bar(content_header)
            content_toolbar.set_content(stack)
            content_page = Adw.NavigationPage.new(content_toolbar, title="Inhalt")

            split_view.set_sidebar(sidebar_page)
            split_view.set_content(content_page)
            split_view.set_show_content(True)
            
            # CSS hinzufügen um den weißen Separator zu entfernen und Buttons zu stylen
            css_provider = Gtk.CssProvider()
            css_provider.load_from_string("""
                /* Erlaube kleinere Fensterbreite */
                window {
                    min-width: 300px;
                }
                
                navigation-split-view,
                .navigation-split-view {
                    min-width: 300px;
                }
                
                headerbar {
                    min-width: 100px;
                }
                
                /* StackSidebar-spezifische Separatoren */
                stacksidebar separator,
                .sidebar separator,
                stacksidebar row separator,
                stacksidebar.sidebar separator {
                    background-color: transparent;
                    background: transparent;
                    min-width: 0px;
                    min-height: 0px;
                    opacity: 0;
                }
                
                /* Allgemeine Separatoren */
                separator,
                paned separator,
                .navigation-split-view separator,
                navigation-split-view separator {
                    background-color: transparent;
                    background: transparent;
                    min-width: 0px;
                    min-height: 0px;
                    opacity: 0;
                }
                
                /* Sidebar Buttons ohne Standard-Umrahmung */
                #sidebar_scroll button {
                    border: 1px solid transparent;
                    background: transparent;
                    box-shadow: none;
                    outline: none;
                    outline-width: 0;
                    outline-style: none;
                }
                
                /* Focus-Outline entfernen */
                #sidebar_scroll button:focus {
                    outline: none;
                    outline-width: 0;
                    box-shadow: none;
                }
                
                /* Hover-Effekt */
                #sidebar_scroll button:hover {
                    border: 1px solid alpha(currentColor, 0.3);
                    background: alpha(currentColor, 0.05);
                    outline: none;
                }
                
                /* Aktiver/ausgewählter Tab */
                #sidebar_scroll button.active-tab {
                    border: 1px solid alpha(currentColor, 0.5);
                    background: alpha(currentColor, 0.1);
                    outline: none;
                }
                
                /* Aktiver Tab beim Hover */
                #sidebar_scroll button.active-tab:hover {
                    border: 1px solid alpha(currentColor, 0.6);
                    background: alpha(currentColor, 0.15);
                    outline: none;
                }
            """)
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER
            )
            
            logger.info("Setze Window-Content und zeige Fenster...")
            window.set_content(split_view)
            window.present()
            logger.info("Fenster erfolgreich angezeigt!")
            
        except Exception as e:
            logger.error("KRITISCHER FEHLER in create_window()!")
            logger.error(f"Fehlermeldung: {e}")
            logger.error(traceback.format_exc())
            print("\n" + "=" * 80, file=sys.stderr)
            print("FEHLER: Das Hauptfenster konnte nicht erstellt werden!", file=sys.stderr)
            print(f"Fehlermeldung: {e}", file=sys.stderr)
            print("\nBitte prüfen Sie die Log-Datei: ~/.primo/primo.log", file=sys.stderr)
            print("=" * 80 + "\n", file=sys.stderr)
            raise

    def switch_tab(self, stack, tab_name, clicked_button):
        """Wechselt zum ausgewählten Tab und hebt den Button hervor"""
        stack.set_visible_child_name(tab_name)
        # Entferne active-tab Klasse von allen Buttons
        for _, btn in self.sidebar_buttons:
            btn.remove_css_class("active-tab")
        # Füge active-tab Klasse zum geklickten Button hinzu
        clicked_button.add_css_class("active-tab")
    
    def show_about_dialog(self, button):
        about = Adw.AboutDialog.new()
        about.set_application_name("Primo Di Tutto")
        #about.set_version("1.0.0")
        about.set_developer_name("actionschnitzel@guideos.de")
        about.set_copyright("© 2024-2026 GuideOS")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://guideos.de")
        about.set_issue_url("https://github.com/guideos/primo-di-tutto/issues")
        
        about.set_comments(
            "Dein einfacher Einstieg in die Welt von Linux.\n\n"
            "GuideOS ist eine Linux-Distribution, die von Mitgliedern des "
            "Linux Guides Forums ins Leben gerufen wurde."
        )
        
        about.set_developers([
            "GuideOS Community\nGuideOS Core Team"
            
        ])
        
        about.set_application_icon("primo-di-tutto-logo")
        about.present(self.get_active_window())


if __name__ == "__main__":
    try:
        logger.info("Starte Anwendung...")
        logger.info("Erstelle PrimoGTK-Instanz...")
        app = PrimoGTK()
        logger.info("Rufe app.run() auf...")
        exit_code = app.run(sys.argv)
        logger.info(f"Anwendung beendet mit Exit-Code: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        logger.error("KRITISCHER FEHLER beim Start der Anwendung!")
        logger.error(f"Fehlermeldung: {e}")
        logger.error(traceback.format_exc())
        print("\n" + "=" * 80, file=sys.stderr)
        print("FEHLER: Die Anwendung konnte nicht gestartet werden!", file=sys.stderr)
        print(f"Fehlermeldung: {e}", file=sys.stderr)
        print("\nDetails finden Sie in der Log-Datei: ~/.primo/primo.log", file=sys.stderr)
        print("=" * 80 + "\n", file=sys.stderr)
        sys.exit(1)

# Hinweis: Markup-Fehler (z.B. & → &amp;) müssen in den jeweiligen Tab-Implementierungen korrigiert werden.
