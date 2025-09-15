import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
from resorcess import *
from tabs.pop_ups import *
import subprocess
from tkinter import messagebox
import threading
from io import BytesIO
from tabs.system_dict_lib import SoftwareSys
from logger_config import setup_logger

logger = setup_logger(__name__)


class ExpertTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.inst_notebook = ttk.Notebook(self)
        self.inst_notebook.pack(fill=BOTH, expand=True)

        # bootloader_frame = ttk.Frame(self.inst_notebook)
        source_frame = ttk.Frame(self.inst_notebook)
        # kernel_frame = ttk.Frame(self.inst_notebook)
        admin_frame = ttk.Frame(self.inst_notebook)

        # bootloader_frame.pack(fill="both", expand=True)
        source_frame.pack(fill="both", expand=True)
        # kernel_frame.pack(fill="both", expand=True)
        admin_frame.pack(fill="both", expand=True)

        # self.inst_notebook.add(bootloader_frame, compound=LEFT, text="Bootloader")
        self.inst_notebook.add(source_frame, compound=LEFT, text="Quellen")
        # self.inst_notebook.add(kernel_frame, compound=LEFT, text="Kernel")
        self.inst_notebook.add(admin_frame, compound=LEFT, text="Admin")

        # bootloader_note_frame = BootloaderPanel(bootloader_frame)
        # bootloader_note_frame.pack(fill=tk.BOTH, expand=True)

        source_note_frame = SourcePanel(source_frame)
        source_note_frame.pack(fill=tk.BOTH, expand=True)

        # kernel_note_frame = KernelPanel(kernel_frame)
        # kernel_note_frame.pack(fill=tk.BOTH, expand=True)

        admin_note_frame = AdminPanel(admin_frame)
        admin_note_frame.pack(fill=tk.BOTH, expand=True)


class AdminPanel(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Frame für Canvas und Scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas-Container für sys_btn_frame
        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar hinzufügen
        scrollbar = ttk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame in den Canvas einfügen
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # sys_btn_frame in das scrollbare Frame einfügen
        sys_btn_frame = ttk.LabelFrame(scrollable_frame, text="Werkzeuge", padding=20)
        sys_btn_frame.pack(fill="both", expand=tk.TRUE)

        sys_btn_frame.grid_columnconfigure(0, weight=2)
        sys_btn_frame.grid_columnconfigure(1, weight=2)
        sys_btn_frame.grid_columnconfigure(2, weight=2)
        sys_btn_frame.grid_columnconfigure(3, weight=1)
        sys_btn_frame.grid_columnconfigure(4, weight=2)

        def sys_btn_action(sys_key):
            # SoftwareSys.sys_dict[sys_key]["Action"]
            command = SoftwareSys.sys_dict[sys_key]["Action"]
            print(command)
            os.popen(command)

        self.sys_btn_icons = []

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            icon = tk.PhotoImage(file=sys_info["Icon"])
            self.sys_btn_icons.append(icon)

        max_columns = 4

        for i, (sys_key, sys_info) in enumerate(SoftwareSys.sys_dict.items()):
            row = i // max_columns
            column = i % max_columns

            sys_button = ttk.Button(
                sys_btn_frame,
                text=sys_info["Name"],
                image=self.sys_btn_icons[i],
                command=lambda key=sys_key: sys_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            sys_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_button.bind(
                "<Enter>", lambda event, key=sys_key: self.on_hover(event, key)
            )
            sys_button.bind("<Leave>", self.on_leave)

        sys_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        sys_info_frame.pack(pady=20, padx=20, fill="both")

        # Label für die Anzeige der Beschreibung
        self.sys_info_label = tk.Label(sys_info_frame, justify="left", wraplength=900)
        self.sys_info_label.pack(anchor="w")

    # Funktion für das Hover-Ereignis
    def on_hover(self, event, key):
        self.sys_info_label.configure(text=SoftwareSys.sys_dict[key]["Description"])

    # Funktion für das Verlassen des Buttons
    def on_leave(self, event):
        self.sys_info_label.configure(text="")

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
                kernel_descriptions[f"linux-image-{current_kernel}"] = (
                    "Aktueller Standard-Debian-Kernel."
                )
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
                kernel_descriptions[kernel_name] = (
                    f"Installierter Kernel: {kernel_version}"
                )

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
