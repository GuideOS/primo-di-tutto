import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from resorcess import *
from tabs.pop_ups import *
import subprocess
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import requests
from io import BytesIO
from logger_config import setup_logger

logger = setup_logger(__name__)


class ExpertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        #bootloader_frame = ttk.Frame(self.inst_notebook)
        source_frame = ttk.Frame(self.inst_notebook)
        #kernel_frame = ttk.Frame(self.inst_notebook)

        #bootloader_frame.pack(fill="both", expand=True)
        source_frame.pack(fill="both", expand=True)
        #kernel_frame.pack(fill="both", expand=True)

        #self.inst_notebook.add(bootloader_frame, compound=LEFT, text="Bootloader")
        self.inst_notebook.add(source_frame, compound=LEFT, text="Quellen")
        #self.inst_notebook.add(kernel_frame, compound=LEFT, text="Kernel")

       # bootloader_note_frame = BootloaderPanel(bootloader_frame)
        #bootloader_note_frame.pack(fill=tk.BOTH, expand=True)

        source_note_frame = SourcePanel(source_frame)
        source_note_frame.pack(fill=tk.BOTH, expand=True)

        #kernel_note_frame = KernelPanel(kernel_frame)
        #kernel_note_frame.pack(fill=tk.BOTH, expand=True)


class BootloaderPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.folder_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/folder_s_light.png"
        )
        self.backup_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/backup_s_light.png"
        )
        self.deb_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/deb_s_light.png"
        )
        self.recover_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/recover_s_light.png"
        )

        def get_grub_timeout():
            grub_config_path = "/etc/default/grub"
            timeout_style = None
            timeout_value = None

            try:
                with open(grub_config_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith("GRUB_TIMEOUT_STYLE"):
                            timeout_style = line.split("=")[1].strip().strip('"')
                        elif line.startswith("GRUB_TIMEOUT"):
                            timeout_value = line.split("=")[1].strip().strip('"')
                            if not timeout_value.isdigit():
                                logger.error(
                                    f"Unerwarteter Wert für GRUB_TIMEOUT: '{timeout_value}'"
                                )
                                timeout_value = None

                if timeout_value is not None and timeout_value.isdigit():
                    return int(timeout_value)
                elif timeout_style == "menu":
                    logger.warning(
                        "GRUB_TIMEOUT_STYLE ist auf 'menu' gesetzt. Verwende den Timeout-Wert dennoch."
                    )
                    return 11
                else:
                    logger.warning(
                        "GRUB_TIMEOUT_STYLE oder GRUB_TIMEOUT fehlen oder sind ungültig."
                    )

            except FileNotFoundError:
                logger.error("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                logger.error(f"Ein Fehler ist aufgetreten: {e}")

            return 6

        def get_grub_timeout_style():
            grub_config_path = "/etc/default/grub"
            try:
                with open(grub_config_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith("GRUB_TIMEOUT_STYLE"):
                            return line.split("=")[1].strip().strip('"')
            except FileNotFoundError:
                logger.error("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                logger.error(f"Ein Fehler ist aufgetreten: {e}")

            return "menu"

        def set_grub_timeout(timeout):
            grub_config_path = "/etc/default/grub"
            command = f"""
            pkexec bash -c '
            if grep -q "^GRUB_TIMEOUT=" {grub_config_path}; then
                sed -i "s/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT={timeout}/" {grub_config_path};
            else
                echo "GRUB_TIMEOUT={timeout}" >> {grub_config_path};
            fi
            update-grub'
            """
            os.system(command)

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info(f"GRUB-Timeout erfolgreich auf {timeout} gesetzt.")
                logger.info(result.stdout.decode("utf-8"))
            except subprocess.CalledProcessError as e:
                logger.error(f"Fehler beim Setzen des GRUB-Timeout: {e}")
                logger.error(e.stderr.decode("utf-8"))

        def set_grub_timeout_style(style):
            grub_config_path = "/etc/default/grub"
            command = f"pkexec bash -c 'sed -i \"s/^GRUB_TIMEOUT_STYLE=.*/GRUB_TIMEOUT_STYLE={style}/\" {grub_config_path} && update-grub'"

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info(f"GRUB_TIMEOUT_STYLE erfolgreich auf {style} gesetzt.")
                logger.info(result.stdout.decode("utf-8"))
            except subprocess.CalledProcessError as e:
                logger.error(f"Fehler beim Setzen des GRUB_TIMEOUT_STYLE: {e}")
                logger.error(e.stderr.decode("utf-8"))

        def update_grub_timeout():
            try:
                timeout = int(grub_timeout_spinbox.get())
                if timeout < 0:
                    raise ValueError("Das Timeout darf nicht negativ sein.")
                set_grub_timeout(timeout)
            except ValueError as ve:
                logger.error(f"Ungültige Eingabe: {ve}")

        def update_grub_menu():
            if grub_state_toggle_var.get() == 1:
                set_grub_timeout_style("menu")
            else:
                set_grub_timeout_style("hidden")

                self.backup_frame = ttk.LabelFrame(
                    self, text="Beschreibung", padding=20
                )

        self.recover_frame = ttk.LabelFrame(self, text="Grub Optionen", padding=50)
        self.recover_frame.pack(pady=20, padx=20, fill=BOTH)

        self.recover_frame.columnconfigure(0, weight=1)
        self.recover_frame.rowconfigure(0, weight=1)

        grub_state_label = ttk.Label(
            self.recover_frame,
            text="Boot-Menü aktivieren",
        )
        grub_state_label.grid(row=0, column=0, sticky="ew")

        grub_state_toggle_var = tk.IntVar()
        current_style = get_grub_timeout_style()
        if current_style == "menu":
            grub_state_toggle_var.set(1)
        else:
            grub_state_toggle_var.set(0)

        grub_state_toggle = ttk.Checkbutton(
            self.recover_frame,
            style="Switch.TCheckbutton",
            variable=grub_state_toggle_var,
            command=update_grub_menu,
        )
        grub_state_toggle.grid(row=0, column=2)

        grub_timeout_label = ttk.Label(self.recover_frame, text="GRUB Timeout setzen")
        grub_timeout_label.grid(row=1, column=0, sticky="ew")

        default_timeout = get_grub_timeout()

        grub_timeout_spinbox = ttk.Spinbox(
            self.recover_frame, from_=6, to=60, increment=1
        )
        grub_timeout_spinbox.set(default_timeout)
        grub_timeout_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        grub_timeout_button = ttk.Button(
            self.recover_frame, text="Auswählen", command=update_grub_timeout
        )
        grub_timeout_button.grid(row=1, column=2)

        def get_grub_gfxmode():
            grub_config_path = "/etc/default/grub"
            gfxmode = None
            gfxmode_commented = None

            try:
                with open(grub_config_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith("#GRUB_GFXMODE"):
                            gfxmode_commented = line.split("=")[1].strip().strip('"')
                        elif line.startswith("GRUB_GFXMODE"):
                            gfxmode = line.split("=")[1].strip().strip('"')

                if gfxmode:
                    return gfxmode
                elif gfxmode_commented:
                    return "Standardwert"
                else:
                    return "Standardwert"

            except FileNotFoundError:
                logger.error("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                logger.error(f"Ein Fehler ist aufgetreten: {e}")

            return "Standardwert"

        def set_grub_gfxmode(resolution):
            grub_config_path = "/etc/default/grub"

            if resolution == "Standardwert":
                command = f"pkexec bash -c 'sed -i \"s/^GRUB_GFXMODE=.*/#GRUB_GFXMODE=640x480/\" {grub_config_path} && update-grub'"
            else:
                command = f"pkexec bash -c 'sed -i \"s/^#\\?GRUB_GFXMODE=.*/GRUB_GFXMODE={resolution}/\" {grub_config_path} && update-grub'"

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info(f"GRUB GFXMODE erfolgreich auf {resolution} gesetzt.")
                logger.info(result.stdout.decode("utf-8"))
            except subprocess.CalledProcessError as e:
                logger.error(f"Fehler beim Setzen des GRUB GFXMODE: {e}")
                logger.error(e.stderr.decode("utf-8"))

        def update_gfxmode():
            resolution = grub_res_combobox.get()
            set_grub_gfxmode(resolution)

        grub_res_label = ttk.Label(self.recover_frame, text="GRUB Auflösung setzen")
        grub_res_label.grid(row=2, column=0, sticky="ew")

        resolutions = [
            "640x480",
            "800x600",
            "1024x768",
            "1280x1024",
            "1600x1200",
            "1920x1080",
            "2560x1440",
            "Standardwert",
        ]

        grub_res_combobox = ttk.Combobox(
            self.recover_frame, values=resolutions, state="readonly"
        )

        current_gfxmode = get_grub_gfxmode()
        grub_res_combobox.set(current_gfxmode)
        grub_res_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        grub_res_button = ttk.Button(
            self.recover_frame, text="Auswählen", command=update_gfxmode
        )
        grub_res_button.grid(row=2, column=2, sticky="ew")

        self.backup_frame = ttk.LabelFrame(self, text="Info", padding=20)
        self.backup_frame.pack(pady=20, padx=20, fill=BOTH)

        self.backup_frame.columnconfigure(0, weight=1)
        self.backup_frame.rowconfigure(0, weight=1)

        grub_info = """
Grub steht für Grand Unified Bootloader und dient zum Starten von Betriebssystemen wie Linux und Windows.
Viele Linux Distributionen verwenden GRUB als Standard Bootloader.

Features

- Unterstützung für viele Dateisysteme, u.a.: ext2, ext3, ext4, btrfs, XFS, ZFS, FAT (und einige mehr)
- Plattform und Architektur Unterstützung für x86, x64, PowerPC und ARM/ARM64
- Integrierte Shell für Skripte und Befehle sowie Support für die Programmiersprache Lua
- Anpassbare Auswahlmenüs (Farben, Hintergrundbilder, Aufbau/Struktur und deren Funktion)
- Bootet automatisiert oder über ein Auswahlmenü Betriebssysteme
- Betriebssysteme können von Festplatten, Disketten, CD- und DVD Medien, Imagedateien (ISO) und USB-Sticks gebootet
- Multi-Boot Support um mehrere Betriebssysteme auf einem Computer zu betreiben (z.B. Ubuntu und Windows)
- GRUB kann mit einem Passwort versehen werden
- Linux-Kernel können über eine Netzwerkverbindung geladen werden
- GRUB kommt sowohl mit MBR und GPT Partitionstabellen zurecht
- GRUB verfügt über einen Rettungsmodus um Bootprobleme beheben zu können

GRUB bietet mehrere Konfigurationsdateien um ihn an seine Wünsche anzupassen.
Neben Farben, Schriften und Hintergrundbildern kann die Reihenfolge und Benennung der Menüeinträge angepasst werden. 
Es ist auch möglich, verschiedene Linux-Kernel-Versionen über GRUB zu booten.
"""

        self.backup_discription = ttk.Label(
            self.backup_frame,
            text=grub_info,
            justify="left",
            anchor=W,
        ).grid(row=0, column=0, columnspan=2, sticky="ew")


class SourcePanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")

        self.added_repositories = ttk.LabelFrame(
            self, text="Eingebundene Repositories", padding=20
        )
        self.added_repositories.pack(fill="both", expand=True, padx=20, pady=20)

        self.added_tree_frame = tk.Frame(self.added_repositories)
        self.added_tree_frame.pack(fill="both", expand=True)

        self.added_treeview = ttk.Treeview(
            self.added_tree_frame, columns=("name"), show="headings"
        )
        self.added_treeview.heading("name", text="Name")
        self.added_treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.added_tree_frame, orient="vertical", command=self.added_treeview.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.added_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.add_sources_to_treeview()

        def open_source_f_d():
            popen(f"software-properties-gtk")

        self.open_source_folder = ttk.Button(
            self.added_repositories,
            text="Quellen bearbeiten",
            command=open_source_f_d,
            style="Custom.TButton",
        )
        self.open_source_folder.pack(pady=20, fill="x")

    def add_sources_to_treeview(self):
        sources_d1 = os.listdir("/etc/apt/sources.list.d")

        for file in sources_d1:
            self.added_treeview.insert("", "end", values=(file))


class KernelPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        def add_liquorix_repository():
            try:
                subprocess.run(
                    [
                        "sudo",
                        "sh",
                        "-c",
                        'echo "deb http://liquorix.net/debian sid main" > /etc/apt/sources.list.d/liquorix.list',
                    ],
                    check=True,
                )
                subprocess.run(
                    [
                        "wget",
                        "-O",
                        "/tmp/liquorix.key",
                        "https://liquorix.net/liquorix-keyring.gpg",
                    ],
                    check=True,
                )
                subprocess.run(
                    [
                        "sudo",
                        "cp",
                        "/tmp/liquorix.key",
                        "/etc/apt/trusted.gpg.d/liquorix-keyring.gpg",
                    ],
                    check=True,
                )
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                messagebox.showinfo(
                    "Erfolg", "Liquorix-Repository wurde erfolgreich hinzugefügt."
                )
            except subprocess.CalledProcessError as e:
                messagebox.showerror(
                    "Fehler", f"Fehler beim Hinzufügen des Liquorix-Repositorys: {e}"
                )

        def install_kernel(kernel_version):
            if kernel_version == "linux-image-liquorix-amd64":
                add_liquorix_repository()
            try:
                subprocess.run(
                    ["sudo", "apt-get", "install", "-y", kernel_version], check=True
                )
                messagebox.showinfo(
                    "Erfolg", f"Kernel {kernel_version} wurde erfolgreich installiert."
                )
            except subprocess.CalledProcessError as e:
                messagebox.showerror(
                    "Fehler", f"Fehler bei der Installation des Kernels: {e}"
                )

        def on_install_button_click():
            kernel_version = kernel_var.get()
            if kernel_version:
                messagebox.showinfo(
                    "Hinweis",
                    "Ein Terminal wird sich öffnen. Möglicherweise müssen Sie die Installation bestätigen und das Root-Passwort eingeben.",
                )
                threading.Thread(target=install_kernel, args=(kernel_version,)).start()
            else:
                messagebox.showwarning(
                    "Warnung", "Bitte wählen Sie eine Kernel-Version aus."
                )

        def update_description(*args):
            kernel_version = kernel_var.get()
            description = kernel_descriptions.get(kernel_version, "")
            description_label.config(text=description)

        def get_installed_kernel_versions():
            try:
                result = subprocess.run(
                    ["dpkg", "--list", "linux-image-*"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                kernel_versions = []
                for line in result.stdout.splitlines():
                    if line.startswith("ii"):
                        parts = line.split()
                        if len(parts) > 2 and "linux-image" in parts[1]:
                            kernel_versions.append((parts[1], parts[2]))
                return kernel_versions
            except subprocess.CalledProcessError as e:
                messagebox.showerror(
                    "Fehler", f"Fehler beim Abrufen der Kernel-Versionen: {e}"
                )
                return []

        # Liste der verfügbaren Kernel-Versionen und ihre Beschreibungen
        kernel_versions = [
            ("LTS-Kernel", "linux-image-amd64"),
            ("Realtime-Kernel", "linux-image-rt-amd64"),
            ("Liquorix-Kernel", "linux-image-liquorix-amd64"),
        ]
        kernel_descriptions = {
            "linux-image-amd64": "LTS Kernel: Stabil und langfristig unterstützt.",
            "linux-image-rt-amd64": "Real-Time Kernel: Für Echtzeitanwendungen optimiert.",
            "linux-image-liquorix-amd64": "Liquorix Kernel: Für Desktop- und Multimedia-Anwendungen optimiert.",
        }

        # Aktuellen Standard-Debian-Kernel hinzufügen
        try:
            result = subprocess.run(
                ["uname", "-r"], capture_output=True, text=True, check=True
            )
            current_kernel = result.stdout.strip()
            if "liquorix" not in current_kernel:
                kernel_versions.append(
                    ("Aktueller Standard-Kernel", f"linux-image-{current_kernel}")
                )
                kernel_descriptions[
                    f"linux-image-{current_kernel}"
                ] = "Aktueller Standard-Debian-Kernel."
        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Fehler", f"Fehler beim Abrufen des aktuellen Kernels: {e}"
            )

        # Installierte Kernel-Versionen abrufen und hinzufügen
        installed_kernels = get_installed_kernel_versions()
        for kernel_name, kernel_version in installed_kernels:
            if kernel_name not in [kv[1] for kv in kernel_versions]:
                kernel_versions.append(
                    (f"Installierter Kernel: {kernel_name}", kernel_name)
                )
                kernel_descriptions[
                    kernel_name
                ] = f"Installierter Kernel: {kernel_version}"

        self.kernel_main_frame = ttk.LabelFrame(
            self, text="Kernel-Modifiktion", padding=20
        )
        self.kernel_main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        kernel_version_frame = ttk.LabelFrame(
            self.kernel_main_frame, text="Kernel Version"
        )
        kernel_version_frame.pack(padx=10, pady=5, fill="x")

        kernel_var = tk.StringVar()
        kernel_var.trace("w", update_description)
        for idx, (kernel_name, kernel_value) in enumerate(kernel_versions):
            ttk.Radiobutton(
                kernel_version_frame,
                text=kernel_name,
                variable=kernel_var,
                value=kernel_value,
            ).grid(row=idx + 1, column=0, padx=10, sticky=tk.W)

        kernel_dsc_frame = ttk.LabelFrame(self.kernel_main_frame, text="Beschreibung")
        kernel_dsc_frame.pack(padx=10, pady=5, fill="x")

        description_label = tk.Label(kernel_dsc_frame, text="", justify=tk.LEFT)
        description_label.grid(
            row=0,
            column=1,
            columnspan=2,
            rowspan=len(kernel_versions) + 1,
            padx=10,
            pady=5,
            sticky=tk.NW,
        )

        install_button = ttk.Button(
            self.kernel_main_frame,
            text="Installieren",
            command=on_install_button_click,
            style="Custom.TButton",
        )
        install_button.pack(padx=10, pady=20, fill="x")
