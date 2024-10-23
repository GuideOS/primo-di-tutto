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
                    return 11  
                else:
                    print("GRUB_TIMEOUT_STYLE oder GRUB_TIMEOUT fehlen oder sind ungültig.")
                
            except FileNotFoundError:
                print("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")

            return 6  

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
            
            return 'menu'  

        def set_grub_timeout(timeout):
            grub_config_path = '/etc/default/grub'
            command = f"pkexec bash -c 'sed -i \"s/^GRUB_TIMEOUT=.*/GRUB_TIMEOUT={timeout}/\" {grub_config_path} && update-grub'"
            
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB-Timeout erfolgreich auf {timeout} gesetzt.")
                print(result.stdout.decode('utf-8'))  
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB-Timeout: {e}")
                print(e.stderr.decode('utf-8'))  

        def set_grub_timeout_style(style):
            grub_config_path = '/etc/default/grub'
            command = f"pkexec bash -c 'sed -i \"s/^GRUB_TIMEOUT_STYLE=.*/GRUB_TIMEOUT_STYLE={style}/\" {grub_config_path} && update-grub'"
            
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB_TIMEOUT_STYLE erfolgreich auf {style} gesetzt.")
                print(result.stdout.decode('utf-8'))  
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB_TIMEOUT_STYLE: {e}")
                print(e.stderr.decode('utf-8'))  

        def update_grub_timeout():
            try:
                timeout = int(grub_timeout_spinbox.get())
                if timeout < 0:
                    raise ValueError("Das Timeout darf nicht negativ sein.")
                set_grub_timeout(timeout)
            except ValueError as ve:
                print(f"Ungültige Eingabe: {ve}")

        def update_grub_menu():
            if grub_state_toggle_var.get() == 1:
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


        grub_state_label = ttk.Label(self.recover_frame, text="Boot-Menü aktivieren",)
        grub_state_label.grid(row=0,column=0,sticky="ew")

        grub_state_toggle_var = tk.IntVar()
        current_style = get_grub_timeout_style()
        if current_style == "menu":
            grub_state_toggle_var.set(1)
        else:
            grub_state_toggle_var.set(0)

        grub_state_toggle = ttk.Checkbutton(self.recover_frame, style='Switch.TCheckbutton',  variable=grub_state_toggle_var, command=update_grub_menu)
        grub_state_toggle.grid(row=0,column=2)


        grub_timeout_label = ttk.Label(self.recover_frame, text="GRUB Timeout setzen")
        grub_timeout_label.grid(row=1,column=0,sticky="ew")

        default_timeout = get_grub_timeout()

        grub_timeout_spinbox = ttk.Spinbox(self.recover_frame, from_=6, to=60, increment=1)
        grub_timeout_spinbox.set(default_timeout)
        grub_timeout_spinbox.grid(row=1,column=1,padx=5,pady=5, sticky="ew")

        grub_timeout_button = ttk.Button(self.recover_frame, text="Auswählen", command=update_grub_timeout)
        grub_timeout_button.grid(row=1,column=2)




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
                    return gfxmode  
                elif gfxmode_commented:
                    return "Standardwert"  
                else:
                    return "Standardwert"  
            
            except FileNotFoundError:
                print("Die GRUB-Konfigurationsdatei wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
            
            return "Standardwert"

        def set_grub_gfxmode(resolution):
            grub_config_path = '/etc/default/grub'
            
            if resolution == "Standardwert":
                command = f"pkexec bash -c 'sed -i \"s/^GRUB_GFXMODE=.*/#GRUB_GFXMODE=640x480/\" {grub_config_path} && update-grub'"
            else:
                command = f"pkexec bash -c 'sed -i \"s/^#\\?GRUB_GFXMODE=.*/GRUB_GFXMODE={resolution}/\" {grub_config_path} && update-grub'"

            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"GRUB GFXMODE erfolgreich auf {resolution} gesetzt.")
                print(result.stdout.decode('utf-8'))  
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Setzen des GRUB GFXMODE: {e}")
                print(e.stderr.decode('utf-8'))  

        def update_gfxmode():
            resolution = grub_res_combobox.get()
            set_grub_gfxmode(resolution)


        grub_res_label = ttk.Label(self.recover_frame, text="GRUB Auflösung setzen")
        grub_res_label.grid(row=2,column=0,sticky="ew")

        resolutions = ["640x480", "800x600", "1024x768", "1280x1024", "1600x1200", "1920x1080", "2560x1440", "Standardwert"]

        grub_res_combobox = ttk.Combobox(self.recover_frame, values=resolutions, state="readonly")

        current_gfxmode = get_grub_gfxmode()
        grub_res_combobox.set(current_gfxmode)
        grub_res_combobox.grid(row=2,column=1,sticky="ew",padx=5,pady=5)

        grub_res_button = ttk.Button(self.recover_frame, text="Auswählen", command=update_gfxmode)
        grub_res_button.grid(row=2,column=2,sticky="ew")


