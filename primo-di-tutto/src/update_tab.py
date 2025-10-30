import gi
import threading
import subprocess

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class UpdateTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        info = Gtk.Label(label="Hier kannst Du alle verfügbaren Aktualisierungen für Dein System installieren. Dies umfasst Updates für das Betriebssystem, installierte Software und Anwendungen aus verschiedenen Quellen wie APT und Flatpak. Klicke einfach auf 'Alles Aktualisieren', um den Prozess zu starten. Während der Aktualisierung werden alle Schritte in einem Terminalfenster angezeigt, damit Du den Fortschritt verfolgen kannst.")
        info.set_wrap(True)
        info.set_max_width_chars(90)
        info.set_xalign(0.0)
        self.append(info)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.append(button_box)

        update_btn = Gtk.Button(label="Alles Aktualisieren")
        update_btn.set_hexpand(True)
        update_btn.connect("clicked", self.on_update_clicked)
        button_box.append(update_btn)

        term_frame = Gtk.Frame()
        term_frame.set_label("Prozess")
        term_frame.set_hexpand(True)
        term_frame.set_vexpand(True)
        self.append(term_frame)

        term_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        term_box.set_margin_top(10)
        term_box.set_margin_bottom(10)
        term_box.set_margin_start(10)
        term_box.set_margin_end(10)
        term_frame.set_child(term_box)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(self.textview)
        term_box.append(scrolled)

        self.quit_btn = Gtk.Button(label="Beenden")
        self.quit_btn.set_hexpand(False)
        self.quit_btn.connect("clicked", self.on_quit_clicked)
        self.quit_btn.set_sensitive(False)
        term_box.append(self.quit_btn)

    def on_update_clicked(self, button):
        self.textview.get_buffer().set_text("")
        self.quit_btn.set_sensitive(False)
        thread = threading.Thread(target=self.run_update)
        thread.start()

    def run_update(self):
        command = "pkexec /home/schnitzel/primo-di-tutto/primo-di-tutto/scripts/all_up"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(process.stdout.readline, ""):
            GLib.idle_add(self.append_text, line)
        process.stdout.close()
        process.wait()
        GLib.idle_add(self.quit_btn.set_sensitive, True)

    def append_text(self, text):
        buf = self.textview.get_buffer()
        end_iter = buf.get_end_iter()
        buf.insert(end_iter, text)

    def on_quit_clicked(self, button):
        self.textview.get_buffer().set_text("")
        self.quit_btn.set_sensitive(False)
