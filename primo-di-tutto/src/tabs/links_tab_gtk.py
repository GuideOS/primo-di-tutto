import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import webbrowser

class LinksTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(30)
        self.set_margin_end(30)

        linux_links = {
            "Rueegger-Blog - Tolle Artikel zu Linux-Themen": "https://www.rueegger.me/",
            "Holarse - Linux-Spiele-News": "https://holarse.de/",
            "ProtonDB - Prüfe die Kompatibilität deiner Spiele": "https://www.protondb.com/",
            "ProtonDB Borked - Spiele, die absolut gar nicht auf Linux laufen": "https://www.protondb.com/explore?sort=fixWanted",
            "LinuxNews - Das Neueste aus der Linux-Welt": "https://linuxnews.de/",
            "GNU/LINUX.ch - Tiefergehende Artikel zu Linux-Themen": "https://gnulinux.ch/",
            "Linux Command Library - Wissen, was ein Kommando tut": "https://linuxcommandlibrary.com/",
            "Open OS - Linux lernen": "http://www.openos.at/",
            "Distrowatch - Ausführliche Liste und Beschreibungen aller Distributionen": "https://distrowatch.com/",
            "Decocode - Wissensdatenbank": "https://www.decocode.de/",
            "Linux-Bibel - Die freundliche Website rund um Debian und Linux": "https://linux-bibel.at/",
        }

        grid = Gtk.Grid()
        grid.set_column_spacing(0)
        grid.set_row_spacing(8)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.append(grid)

        for idx, (label, url) in enumerate(linux_links.items()):
            btn = Gtk.Button(label=label)
            btn.set_hexpand(True)
            btn.connect("clicked", self.open_link, url)
            grid.attach(btn, 0, idx, 1, 1)

    def open_link(self, button, url):
        webbrowser.open_new_tab(url)
