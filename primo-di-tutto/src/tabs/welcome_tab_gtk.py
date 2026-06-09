
from gi.repository import Gtk
from pathlib import Path
import os
import subprocess
from resorcess import application_path, user

class WelcomeTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        #user = "live"
        # Logo oben (zentriert)
        logo_path = os.path.join(application_path, "images/icons/guideo_font_logo_dark.png")
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        logo_box.set_halign(Gtk.Align.CENTER)
        logo = Gtk.Picture.new_for_filename(logo_path)
        logo.set_content_fit(Gtk.ContentFit.CONTAIN)
        logo.set_size_request(120, 120)
        logo_box.append(logo)
        self.append(logo_box)


        # Begrüßungstext
        if user.lower() in ["live", "linux"]:
            welcome_message = "Hallo!"
            welcome_text_message = "Schön, dass du dir GuideOS anschaust. Du befindest dich im Live-Modus. Guck dich in Ruhe um und wenn du möchtest, komm hierher zurück, um GuideOS zu installieren. Wir wünschen dir viel Spaß."
            show_autostart = False
        else:
            welcome_message = f"Welcome {user.upper()}!"
            welcome_text_message = (
                "Dein einfacher Einstieg in die Welt von Linux.\n\n"
                "GuideOS ist eine Linux-Distribution, die von Mitgliedern des Linux Guides Forums ins Leben gerufen wurde. Sie wurde Ende 2024 entwickelt, um mit der Community gemeinsam einen Weg in die Welt von Linux zu finden. Unser Ziel ist es nicht nur, ein Betriebssystem zu schaffen, sondern vor allem den gemeinsamen Entwicklungsprozess zu erleben. Der Weg ist das Ziel!\n\n"
                "GuideOS richtet sich nicht nur an Anfänger und Umsteiger, sondern lädt alle Interessierten ein, mitzuwirken – auch ohne Programmierkenntnisse. Jeder kann etwas beitragen, sei es durch das Testen neuer Funktionen, das Einbringen von Ideen oder das Teilen von Erfahrungen.\n\n"
                "Der Schwerpunkt liegt aktuell darauf, zu schauen, ob wir gemeinsam mit der Community eine solche Distribution erfolgreich auf die Beine stellen können.\n\n"
                "Ob du Fragen hast, Ideen einbringen oder einfach nur Teil dieser wachsenden Gemeinschaft werden möchtest – besuche uns im Forum unter forum.linuxguides.de.\n\n"
                "Wir freuen uns über jeden, der GuideOS nutzt und mitgestaltet!"
            )
            show_autostart = True

        # Willkommens-Label
        welcome_label = Gtk.Label(label=welcome_message)
        welcome_label.set_margin_top(8)
        welcome_label.set_margin_bottom(8)
        welcome_label.set_xalign(0.5)
        welcome_label.set_css_classes(["title-1"])
        self.append(welcome_label)

        # Begrüßungstext (mehrzeilig, zentriert oder linksbündig, begrenzt)
        text_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        text_box.set_halign(Gtk.Align.CENTER)
        text_box.set_hexpand(True)
        welcome_text_label = Gtk.Label(label=welcome_text_message)
        welcome_text_label.set_wrap(True)
        welcome_text_label.set_wrap_mode(Gtk.WrapMode.WORD)
        if user.lower() in ["live", "linux"]:
            welcome_text_label.set_xalign(0.5)
            welcome_text_label.set_justify(Gtk.Justification.CENTER)
        else:
            welcome_text_label.set_xalign(0)
            welcome_text_label.set_justify(Gtk.Justification.LEFT)
        welcome_text_label.set_valign(Gtk.Align.CENTER)
        text_box.append(welcome_text_label)
        self.append(text_box)

        # Live-Modus: Installationsbutton und Horn-Icon unter dem Text, alles zentriert
        if user.lower() in ["live", "linux"]:
            horn_path = os.path.join(application_path, "images/icons/guidehorn.png")
            horn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            horn_box.set_halign(Gtk.Align.CENTER)
            if os.path.exists(horn_path):
                horn = Gtk.Picture.new_for_filename(horn_path)
                horn.set_content_fit(Gtk.ContentFit.CONTAIN)
                horn.set_size_request(64, 64)
                horn_box.append(horn)
            install_btn = Gtk.Button(label="GuideOS installieren")
            install_btn.add_css_class("suggested-action")
            install_btn.set_margin_top(12)
            install_btn.connect("clicked", self.on_install_clicked)
            horn_box.append(install_btn)
            self.append(horn_box)

        # Installierter Modus: Autostart-Option in Rahmen
        if show_autostart:
            frame = Gtk.Frame()
            frame.set_margin_top(24)
            frame.set_margin_bottom(8)
            frame.set_margin_start(8)
            frame.set_margin_end(8)
            frame.set_label("Autostart")
            autostart_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            autostart_box.set_margin_top(12)
            autostart_box.set_margin_bottom(12)
            autostart_label = Gtk.Label(label="Hier kannst Du den Autostart dieses Programms deaktivieren. Nach dem nächsten Start wird der Willkommensbildschirm entfernt und Primo wird zu einem Systemtool.")
            autostart_label.set_wrap(True)
            autostart_label.set_xalign(0)
            autostart_box.append(autostart_label)
            self.autostart_switch = Gtk.Switch()
            # Switch ist AN wenn Autostart aktiv ist (wird von main_gtk.py erstellt)
            self.autostart_switch.set_active(True)
            self.autostart_switch.connect("state-set", self.on_autostart_toggled)
            autostart_box.append(self.autostart_switch)
            frame.set_child(autostart_box)
            self.append(frame)

        # NVIDIA-Button (nur wenn installiert und NVIDIA vorhanden)
        if user.lower() not in ["live", "linux"] and self.has_nvidia_gpu():
            nvidia_path = os.path.join(application_path, "images/icons/nvidia-attentione.png")
            nvidia_icon = None
            if os.path.exists(nvidia_path):
                nvidia_icon = Gtk.Image.new_from_file(nvidia_path)
                nvidia_icon.set_pixel_size(24)
            nvidia_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            if nvidia_icon:
                nvidia_btn_box.append(nvidia_icon)
            nvidia_btn_label = Gtk.Label(label="NVIDIA-Manager öffnen")
            nvidia_btn_label.set_xalign(0)
            nvidia_btn_box.append(nvidia_btn_label)
            nvidia_btn = Gtk.Button()
            nvidia_btn.set_child(nvidia_btn_box)
            nvidia_btn.connect("clicked", self.on_nvidia_clicked)
            nvidia_btn.set_margin_top(8)
            self.append(nvidia_btn)

    def on_install_clicked(self, button):
        subprocess.Popen(["/usr/bin/calamares-install-guideos"])

    def on_nvidia_clicked(self, button):
        """Öffnet den NVIDIA-Manager."""
        try:
            subprocess.Popen(["x-terminal-emulator", "-e", "pkexec /usr/bin/debian-nvidia-installer"])
        except Exception as e:
            print(f"Fehler beim Öffnen des NVIDIA-Managers: {e}")

    def check_autostart_status(self):
        autostart_file = Path(os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop"))
        if autostart_file.exists():
            with open(autostart_file, "r") as file:
                for line in file:
                    if line.startswith("X-GNOME-Autostart-enabled="):
                        return line.strip().endswith("true")
        return False

    def on_autostart_toggled(self, switch, state):
        """Wird aufgerufen wenn der Switch umgeschaltet wird - deaktiviert den Autostart."""
        # Nur reagieren wenn Switch ausgeschaltet wird
        if not state:
            # 1. firstrun=no in Config setzen
            config_file_path = Path(os.path.expanduser("~/.primo/primo.conf"))
            self.update_config_file(config_file_path)
            
            # 2. X-GNOME-Autostart-enabled=false in Autostart-Datei setzen
            autostart_file_path = Path(os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop"))
            self.update_autostart_file(False, autostart_file_path)
            
            # Switch deaktivieren damit er nicht mehr geändert werden kann
            self.autostart_switch.set_sensitive(False)
        return False

    def update_config_file(self, config_file_path):
        """Aktualisiert die Konfigurationsdatei, um den Autostart zu deaktivieren."""
        if config_file_path.exists():
            with open(config_file_path, "r") as config_file:
                config_lines = config_file.readlines()
        else:
            config_lines = []
            # Verzeichnis erstellen, falls es nicht existiert
            config_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file_path, "w") as config_file:
            firstrun_set = False
            for line in config_lines:
                if line.startswith("firstrun="):
                    config_file.write("firstrun=no\n")
                    firstrun_set = True
                else:
                    config_file.write(line)

            # Falls "firstrun=" nicht gefunden wurde, am Ende hinzufügen
            if not firstrun_set:
                config_file.write("firstrun=no\n")

    def update_autostart_file(self, enabled, autostart_file=None):
        """Aktualisiert die .desktop-Datei für den Autostart basierend auf dem Switch-Status."""
        if autostart_file is None:
            autostart_file = Path(os.path.expanduser("~/.config/autostart/primo-di-tutto.desktop"))
        
        # Verzeichnis erstellen, falls es nicht existiert
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
        with open(autostart_file, "w") as file:
            file.write(content)

    def has_nvidia_gpu(self):
        try:
            output = subprocess.check_output(["lspci"], text=True)
            return "NVIDIA" in output
        except Exception:
            return False
