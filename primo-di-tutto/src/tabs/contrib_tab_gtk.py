import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import webbrowser
import subprocess

class ContribTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # --- Participation Section ---
        take_part_frame = Gtk.Frame()
        take_part_frame.set_label("Mach mit !")
        take_part_frame.set_margin_bottom(20)
        take_part_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        take_part_box.set_margin_top(20)
        take_part_box.set_margin_bottom(20)
        take_part_box.set_margin_start(20)
        take_part_box.set_margin_end(20)
        take_part_frame.set_child(take_part_box)
        self.append(take_part_frame)

        take_part_message = Gtk.Label(
            label="Das GuideOS-Projekt nimmt Open Source sehr ernst. Der wohl wichtigste Pfeiler der Philosophie ist die Teilhabe. Mit GuideOS wollen wir nicht die große neue Distro erschaffen, sondern einen einfachen Zugang zu Linux ermöglichen. Dazu gehört auch, dass Nutzer jeden Kenntnisstandes daran arbeiten können. Du kannst im Forum deine Meinung sagen, Code über Git beisteuern oder ohne Anmeldung eine Fehlermeldung verfassen (natürlich komplett anonym).",
            wrap=True,
            xalign=0
        )
        take_part_box.append(take_part_message)

        def open_website(_btn, url):
            webbrowser.open(url)

        def open_ticket(_btn):
            subprocess.Popen(["guideos-ticket-tool"])

        # Buttons
        btns = [
            ("GuideOS Website", "https://guideos.de"),
            ("Werde Teil der Community!", "https://forum.linuxguides.de/core/index.php?dashboard/"),
            ("GuideOS auf GitHub", "https://github.com/GuideOS"),
            ("GuideOS.eu Repository", "https://guideos.eu/repo/")
        ]
        for text, url in btns:
            btn = Gtk.Button(label=text)
            btn.connect("clicked", open_website, url)
            take_part_box.append(btn)

        send_error = Gtk.Button(label="Melde einen Fehler oder ein Problem")
        send_error.connect("clicked", open_ticket)
        take_part_box.append(send_error)

        # --- Dankes-Section ---
        thx_frame = Gtk.Frame()
        thx_frame.set_label("Ewiger Dank geht raus an die Community-Mitglieder ...")
        thx_frame.set_margin_bottom(20)
        thx_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        thx_box.set_margin_top(20)
        thx_box.set_margin_bottom(20)
        thx_box.set_margin_start(20)
        thx_box.set_margin_end(20)
        thx_frame.set_child(thx_box)
        self.append(thx_frame)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        thx_box.append(scrolled)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.get_buffer().set_text(
            "@Actionschnitzel @Bulvai @DenalB @evilware666 @Fhyrst @Freydis @Gamma @GF-S15 @Gonzo-3004 @Hammer20l @harihegen @kim88 @KTT73 @maik3531 @Mastertac @MyLibertard @Nightworker @Perval @PinguinTV @Ritchy @Stardenver @Stephan @StephanR @stryvyr @dantechgamegeek @Toadie @vizh"
        )
        scrolled.set_child(textview)
