from os import popen
from tkinter import *
from tkinter import ttk
import webbrowser
from resorcess import *
from tabs.pop_ups import *


class ContribTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        def open_website():
            webbrowser.open("https://guideos.de")

        def open_board():
            webbrowser.open("https://forum.linuxguides.de/core/index.php?dashboard/")

        # --- Participation Section ---
        self.take_part_frame = ttk.LabelFrame(self, text="Mach mit !", padding=20)
        self.take_part_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Description of the GuideOS project and participation philosophy
        take_part_message = ttk.Label(
            self.take_part_frame,
            wraplength=900,
            text="Das GuideOS-Projekt nimmt Open Source sehr ernst. Der wohl wichtigste Pfeiler der Philosophie ist die Teilhabe. Mit GuideOS wollen wir nicht die große neue Distro erschaffen, sondern einen einfachen Zugang zu Linux ermöglichen. Dazu gehört auch, dass Nutzer jeden Kenntnisstandes daran arbeiten können. Du kannst im Forum deine Meinung sagen, Code über Git beisteuern oder ohne Anmeldung eine Fehlermeldung verfassen (natürlich komplett anonym).",
        )
        take_part_message.pack(fill="x")

        # Button to open the GuideOS website
        go_home = ttk.Button(
            self.take_part_frame,
            text="GuideOS Website",
            style="Custom.TButton",
            command=open_website,
        )
        go_home.pack(fill="x", expand=True, pady=5)

        # Button to join the community forum
        go_board = ttk.Button(
            self.take_part_frame,
            text="Werde Teil der Community!",
            style="Custom.TButton",
            command=open_board,
        )
        go_board.pack(fill="x", expand=True, pady=5)

        def open_gitlab():
            webbrowser.open("https://github.com/GuideOS")

        def open_obs():
            webbrowser.open("https://build.opensuse.org/project/show/home:guideos")

        def open_ticket():
            popen("guideos-ticket-tool")

        # Button to open the GuideOS GitHub page
        go_git = ttk.Button(
            self.take_part_frame,
            text="GuideOS auf GitHub",
            style="Custom.TButton",
            command=open_gitlab,
        )
        go_git.pack(fill="x", expand=True, pady=5)

        # Button to open the Open Build Service page
        go_obs = ttk.Button(
            self.take_part_frame,
            text="GuideOS auf Open Build Service",
            style="Custom.TButton",
            command=open_obs,
        )
        go_obs.pack(fill="x", expand=True, pady=5)

        # Button to report a bug or issue
        send_error = ttk.Button(
            self.take_part_frame,
            text="Melde einen Fehler oder ein Problem",
            style="Custom.TButton",
            command=open_ticket,
        )
        send_error.pack(fill="x", expand=True, pady=5)

        self.thx_frame = ttk.LabelFrame(
            self,
            text="Ewiger Dank geht raus an die Community-Mitglieder ...",
            padding=20,
        )
        self.thx_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Create a text box and set the background color
        text_box = tk.Text(
            self.thx_frame, wrap="word"
        )  # Here the background color is changed
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(
            self.thx_frame, orient=tk.VERTICAL, command=text_box.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Connect the scrollbar to the text box
        text_box.config(yscrollcommand=scrollbar.set)

        # Insert text into the text box
        text_box.insert(
            tk.END,
            "@Bulvai @DenalB @evilware666 @Fhyrst @Gamma @GF-S15 @Gonzo-3004 @Hammer20l @harihegen @kim88 @KTT73 @maik3531 @Mastertac @MyLibertard @Nightworker @Perval @PinguinTV @Ritchy @Stardenver @Stephan @StephanR @stryvyr @dantechgamegeek @Toadie @vizh",
        )

        # Make the text box read-only
        text_box.config(state=tk.DISABLED)
