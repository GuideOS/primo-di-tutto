import gi
import webbrowser

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class LinksTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(30)
        self.set_margin_end(30)

        linux_links = {
            "Rueegger Blog - Tolle Artikel zu Linux-Themen": "https://www.rueegger.me/",
            "Holarse - Linuxspiele-News": "https://holarse.de/",
            "ProtonDB - Checke die Kompatibilitär deiner Games": "https://www.protondb.com/",
            "LinuxNews - Das Neueste aus der Linux Welt": "https://linuxnews.de/",
            "GNU/LINUX.ch - Tiefergehende Artikel zu Linux-Themen": "https://gnulinux.ch/",
            "Linux Command Library - Wissen, was ein Kommando tut": "https://linuxcommandlibrary.com/",
            "Open OS - Linux lernen": "http://www.openos.at/",
            "Distrowatch - Ausführliche Liste und Beschreibungen aller Distros": "https://distrowatch.com/",
            "Decocode - Wissens-Datenbank": "https://www.decocode.de/",
            "Linux-Bibel - Die freundliche Website rund um Debian und Linux": "https://linux-bibel.at/",
        }

        for label, url in linux_links.items():
            btn = Gtk.Button(label=label)
            btn.set_hexpand(True)
            btn.connect("clicked", lambda w, url=url: webbrowser.open_new_tab(url))
            self.append(btn)
