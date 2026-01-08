import gi
gi.require_version("Adw", "1")
from gi.repository import Gtk
from gi.repository import Adw

class AboutTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        
        # Button zum Öffnen des About-Dialogs
        about_btn = Gtk.Button(label="Über Primo anzeigen")
        about_btn.add_css_class("pill")
        about_btn.add_css_class("suggested-action")
        about_btn.set_size_request(200, 50)
        about_btn.connect("clicked", self.show_about_dialog)
        self.append(about_btn)
    
    def show_about_dialog(self, button):
        about = Adw.AboutDialog.new()
        about.set_application_name("Primo Di Tutto")
        about.set_version("1.0.0")
        about.set_developer_name("GuideOS Team")
        about.set_copyright("© 2024-2026 GuideOS")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://forum.linuxguides.de")
        about.set_issue_url("https://github.com/guideos/primo-di-tutto/issues")
        
        about.set_comments(
            "Dein einfacher Einstieg in die Welt von Linux.\n\n"
            "GuideOS ist eine Linux-Distribution, die von Mitgliedern des "
            "Linux Guides Forums ins Leben gerufen wurde."
        )
        
        about.set_developers([
            "GuideOS Community"
        ])
        
        about.set_application_icon("io.github.guideos.primo")
        
        about.present(self.get_root())
