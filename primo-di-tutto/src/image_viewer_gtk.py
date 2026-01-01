import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import sys
import os

class ImageWindow(Gtk.Window):
    def __init__(self, image_path):
        super().__init__(title="Bildanzeige (Originalgröße, mit Scroll)")

        # ScrolledWindow erstellen
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # Bild in Gtk.Picture laden
        picture = Gtk.Picture.new_for_filename(image_path)
        picture.set_keep_aspect_ratio(True)  # Seitenverhältnis beibehalten
        picture.set_can_shrink(False)       # Skalierung deaktivieren

        scrolled_window.set_child(picture)

        # ScrolledWindow als Hauptinhalt setzen
        self.set_child(scrolled_window)

if __name__ == "__main__":
    image_path = "logo.png"  # Pfad zum Bild
    if not os.path.isfile(image_path):
        print(f"Bild '{image_path}' nicht gefunden.")
        sys.exit(1)

    app = Gtk.Application()

    def on_activate(app):
        win = ImageWindow(image_path)
        win.set_application(app)
        win.present()

    app.connect("activate", on_activate)
    app.run()
