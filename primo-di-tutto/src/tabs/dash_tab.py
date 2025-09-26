import os
from os import popen
from tkinter import *
from tkinter import ttk
import tkinter as tk
import platform
import psutil
from time import strftime
import socket
import subprocess
from PIL import ImageTk, Image
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_manage import count_flatpaks
from tabs.pop_ups import *
from logger_config import setup_logger

logger = setup_logger(__name__)


class DashTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.system_icon = ImageTk.PhotoImage(
            Image.open(f"{application_path}/images/icons/logo.png")
        )
        if "dark" in theme_name or "Dark" in theme_name:

            self.distro_guide_logo_img = ImageTk.PhotoImage(
                Image.open(
                    f"{application_path}/images/icons/guideos_logo_dash_dark.png"
                )
            )
        else:

            self.distro_guide_logo_img = ImageTk.PhotoImage(
                Image.open(
                    f"{application_path}/images/icons/guideos_logo_dash_light.png"
                )
            )

        # Open the /proc/device-tree/model file for reading
        try:
            with open("/proc/device-tree/model", "r") as model_file:
                # Read and print the model information
                global pi_model
                pi_model = model_file.read().strip()
                logger.info(f"Raspberry Pi Model: {pi_model}")

        except FileNotFoundError:
            logger.info(
                "The /proc/device-tree/model file does not exist. You are not using a Pi"
            )
            pi_model = "Dein Computer"
        except Exception as e:
            logger.error("An error occurred:", str(e))

        # Create a frame to hold the progress bars
        self.usage_frame = ttk.LabelFrame(
            self,
            text="Systemnutzung",
        )
        self.usage_frame.pack(fill="x", pady=20, padx=60)
        # self.usage_frame.pack_propagate(0)

        # Create a frame to hold the progress bars
        self.useage_container = ttk.Frame(
            self.usage_frame,
        )

        self.useage_container.pack(fill="x")

        # Create a label and progress bar for CPU usage
        cpu_label = tk.Label(
            self.useage_container,
            text="CPU",
            font=("Sans", 12),
        )
        cpu_label.grid(row=1, column=0, sticky="nsew")

        self.cpu_percent = tk.Label(
            self.useage_container,
            text="0%",
            font=("Sans", 20),
        )
        self.cpu_percent.grid(row=0, column=0, sticky="nsew")

        # Create a label and progress bar for RAM usage
        ram_label = tk.Label(
            self.useage_container,
            text="RAM",
            font=("Sans", 12),
        )
        ram_label.grid(row=1, column=1, sticky="nsew")

        self.ram_percent = Label(
            self.useage_container,
            text="0%",
            font=("Sans", 20),
        )
        self.ram_percent.grid(row=0, column=1, sticky="nsew")

        # Create a label and progress bar for HDD usage
        hdd_label = tk.Label(
            self.useage_container,
            text="HDD",
            font=("Sans", 12),
        )
        hdd_label.grid(row=1, column=2, sticky="nsew")

        self.hdd_percent = tk.Label(
            self.useage_container,
            text="0%",
            font=("Sans", 20),
        )
        self.hdd_percent.grid(row=0, column=2, sticky="nsew")

        # Konfiguriere jede Spalte so, dass sie expandiert
        self.useage_container.grid_columnconfigure(0, weight=1)
        self.useage_container.grid_columnconfigure(1, weight=1)
        self.useage_container.grid_columnconfigure(2, weight=1)

        # Keine Gewichtung für die Zeilen, sodass sie nicht expandieren
        self.useage_container.grid_rowconfigure(0, weight=0)
        self.useage_container.grid_rowconfigure(1, weight=0)

        primo_logo_label = ttk.Label(self, image=self.system_icon)
        primo_logo_label.pack()

        self.os_info_frame = ttk.LabelFrame(
            self,
            text=pi_model,
            padding=20,
        )

        self.os_info_frame.pack(pady=20, fill="x", padx=60)

        self.info_frame_container = Frame(
            self.os_info_frame,
        )

        self.info_frame_container.pack(fill="x", expand=TRUE, anchor="n")

        self.info_frame_container.grid_columnconfigure(0, weight=1)
        self.info_frame_container.grid_columnconfigure(1, weight=1)
        self.info_frame_container.grid_columnconfigure(2, weight=1)
        self.info_frame_container.grid_columnconfigure(3, weight=1)

        self.info_frame_container.grid_rowconfigure(0, weight=0)
        self.info_frame_container.grid_rowconfigure(1, weight=0)

        # CPU Info Frame & Labels
        self.cpu_info_frame = ttk.LabelFrame(self.info_frame_container, text="CPU")
        self.cpu_info_frame.grid(column=0, row=0, sticky="nesw")

        self.cpu_model_label = tk.Label(self.cpu_info_frame, text="Model:")
        self.cpu_model_label.pack(anchor="w", padx=10)

        self.cpu_max_label = tk.Label(self.cpu_info_frame, text="Max:")
        self.cpu_max_label.pack(anchor="w", padx=10)

        self.cpu_current_label = tk.Label(self.cpu_info_frame, text="Current:")
        self.cpu_current_label.pack(anchor="w", padx=10)

        self.cpu_min_label = tk.Label(self.cpu_info_frame, text="Min:")
        self.cpu_min_label.pack(anchor="w", padx=10)

        # OS Info Frame & Labels
        self.os_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Betriebssystem",
        )
        self.os_label_frame.grid(column=0, row=1, rowspan=2, sticky="nesw")

        self.distro_label = tk.Label(self.os_label_frame, text="Distro:")
        self.distro_label.pack(anchor="w", padx=10)

        self.architecture_label = tk.Label(self.os_label_frame, text="Architecture:")
        self.architecture_label.pack(anchor="w", padx=10)

        self.kernel_label = tk.Label(self.os_label_frame, text="Kernel:")
        self.kernel_label.pack(anchor="w", padx=10)

        self.shell_label = tk.Label(self.os_label_frame, text="Shell:")
        self.shell_label.pack(anchor="w", padx=10)

        self.desktop_label = tk.Label(self.os_label_frame, text="Desktop:")
        self.desktop_label.pack(anchor="w", padx=10)

        self.window_manager_label = tk.Label(
            self.os_label_frame, text="Window Manager:"
        )
        self.window_manager_label.pack(anchor="w", padx=10)

        self.session_label = tk.Label(self.os_label_frame, text="Session:")
        self.session_label.pack(anchor="w", padx=10)

        self.resolution_label = tk.Label(self.os_label_frame, text="Resolution:")
        self.resolution_label.pack(anchor="w", padx=10)

        self.user_label = tk.Label(self.os_label_frame, text="User:")
        self.user_label.pack(anchor="w", padx=10)

        self.info_frame_column_2 = Frame(
            self.info_frame_container,
        )

        self.mem_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Arbeitsspeicher",
        )
        self.mem_label_frame.grid(column=1, row=2, sticky="nesw", padx=5)

        self.ram_total_label = tk.Label(self.mem_label_frame, text="Ram Total:")
        self.ram_total_label.pack(anchor="w", padx=10)

        self.ram_available_label = tk.Label(self.mem_label_frame, text="Ram Available:")
        self.ram_available_label.pack(anchor="w", padx=10)

        self.ram_used_label = tk.Label(self.mem_label_frame, text="Ram Used:")
        self.ram_used_label.pack(anchor="w", padx=10)

        self.swap_total_label = tk.Label(self.mem_label_frame, text="Swap Total:")
        self.swap_total_label.pack(anchor="w", padx=10)

        self.swap_free_label = tk.Label(self.mem_label_frame, text="Swap Free:")
        self.swap_free_label.pack(anchor="w", padx=10)

        self.swap_used_label = tk.Label(self.mem_label_frame, text="Swap Used:")
        self.swap_used_label.pack(anchor="w", padx=10)

        self.net_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Netzwerk",
        )
        self.net_label_frame.grid(column=1, row=0, sticky="nesw", padx=5)

        self.hostname_label = tk.Label(self.net_label_frame, text="Hostname:")
        self.hostname_label.pack(anchor="w", padx=10)

        self.ip_label = tk.Label(self.net_label_frame, text="IP:")
        self.ip_label.pack(anchor="w", padx=10)

        self.web_label = tk.Label(self.net_label_frame, text="Web:")
        self.web_label.pack(anchor="w", padx=10)

        self.down_label = tk.Label(self.net_label_frame, text="Down:")
        self.down_label.pack(anchor="w", padx=10)

        self.up_label = tk.Label(self.net_label_frame, text="Up:")
        self.up_label.pack(anchor="w", padx=10)

        self.disk_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Festplatte",
        )
        self.disk_label_frame.grid(column=1, row=1, sticky="nesw", padx=5)

        self.total_size_label = tk.Label(self.disk_label_frame, text="Total Size:")
        self.total_size_label.pack(anchor="w", padx=10)

        self.used_label = tk.Label(self.disk_label_frame, text="Used:")
        self.used_label.pack(anchor="w", padx=10)

        self.free_label = tk.Label(self.disk_label_frame, text="Free:")
        self.free_label.pack(anchor="w", padx=10)

        self.pakage_count_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Pakete",
        )
        self.pakage_count_label_frame.grid(column=2, columnspan=2, row=0, sticky="nesw")

        self.debian_label = tk.Label(self.pakage_count_label_frame, text="Debian:")
        self.debian_label.pack(anchor="w", padx=10)

        self.flatpak_label = tk.Label(self.pakage_count_label_frame, text="Flatpak:")
        self.flatpak_label.pack(anchor="w", padx=10)

        self.snap_label = tk.Label(self.pakage_count_label_frame, text="Snap:")
        self.snap_label.pack(anchor="w", padx=10)

        self.distro_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Grafikkarte",
        )

        self.distro_label_frame.grid(column=2, columnspan=2, row=1, sticky="nesw")

        # Ein label das den namen der Grafikkarte anzeigt
        self.gpu_name_label = Label(
            self.distro_label_frame, text=f"Modell: {self.get_gpu_model()}"
        )
        self.gpu_name_label.pack(anchor="w", padx=10)

        self.gpu_memory_label = Label(
            self.distro_label_frame, text=f"Speicher: {self.get_gpu_memory()}"
        )
        self.gpu_memory_label.pack(anchor="w", padx=10)

        # Label Frame der Look heißt
        self.look_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Erscheinungsbild",
        )
        self.look_label_frame.grid(column=2, columnspan=2, row=2, sticky="nesw")
        self.desktop_theme_label = Label(
            self.look_label_frame, text=f"Theme: {theme_name}"
        )
        self.desktop_theme_label.pack(anchor="w", padx=10)

        self.icon_theme_label = Label(
            self.look_label_frame, text=f"Icons: {self.get_icon_theme()}"
        )
        self.icon_theme_label.pack(anchor="w", padx=10)

        # label das den cursor theme anzeigt
        self.cursor_theme_label = Label(
            self.look_label_frame, text=f"Cursor: {self.get_cursor_theme()}"
        )
        self.cursor_theme_label.pack(anchor="w", padx=10)

        self.update_labels()

    def update_labels(self):

        # Screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # System information
        my_system = platform.uname()
        cpufreq = psutil.cpu_freq()
        swap = psutil.swap_memory()
        get_shell = os.environ["SHELL"]
        get_xdg_session = os.environ["XDG_SESSION_TYPE"]

        # CPU temperature retrieval
        cpu_temp = self.get_cpu_temperature()

        # Resource usage
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        hdd_usage = psutil.disk_usage("/").percent
        svmem = psutil.virtual_memory()

        # Update labels for CPU and memory
        self.update_cpu_labels(cpu_usage, cpu_temp, cpufreq)
        self.update_memory_labels(svmem, swap)

        # Network information
        lan_ip, down_rate, up_rate, web_state = self.get_network_info()

        # System hostname and IP
        self.hostname = socket.gethostname()
        self.IPAddr = socket.gethostbyname(self.hostname)
        self.hostname_label.configure(text=f"Hostname: {self.hostname}")
        self.ip_label.configure(text=f"IP: {lan_ip}")
        self.web_label.configure(text=f"Web: {web_state}")
        self.down_label.configure(text=f"Down: {down_rate} MB/s")
        self.up_label.configure(text=f"Up: {up_rate} MB/s")

        # Update OS information
        self.update_os_labels(my_system)
        # Theme dynamisch auslesen
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface gtk-theme",
                shell=True,
                universal_newlines=True,
            )
            current_theme = output.strip().strip("'")
        except Exception:
            current_theme = "N/A"
        self.desktop_theme_label.configure(text=f"Theme: {current_theme}")
        # Icon-Theme dynamisch auslesen
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface icon-theme",
                shell=True,
                universal_newlines=True,
            )
            current_icon_theme = output.strip().strip("'")
        except Exception:
            current_icon_theme = "N/A"
        self.icon_theme_label.configure(text=f"Icons: {current_icon_theme}")
        # Cursor-Theme dynamisch auslesen
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface cursor-theme",
                shell=True,
                universal_newlines=True,
            )
            current_cursor_theme = output.strip().strip("'")
        except Exception:
            current_cursor_theme = "N/A"
        self.cursor_theme_label.configure(text=f"Cursor: {current_cursor_theme}")
        # Update disk information
        self.update_disk_labels()

        # Update package information
        self.update_package_info()

        # Schedule the next update
        self.after(3000, self.update_labels)

    # Funktion die icon theme für cinnamon ausliest
    def get_icon_theme(self):
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface icon-theme",
                shell=True,
                universal_newlines=True,
            )
            icon_theme = output.strip().strip("'")
            return icon_theme
        except Exception:
            return "N/A"

    # Funktion die cursor theme für cinnamon ausliest
    def get_cursor_theme(self):
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface cursor-theme",
                shell=True,
                universal_newlines=True,
            )
            cursor_theme = output.strip().strip("'")
            return cursor_theme
        except Exception:
            return "N/A"

    def _clean_gpu_name(self, raw_name):
        """Bereinigt und kürzt GPU-Namen auf Hersteller + Modell."""
        if not raw_name or raw_name == "N/A":
            return raw_name
        
        name = raw_name.strip()
        
        # NVIDIA Bereinigung
        if "NVIDIA" in name or "GeForce" in name or "Quadro" in name or "Tesla" in name:
            # Entferne Herstellerinfo am Anfang
            name = name.replace("NVIDIA Corporation ", "")
            name = name.replace("NVIDIA ", "")
            
            # Vereinfache GeForce Namen
            if "GeForce" in name:
                # GeForce RTX 4090 -> NVIDIA RTX 4090
                import re
                match = re.search(r'GeForce\s+(.*?)(\s+\(|$)', name)
                if match:
                    model = match.group(1).strip()
                    return f"NVIDIA {model}"
            
            # Quadro/Tesla Namen
            if "Quadro" in name or "Tesla" in name:
                match = re.search(r'(Quadro|Tesla)\s+([^(\[]+)', name)
                if match:
                    return f"NVIDIA {match.group(1)} {match.group(2).strip()}"
            
            # Fallback für andere NVIDIA
            return f"NVIDIA {name}"
        
        # AMD/ATI Bereinigung  
        elif "AMD" in name or "ATI" in name or "Radeon" in name:
            # Entferne Herstellerinfo
            name = name.replace("Advanced Micro Devices, Inc. [AMD/ATI] ", "")
            name = name.replace("Advanced Micro Devices, Inc. ", "")
            name = name.replace("AMD/ATI ", "")
            name = name.replace("AMD ", "")
            
            # Radeon Namen vereinfachen
            if "Radeon" in name:
                import re
                # Suche nach Radeon + Modell ohne Zusatzinfo
                patterns = [
                    r'Radeon\s+(RX\s+\d+\s*\w*)',  # RX 5500 XT
                    r'Radeon\s+(R\d+\s+\d+)',      # R9 290
                    r'Radeon\s+(HD\s+\d+)',        # HD 7970
                    r'Radeon\s+(\w+\s*\d+)',       # Vega 64
                    r'Radeon\s+([^(\[/]+)'         # Fallback
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, name)
                    if match:
                        model = match.group(1).strip()
                        # Entferne Zusatzinfo in Klammern und schließende Klammern
                        model = re.sub(r'\s*[\(\[].*', '', model)
                        model = re.sub(r'[\)\]]+$', '', model)
                        return f"AMD Radeon {model}"
            
            # Andere AMD GPUs (RDNA, Vega etc.)
            import re
            match = re.search(r'(RDNA|Vega|Navi)\s*\d*\s*([^(\[\s/]+)?', name)
            if match:
                arch = match.group(1)
                model = match.group(2) if match.group(2) else ""
                return f"AMD {arch} {model}".strip()
            
            # Fallback für AMD
            clean_name = re.sub(r'\s*[\(\[].*', '', name)
            return f"AMD {clean_name}"
        
        # Intel Bereinigung
        elif "Intel" in name:
            name = name.replace("Intel Corporation ", "")
            name = name.replace("Intel(R) ", "")
            name = name.replace("Intel ", "")
            
            import re
            # Intel HD/UHD/Iris Graphics
            patterns = [
                r'(UHD Graphics\s*\d*)',
                r'(HD Graphics\s*\d*)',  
                r'(Iris\s+\w*\s*\d*)',
                r'(Arc\s+\w\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, name, re.IGNORECASE)
                if match:
                    model = match.group(1).strip()
                    return f"Intel {model}"
            
            # Fallback für Intel
            clean_name = re.sub(r'\s*[\(\[].*', '', name)
            return f"Intel {clean_name}"
        
        # Unbekannte Hersteller - versuche zu kürzen
        else:
            import re
            # Entferne Revision und Zusatzinfo
            name = re.sub(r'\s*\(rev\s+\w+\)', '', name)
            name = re.sub(r'\s*[\(\[].*', '', name)
            # Entferne übrig gebliebene schließende Klammern
            name = re.sub(r'[\)\]]+$', '', name).strip()
            
            # Wenn immer noch sehr lang, kürze auf ersten Teil
            if len(name) > 40:
                parts = name.split()
                if len(parts) > 3:
                    name = " ".join(parts[:3]) + "..."
            
            return name

    # Sehr robuste Funktion um das Modell der Grafikkarte auszulesen
    def get_gpu_model(self):
        """Sehr robuste Methode zur Erkennung des GPU-Modells für alle GPU-Typen."""
        
        # Methode 1: nvidia-smi für NVIDIA GPUs (beste Qualität)
        try:
            output = subprocess.check_output(
                "nvidia-smi --query-gpu=name --format=csv,noheader,nounits", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output and output != "N/A" and len(output) > 3:
                # Mehrere GPUs unterstützen
                gpu_names = [name.strip() for name in output.split('\n') if name.strip()]
                cleaned_names = [self._clean_gpu_name(name) for name in gpu_names[:3]]
                return " | ".join(cleaned_names)  # Max 3 GPUs
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 2: AMD rocm-smi für moderne AMD GPUs
        try:
            output = subprocess.check_output(
                "rocm-smi --showproductname", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output and "Card series" in output:
                lines = output.split('\n')
                gpu_models = []
                for line in lines:
                    if "Card series" in line and ":" in line:
                        model = line.split(":", 1)[1].strip()
                        if model and model != "N/A":
                            gpu_models.append(model)
                if gpu_models:
                    cleaned_models = [self._clean_gpu_name(model) for model in gpu_models[:2]]
                    return " | ".join(cleaned_models)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 3: lspci für universelle Hardware-Erkennung (zuverlässigste Methode)
        try:
            output = subprocess.check_output(
                "lspci | grep -iE 'vga|3d|display'", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            
            if output:
                lines = output.split('\n')
                gpu_models = []
                for line in lines:
                    if ":" in line:
                        # Extrahiere GPU-Info nach dem PCI-Slot
                        parts = line.split(":", 2)
                        if len(parts) >= 3:
                            gpu_info = parts[2].strip()
                        elif len(parts) == 2:
                            gpu_info = parts[1].strip()
                        else:
                            continue
                            
                        # Bereinige Controller-Bezeichnungen
                        cleaners = [
                            "VGA compatible controller: ",
                            "3D controller: ",
                            "Display controller: ",
                            "Audio device: "  # Manchmal fälschlich erkannt
                        ]
                        for cleaner in cleaners:
                            gpu_info = gpu_info.replace(cleaner, "")
                        
                        # Entferne Revision Info am Ende
                        gpu_info = gpu_info.split(" (rev ")[0]
                        
                        # Filtere offensichtliche Audio-Devices
                        if not any(audio_term in gpu_info.lower() for audio_term in ['audio', 'sound', 'hdmi audio']):
                            gpu_models.append(gpu_info.strip())
                
                if gpu_models:
                    # Entferne Duplikate aber behalte Reihenfolge
                    unique_models = []
                    for model in gpu_models:
                        if model not in unique_models:
                            unique_models.append(model)
                    # Bereinige die GPU-Namen
                    cleaned_models = [self._clean_gpu_name(model) for model in unique_models[:2]]
                    return " | ".join(cleaned_models)  # Max 2 GPUs
        except Exception:
            pass
        
        # Methode 4: glxinfo für OpenGL-Renderer-Info
        try:
            output = subprocess.check_output(
                "glxinfo | grep -E 'OpenGL renderer|Device:'", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            
            if output:
                lines = output.split('\n')
                for line in lines:
                    if "OpenGL renderer" in line and ":" in line:
                        renderer = line.split(":", 1)[1].strip()
                        # Bereinige Mesa/Driver-Info
                        renderer = renderer.replace("Mesa ", "").split(" (")[0]
                        if renderer and len(renderer) > 5:
                            return self._clean_gpu_name(renderer)
                    elif "Device:" in line and ":" in line:
                        device = line.split(":", 1)[1].strip().split(" (")[0]
                        if device and len(device) > 5:
                            return self._clean_gpu_name(device)
        except Exception:
            pass
        
        # Methode 5: /sys/class/drm für Kernel-DRM-Info
        try:
            import glob
            import os
            gpu_info_list = []
            
            for card_path in glob.glob('/sys/class/drm/card*/device'):
                try:
                    # Versuche vendor und device IDs zu lesen
                    vendor_path = os.path.join(card_path, 'vendor')
                    device_path = os.path.join(card_path, 'device')
                    
                    if os.path.exists(vendor_path) and os.path.exists(device_path):
                        with open(vendor_path, 'r') as f:
                            vendor_id = f.read().strip()
                        with open(device_path, 'r') as f:
                            device_id = f.read().strip()
                        
                        # Bekannte Vendor-IDs
                        vendor_names = {
                            '0x10de': 'NVIDIA',
                            '0x1002': 'AMD/ATI', 
                            '0x8086': 'Intel'
                        }
                        
                        vendor_name = vendor_names.get(vendor_id, f'Unknown({vendor_id})')
                        gpu_info_list.append(f"{vendor_name} GPU ({device_id})")
                except:
                    continue
            
            if gpu_info_list:
                cleaned_info = [self._clean_gpu_name(info) for info in gpu_info_list[:2]]
                return " | ".join(cleaned_info)
        except Exception:
            pass
        
        # Methode 6: lshw als letzter Ausweg
        try:
            output = subprocess.check_output(
                "lshw -C display -short 2>/dev/null", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            
            if output:
                lines = output.split('\n')[1:]  # Skip header
                gpu_models = []
                for line in lines:
                    if line.strip():
                        # lshw short format: H/W path Device Class Description
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            description = parts[3]
                            if description and "display" not in description.lower():
                                gpu_models.append(description)
                
                if gpu_models:
                    cleaned_models = [self._clean_gpu_name(model) for model in gpu_models[:2]]
                    return " | ".join(cleaned_models)
        except Exception:
            pass
        
        return "N/A"

    def get_gpu_memory(self):
        """Sehr robuste Methode zur Erkennung des GPU-Speichers für alle GPU-Typen."""
        
        # Methode 1: nvidia-smi für NVIDIA GPUs (Primärmethode)
        try:
            output = subprocess.check_output(
                "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output and output.replace('.', '').isdigit():
                return f"{output} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 2: nvidia-smi Alternative für NVIDIA
        try:
            output = subprocess.check_output(
                "nvidia-smi -q -d MEMORY | grep 'Total.*MiB' | head -1", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if "MiB" in output:
                import re
                match = re.search(r'(\d+)\s*MiB', output)
                if match:
                    return f"{match.group(1)} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 3: glxinfo für alle OpenGL-kompatiblen GPUs (AMD, Intel, NVIDIA)
        try:
            output = subprocess.check_output(
                "glxinfo | grep -E 'Video memory|Dedicated video memory'", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output:
                import re
                # Suche nach verschiedenen Formaten
                match = re.search(r'(\d+)\s*MB', output)
                if match:
                    return f"{match.group(1)}MB"
                match = re.search(r':\s*(\d+MB)', output)
                if match:
                    return match.group(1)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 4: AMD-spezifische rocm-smi
        try:
            output = subprocess.check_output(
                "rocm-smi --showmeminfo vram --csv", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output and "vram" in output.lower():
                lines = output.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) > 1:
                            mem_str = parts[1].strip()
                            import re
                            match = re.search(r'(\d+)', mem_str)
                            if match:
                                return f"{match.group(1)} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Methode 5: /sys/class/drm für moderne Linux-Systeme
        try:
            import glob
            for card_path in glob.glob('/sys/class/drm/card*/device/mem_info_vram_total'):
                with open(card_path, 'r') as f:
                    vram_bytes = int(f.read().strip())
                    vram_mb = vram_bytes // (1024 * 1024)
                    if vram_mb > 0:
                        return f"{vram_mb} MB"
        except (FileNotFoundError, ValueError, PermissionError):
            pass
        
        # Methode 6: lspci + /proc/meminfo für integrierte GPUs
        try:
            output = subprocess.check_output(
                "lspci | grep -i 'vga\\|display'", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            )
            # Nur für eindeutig integrierte GPUs schätzen
            if any(term in output.lower() for term in ['intel.*hd', 'intel.*uhd', 'intel.*iris', 'amd.*vega.*[0-9]']):
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            total_mem = int(line.split()[1]) // 1024  # KB zu MB
                            # Schätze GPU-Memory (typisch 512MB-2GB für integrierte)
                            estimated_gpu_mem = min(2048, max(512, total_mem // 8))
                            return f"~{estimated_gpu_mem} MB (geschätzt)"
        except Exception:
            pass
        
        # Methode 7: dmesg für Boot-Zeit GPU-Informationen
        try:
            output = subprocess.check_output(
                "dmesg | grep -iE '(vram|memory).*[0-9]+.*mb' | grep -i gpu | tail -1", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output:
                import re
                match = re.search(r'(\d+)\s*mb', output.lower())
                if match:
                    return f"{match.group(1)} MB"
        except Exception:
            pass
        
        # Methode 8: Fallback über lshw (wenn installiert)
        try:
            output = subprocess.check_output(
                "lshw -C display 2>/dev/null | grep -i 'size.*mb'", 
                shell=True, universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
            if output:
                import re
                match = re.search(r'(\d+)\s*mb', output.lower())
                if match:
                    return f"{match.group(1)} MB"
        except Exception:
            pass
        
        return "N/A"

    def get_guideo_version(self):
        # es soll ein der datei /etc/guideo-version ausgelsen werden
        try:
            with open("/etc/guideos-version", "r") as file:
                version = file.read().strip()
            return version
        except FileNotFoundError:
            logger.error("Die Datei /etc/guideo-version wurde nicht gefunden.")
            return "N/A"

    def get_cpu_temperature(self):
        """Get the CPU temperature."""
        try:
            cpu_temp = psutil.sensors_temperatures()
            return round(cpu_temp["cpu_thermal"][0][1])
        except:
            return "N/A"

    def update_cpu_labels(self, cpu_usage, cpu_temp, cpufreq):
        """Update CPU-related labels."""
        self.cpu_percent["text"] = f"{cpu_usage}%"
        # self.cpu_temp_percent["text"] = f"{cpu_temp}°C"
        self.cpu_model_label.configure(text=f"Modell: {self.get_cpu_model_name()}")
        self.cpu_max_label.configure(text=f"Max: {cpufreq.max:.0f} Mhz")
        self.cpu_current_label.configure(text=f"Aktuell: {cpufreq.current:.0f} Mhz")
        self.cpu_min_label.configure(text=f"Min: {cpufreq.min:.0f} Mhz")

    def update_memory_labels(self, svmem, swap):
        """Update memory-related labels."""
        self.ram_percent["text"] = f"{svmem.percent}%"
        self.ram_total_label.configure(
            text=f"RAM Total: {self.get_size(svmem.total)}"
        )
        self.ram_available_label.configure(
            text=f"RAM Frei: {self.get_size(svmem.available)}"
        )
        self.ram_used_label.configure(
            text=f"RAM Genutzt: {self.get_size(svmem.used)}"
        )
        self.swap_total_label.configure(
            text=f"Swap Total: {self.get_size(swap.total)}"
        )
        self.swap_free_label.configure(text=f"Swap Frei: {self.get_size(swap.free)}")
        self.swap_used_label.configure(
            text=f"Swap Genutzt: {self.get_size(swap.used)}"
        )

    def update_disk_labels(self):
        """Update disk-related labels."""
        hdd_usage = psutil.disk_usage("/").percent
        obj_Disk = psutil.disk_usage("/")
        self.total_size_label.configure(
            text=f"Gesamtgröße: {obj_Disk.total / (2**30):.2f} GB"
        )
        self.used_label.configure(text=f"Genutzt: {obj_Disk.used / (2**30):.2f} GB")
        self.free_label.configure(text=f"Frei: {obj_Disk.free / (2**30):.2f} GB")
        self.hdd_percent.configure(text=f"{hdd_usage}%")

    def get_network_info(self):
        """Get network-related information."""
        try:
            local_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            local_ip.connect(("8.8.8.8", 80))
            lan_ip = local_ip.getsockname()[0]
            net_io_counters = psutil.net_io_counters()
            down_rate = round(net_io_counters.bytes_recv / 1024 / 1024, 2)
            up_rate = round(net_io_counters.bytes_sent / 1024 / 1024, 2)
            web_state = "Verbunden"
        except (socket.error, socket.gaierror) as e:
            logger.error(f"Failed to determine local IP address: {e}")
            lan_ip = None
            down_rate = "-"
            up_rate = "-"
            web_state = "Nicht verbunden"

        return lan_ip, down_rate, up_rate, web_state

    def update_os_labels(self, my_system):
        """Update OS-related labels."""
        self.distro_label.configure(text=f"Distro: {self.get_guideo_version()}")
        self.architecture_label.configure(text=f"Architektur: {os_arch_output}")
        self.kernel_label.configure(text=f"Kernel: {my_system.release}")
        self.shell_label.configure(text=f"Shell: {os.environ['SHELL']}")
        self.desktop_label.configure(text=f"Desktop: {get_desktop_environment()}")
        self.window_manager_label.configure(
            text=f"Window Manager: {self.get_window_manager()}"
        )
        self.session_label.configure(text=f"Session: {os.environ['XDG_SESSION_TYPE']}")
        self.resolution_label.configure(
            text=f"Auflösung: {self.winfo_screenwidth()}x{self.winfo_screenheight()}"
        )
        self.user_label.configure(text=f"User: {user}")

    def update_package_info(self):
        """Update package-related information."""
        self.debian_label.configure(text=f"Debian: {deb_counted[:-1]}")
        self.flatpak_label.configure(text=f"Flatpak: {count_flatpaks()}")
        self.snap_label.configure(text=f"Snap: {snap_package_count}")

    def get_size(self, bytes, suffix="B"):
        """Scale bytes to its proper format."""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def get_cpu_model_name(self):
        """Get the CPU model name."""
        command = "lscpu | grep -E 'Model name|Modellname' | awk -F ': ' '{gsub(/^[ \t]+|[ \t]+$/, \"\", $2); print $2}'"
        try:
            output = subprocess.check_output(
                command, shell=True, universal_newlines=True
            )
            return output.strip()
        except subprocess.CalledProcessError:
            return "N/A"

    def get_window_manager(self):
        """Get the name of the window manager."""
        try:
            result = subprocess.run(
                ["wmctrl", "-m"], capture_output=True, text=True, check=True
            )
            output_lines = result.stdout.strip().split("\n")
            for line in output_lines:
                if line.startswith("Name: "):
                    return line.split("Name: ")[1]
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running wmctrl: {e}")

        return None
