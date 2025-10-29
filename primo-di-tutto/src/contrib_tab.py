import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import webbrowser

class ContribTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # --- Participation Section ---
        take_part_frame = Gtk.Frame()
        take_part_frame.set_label("Mach mit !")
        take_part_frame.set_margin_bottom(20)
        take_part_frame.set_hexpand(True)
        take_part_frame.set_vexpand(False)
        take_part_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        take_part_box.set_margin_top(20)
        take_part_box.set_margin_bottom(20)
        take_part_box.set_margin_start(20)
        take_part_box.set_margin_end(20)
        take_part_frame.set_child(take_part_box)
        self.append(take_part_frame)

        take_part_message = Gtk.Label(label="Das GuideOS-Projekt nimmt Open Source sehr ernst. Der wohl wichtigste Pfeiler der Philosophie ist die Teilhabe. Mit GuideOS wollen wir nicht die große neue Distro erschaffen, sondern einen einfachen Zugang zu Linux ermöglichen. Dazu gehört auch, dass Nutzer jeden Kenntnisstandes daran arbeiten können. Du kannst im Forum deine Meinung sagen, Code über Git beisteuern oder ohne Anmeldung eine Fehlermeldung verfassen (natürlich komplett anonym).")
        take_part_message.set_wrap(True)
        take_part_message.set_max_width_chars(90)
        take_part_box.append(take_part_message)

        def open_url(url):
            webbrowser.open(url)

        go_home = Gtk.Button(label="GuideOS Website")
        go_home.connect("clicked", lambda w: open_url("https://guideos.de"))
        take_part_box.append(go_home)

        go_board = Gtk.Button(label="Werde Teil der Community!")
        go_board.connect("clicked", lambda w: open_url("https://forum.linuxguides.de/core/index.php?dashboard/"))
        take_part_box.append(go_board)

        go_git = Gtk.Button(label="GuideOS auf GitHub")
        go_git.connect("clicked", lambda w: open_url("https://github.com/GuideOS"))
        take_part_box.append(go_git)

        go_obs = Gtk.Button(label="GuideOS auf Open Build Service")
        go_obs.connect("clicked", lambda w: open_url("https://build.opensuse.org/project/show/home:guideos"))
        take_part_box.append(go_obs)

        send_error = Gtk.Button(label="Melde einen Fehler oder ein Problem")
        send_error.connect("clicked", lambda w: open_url("guideos-ticket-tool"))  # Alternativ subprocess für lokalen Befehl
        take_part_box.append(send_error)

        # --- Dankes-Section ---
        thx_frame = Gtk.Frame()
        thx_frame.set_label("Ewiger Dank geht raus an die Community-Mitglieder ...")
        thx_frame.set_hexpand(True)
        thx_frame.set_vexpand(True)
        thx_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        thx_box.set_margin_top(20)
        thx_box.set_margin_bottom(20)
        thx_box.set_margin_start(20)
        thx_box.set_margin_end(20)
        thx_frame.set_child(thx_box)
        self.append(thx_frame)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        thx_box.append(scrolled)

        textview = Gtk.TextView()
        textview.set_hexpand(True)
        textview.set_vexpand(True)
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.get_buffer().set_text(
            "@Bulvai @DenalB @evilware666 @Fhyrst @Gamma @GF-S15 @Gonzo-3004 @Hammer20l @harihegen @kim88 @KTT73 @maik3531 @Mastertac @Nightworker @Perval @PinguinTV @Ritchy @Stardenver @Stephan @StephanR @stryvyr @dantechgamegeek @Toadie @vizh"
        )
        scrolled.set_child(textview)
