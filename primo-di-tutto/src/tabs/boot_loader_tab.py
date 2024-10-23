import os
from os import popen
import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from resorcess import *
from apt_manage import *
from flatpak_alias_list import *
from tabs.pop_ups import *
from tabs.system_tab_check import check_dselect
import subprocess


class BootLoaderTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")


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
            grub_config_path = '/etc/default/grub'
            timeout_style = None
            timeout_value = None
            
            try:
                with open(grub_config_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith('GRUB_TIMEOUT_STYLE'):
                            timeout_style = line.split('=')[1].strip().strip('"')
                        elif line.startswith('GRUB_TIMEOUT'):
                            timeout_value = line.split('=')[1].strip().strip('"')
                            if not timeout_value.isdigit():
                                print(f"Unerwarteter Wert für GRUB_TIMEOUT: '{timeout_value}'")
                                timeout_value = None

                if timeout_value is not None and timeout_value.isdigit():
                    return int(timeout_value)
                elif timeout_style == 'menu':
                    print("GRUB_TIMEOUT_STYLE ist auf 'menu' gesetzt. Verwende den Timeout-Wert dennoch.")
                    return 11  # Verwende den GRUB_TIMEOUT-Wert aus der Datei, wenn das Menü aktiv ist
                else:
                    print("GRUB_TIMEOUT_STYLE oder GRUB_TIMEOUT fehlen oder sind ungültig.")
                
            except FileNotFoundError:
                print("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")

            return 6  # Standardwert, falls kein Timeout gefunden wird

        def get_grub_timeout_style():
            grub_config_path = '/etc/default/grub'
            try:
                with open(grub_config_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith('GRUB_TIMEOUT_STYLE'):
                            return line.split('=')[1].strip().strip('"')
            except FileNotFoundError:
                print("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
            
            return 'menu'  # Standardwert, falls keine Einstellung gefunden wird

        def set_grub_timeout(timeout):
            grub_config_path = '/etc/default/grub'
            command = f"pkexec bash -c 'sed -i \"s/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT={timeout}/\" {grub_config_path} && update-grub'"
            
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB-Timeout erfolgreich auf {timeout} gesetzt.")
                print(result.stdout.decode('utf-8'))  # Ausgabe anzeigen
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB-Timeout: {e}")
                print(e.stderr.decode('utf-8'))  # Fehlerausgabe anzeigen

        def set_grub_timeout_style(style):
            grub_config_path = '/etc/default/grub'
            command = f"pkexec bash -c 'sed -i \"s/^GRUB_TIMEOUT_STYLE=.*/GRUB_TIMEOUT_STYLE={style}/\" {grub_config_path} && update-grub'"
            
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB_TIMEOUT_STYLE erfolgreich auf {style} gesetzt.")
                print(result.stdout.decode('utf-8'))  # Ausgabe anzeigen
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB_TIMEOUT_STYLE: {e}")
                print(e.stderr.decode('utf-8'))  # Fehlerausgabe anzeigen

        def update_grub_timeout():
            try:
                timeout = int(spinbox.get())
                if timeout < 0:
                    raise ValueError("Das Timeout darf nicht negativ sein.")
                set_grub_timeout(timeout)
            except ValueError as ve:
                print(f"Ungültige Eingabe: {ve}")

        def update_grub_menu():
            if toggle_var.get() == 1:
                set_grub_timeout_style("menu")
            else:
                set_grub_timeout_style("hidden")

                self.backup_frame = ttk.LabelFrame(
                    self,
                    text="Beschreibung",
                    padding=20
                )
        
        self.backup_frame = Frame(self)
        self.backup_frame.pack(pady=20, padx=20, fill=BOTH)

        self.backup_frame.columnconfigure(0, weight=1)
        self.backup_frame.rowconfigure(0, weight=1)


        self.backup_discription = ttk.Label(
            self.backup_frame,
            text="Hier steht ein schlauer Text über Grub und was die unteren optionen bewirken",
            justify="left",
            anchor=W,
        ).grid(row=0,column=0,columnspan=2,sticky="ew")



        self.recover_frame = ttk.LabelFrame(
            self,
            text="Grub Optionen",
            padding=50
        )
        self.recover_frame.pack(pady=20, padx=20, fill=BOTH)

        self.recover_frame.columnconfigure(0, weight=1)
        self.recover_frame.rowconfigure(0, weight=1)


        label = ttk.Label(self.recover_frame, text="Boot-Menü aktivieren",)
        label.grid(row=0,column=0,sticky="ew")

        # Toggle-Schalter für Boot-Menü
        toggle_var = tk.IntVar()
        current_style = get_grub_timeout_style()
        if current_style == "menu":
            toggle_var.set(1)
        else:
            toggle_var.set(0)

        toggle = ttk.Checkbutton(self.recover_frame, style='Switch.TCheckbutton',  variable=toggle_var, command=update_grub_menu)
        toggle.grid(row=0,column=2)


        # Label erstellen
        label = ttk.Label(self.recover_frame, text="GRUB Timeout setzen")
        label.grid(row=1,column=0,sticky="ew")

        # Timeout auslesen
        default_timeout = get_grub_timeout()

        # Spinbox erstellen
        spinbox = ttk.Spinbox(self.recover_frame, from_=6, to=60, increment=1)
        spinbox.set(default_timeout)
        spinbox.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        # Button zum Aktualisieren des GRUB-Timeouts
        button = ttk.Button(self.recover_frame, text="Auswählen", command=update_grub_timeout)
        button.grid(row=1,column=2)




        # Funktion, um den aktuellen GRUB_GFXMODE-Wert auszulesen
        def get_grub_gfxmode():
            grub_config_path = '/etc/default/grub'
            gfxmode = None
            gfxmode_commented = None
            
            try:
                with open(grub_config_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith('#GRUB_GFXMODE'):
                            gfxmode_commented = line.split('=')[1].strip().strip('"')
                        elif line.startswith('GRUB_GFXMODE'):
                            gfxmode = line.split('=')[1].strip().strip('"')

                if gfxmode:
                    return gfxmode  # Aktiver Wert wird zurückgegeben
                elif gfxmode_commented:
                    return "Standardwert"  # Auskommentierter Wert wird als "Standardwert" behandelt
                else:
                    return "Standardwert"  # Falls nicht vorhanden, Standardwert zurückgeben
            
            except FileNotFoundError:
                print("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
            
            return "Standardwert"

        # Funktion, um GRUB_GFXMODE zu setzen
        def set_grub_gfxmode(resolution):
            grub_config_path = '/etc/default/grub'
            
            if resolution == "Standardwert":
                # Wenn "Standardwert" ausgewählt ist, kommentiere GRUB_GFXMODE aus
                command = f"pkexec bash -c 'sed -i \"s/^GRUB_GFXMODE=.*/#GRUB_GFXMODE=640x480/\" {grub_config_path} && update-grub'"
            else:
                # Setze die ausgewählte Auflösung als GRUB_GFXMODE
                command = f"pkexec bash -c 'sed -i \"s/^#\\?GRUB_GFXMODE=.*/GRUB_GFXMODE={resolution}/\" {grub_config_path} && update-grub'"

            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB GFXMODE erfolgreich auf {resolution} gesetzt.")
                print(result.stdout.decode('utf-8'))  # Ausgabe anzeigen
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB GFXMODE: {e}")
                print(e.stderr.decode('utf-8'))  # Fehlerausgabe anzeigen

        # Funktion, um die aktuelle Auflösung zu speichern
        def update_gfxmode():
            resolution = combobox.get()
            set_grub_gfxmode(resolution)


        # Label für die Auflösung
        label = ttk.Label(self.recover_frame, text="GRUB Auflösung setzen")
        label.grid(row=2,column=0,sticky="ew")

        # Gängige Bildschirmauflösungen für GRUB
        resolutions = ["640x480", "800x600", "1024x768", "1280x1024", "1600x1200", "1920x1080", "2560x1440", "Standardwert"]

        # Combobox erstellen
        combobox = ttk.Combobox(self.recover_frame, values=resolutions, state="readonly")

        # Aktuellen GRUB_GFXMODE auslesen und in die Combobox setzen
        current_gfxmode = get_grub_gfxmode()
        combobox.set(current_gfxmode)
        combobox.grid(row=2,column=1,sticky="ew",padx=5,pady=5)

        # Button zum Anwenden der Auflösung
        button = ttk.Button(self.recover_frame, text="Auswählen", command=update_gfxmode)
        button.grid(row=2,column=2,sticky="ew")


