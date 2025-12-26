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
import threading
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
        theme_name_val = get_theme_cached()
        if "dark" in theme_name_val or "Dark" in theme_name_val:

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

        self.useage_container.grid_columnconfigure(2, weight=1)

        # Configure each column to expand
        self.useage_container.grid_columnconfigure(0, weight=1)
        self.useage_container.grid_columnconfigure(1, weight=1)
        self.useage_container.grid_columnconfigure(2, weight=1)

        # No weighting for rows, so they don't expand
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

        # A label that displays the graphics card name
        self.gpu_name_label = Label(
            self.distro_label_frame, text=f"Modell: {self.get_gpu_model()}"
        )
        self.gpu_name_label.pack(anchor="w", padx=10)

        self.gpu_memory_label = Label(
            self.distro_label_frame, text=f"Speicher: {self.get_gpu_memory()}"
        )
        self.gpu_memory_label.pack(anchor="w", padx=10)

        # Label Frame for appearance/look
        self.look_label_frame = ttk.LabelFrame(
            self.info_frame_container,
            text="Erscheinungsbild",
        )
        self.look_label_frame.grid(column=2, columnspan=2, row=2, sticky="nesw")
        self.theme_label = ttk.Label(
            self.look_label_frame, text=f"Theme: {get_theme_cached()}"
        )
        self.theme_label.pack(anchor="w", padx=10)

        self.icon_theme_label = Label(
            self.look_label_frame, text=f"Icons: {self.get_icon_theme()}"
        )
        self.icon_theme_label.pack(anchor="w", padx=10)

        # Label that displays the cursor theme
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
        # Read theme dynamically
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface gtk-theme",
                shell=True,
                universal_newlines=True,
            )
            current_theme = output.strip().strip("'")
        except Exception:
            current_theme = "N/A"
        self.theme_label.configure(text=f"Theme: {current_theme}")
        # Read icon theme dynamically
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
        # Read cursor theme dynamically
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

    # Function that reads icon theme for cinnamon
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

    # Function that reads cursor theme for cinnamon
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

    def killProcess(self, process):
        """Kill a process if it times out."""
        try:
            process.terminate()
            process.wait(timeout=1)
        except:
            try:
                process.kill()
            except:
                pass

    def getProcessOut(self, command):
        """Execute a command and return its output lines with timeout protection."""
        timeout = 2.0  # Timeout for any subprocess before aborting it

        lines = []
        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, text=True)
            timer = threading.Timer(timeout, self.killProcess, [p])
            timer.start()

            while True:
                line = p.stdout.readline()
                if not line:
                    break
                if line != "":
                    lines.append(line.strip())

            timer.cancel()
            p.wait()

        except Exception as e:
            logger.error(f"Error in getProcessOut: {e}")

        return lines

    def shorten_gpu_name(self, gpu_name):
        """Shortens GPU names for better display."""

        # Remove common unnecessary terms at the beginning
        replacements_start = [
            ("Advanced Micro Devices, Inc. [AMD/ATI] ", "AMD "),
            ("NVIDIA Corporation ", "NVIDIA "),
            ("Intel Corporation ", "Intel "),
            ("ATI Technologies Inc ", "AMD "),
        ]

        shortened = gpu_name
        for old, new in replacements_start:
            if shortened.startswith(old):
                shortened = shortened.replace(old, new, 1)
                break

        # Remove unnecessary terms
        remove_terms = [
            "Corporation",
            "Technologies Inc",
            "Limited",
            "Ltd",
            "Inc.",
            ", Inc",
        ]

        for term in remove_terms:
            shortened = shortened.replace(term, "")

        # Special handling for AMD Radeon
        if "AMD" in shortened and "Radeon" in shortened:
            # Extract the important part: "AMD Radeon RX 6700 XT" etc.
            import re

            match = re.search(r"AMD.*(Radeon.*?)(?:\s*\[|$)", shortened)
            if match:
                shortened = f"AMD {match.group(1)}"

        # Special handling for NVIDIA GeForce
        elif "NVIDIA" in shortened and (
            "GeForce" in shortened or "GTX" in shortened or "RTX" in shortened
        ):
            import re

            match = re.search(
                r"NVIDIA.*(GeForce.*?|GTX.*?|RTX.*?)(?:\s*\[|$)", shortened
            )
            if match:
                shortened = f"NVIDIA {match.group(1)}"

        # Special handling for Intel
        elif "Intel" in shortened:
            import re

            match = re.search(r"Intel.*(HD.*?|UHD.*?|Iris.*?)(?:\s*\[|$)", shortened)
            if match:
                shortened = f"Intel {match.group(1)}"

        # Remove square brackets and everything after
        if "[" in shortened:
            shortened = shortened.split("[")[0].strip()

        # Remove remaining special characters
        import re

        shortened = re.sub(r"[^\w\s\-\.]", "", shortened)

        # Remove multiple spaces
        shortened = " ".join(shortened.split())

        # Remove spaces at beginning/end
        shortened = shortened.strip()

        # Shorten only if really too long (50 characters)
        if len(shortened) > 50:
            shortened = shortened[:47] + "..."

        return shortened

    # Very robust function to read the graphics card model
    def get_gpu_model(self):
        cards = {}
        count = 0
        envpath = os.environ["PATH"]
        os.environ["PATH"] = envpath + ":/usr/local/sbin:/usr/sbin:/sbin"

        try:
            for card in self.getProcessOut("lspci"):
                for prefix in [
                    "VGA compatible controller:",
                    "3D controller:",
                    "Display controller:",
                ]:
                    if prefix in card:
                        cardName = card.split(prefix)[1].split("(rev")[0].strip()
                        # Shorten GPU names for better display
                        cardName = self.shorten_gpu_name(cardName)
                        cards[count] = cardName
                        count += 1
        except Exception as e:
            logger.error(f"Error getting GPU model: {e}")
            cards[0] = "N/A"

        os.environ["PATH"] = envpath

        # Return the first GPU or "N/A" if none found
        gpu_model = cards.get(0, "N/A")
        # print(f"GPU Model detected: {gpu_model}")
        return gpu_model

    def get_gpu_memory(self):
        """Very robust method for detecting GPU memory for all GPU types."""

        # Method 1: nvidia-smi for NVIDIA GPUs (primary method)
        try:
            output = subprocess.check_output(
                "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output and output.replace(".", "").isdigit():
                return f"{output} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Method 2: nvidia-smi alternative for NVIDIA
        try:
            output = subprocess.check_output(
                "nvidia-smi -q -d MEMORY | grep 'Total.*MiB' | head -1",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if "MiB" in output:
                import re

                match = re.search(r"(\d+)\s*MiB", output)
                if match:
                    return f"{match.group(1)} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Method 3: glxinfo for all OpenGL-compatible GPUs (AMD, Intel, NVIDIA)
        try:
            output = subprocess.check_output(
                "glxinfo | grep -E 'Video memory|Dedicated video memory'",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output:
                import re

                # Search for various formats
                match = re.search(r"(\d+)\s*MB", output)
                if match:
                    return f"{match.group(1)}MB"
                match = re.search(r":\s*(\d+MB)", output)
                if match:
                    return match.group(1)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Method 4: AMD-specific rocm-smi
        try:
            output = subprocess.check_output(
                "rocm-smi --showmeminfo vram --csv",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output and "vram" in output.lower():
                lines = output.split("\n")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(",")
                        if len(parts) > 1:
                            mem_str = parts[1].strip()
                            import re

                            match = re.search(r"(\d+)", mem_str)
                            if match:
                                return f"{match.group(1)} MB"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Method 5: /sys/class/drm for modern Linux systems
        try:
            import glob

            for card_path in glob.glob(
                "/sys/class/drm/card*/device/mem_info_vram_total"
            ):
                with open(card_path, "r") as f:
                    vram_bytes = int(f.read().strip())
                    vram_mb = vram_bytes // (1024 * 1024)
                    if vram_mb > 0:
                        return f"{vram_mb} MB"
        except (FileNotFoundError, ValueError, PermissionError):
            pass

        # Method 6: lspci + /proc/meminfo for integrated GPUs
        try:
            output = subprocess.check_output(
                "lspci | grep -i 'vga\\|display'",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )
            # Only estimate for clearly integrated GPUs
            if any(
                term in output.lower()
                for term in [
                    "intel.*hd",
                    "intel.*uhd",
                    "intel.*iris",
                    "amd.*vega.*[0-9]",
                ]
            ):
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            total_mem = int(line.split()[1]) // 1024  # KB to MB
                            # Estimate GPU memory (typically 512MB-2GB for integrated)
                            estimated_gpu_mem = min(2048, max(512, total_mem // 8))
                            return f"~{estimated_gpu_mem} MB (geschätzt)"
        except Exception:
            pass

        # Method 7: dmesg for boot-time GPU information
        try:
            output = subprocess.check_output(
                "dmesg | grep -iE '(vram|memory).*[0-9]+.*mb' | grep -i gpu | tail -1",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output:
                import re

                match = re.search(r"(\d+)\s*mb", output.lower())
                if match:
                    return f"{match.group(1)} MB"
        except Exception:
            pass

        # Method 8: Fallback via lshw (if installed)
        try:
            output = subprocess.check_output(
                "lshw -C display 2>/dev/null | grep -i 'size.*mb'",
                shell=True,
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if output:
                import re

                match = re.search(r"(\d+)\s*mb", output.lower())
                if match:
                    return f"{match.group(1)} MB"
        except Exception:
            pass

        return "N/A"

    def get_guideo_version(self):
        # Read from the file /etc/guideo-version
        try:
            with open("/etc/guideos-version", "r") as file:
                version = file.read().strip()
            return version
        except FileNotFoundError:
            logger.error("The file /etc/guideo-version was not found.")
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
        self.ram_total_label.configure(text=f"RAM Total: {self.get_size(svmem.total)}")
        self.ram_available_label.configure(
            text=f"RAM Frei: {self.get_size(svmem.available)}"
        )
        self.ram_used_label.configure(text=f"RAM Genutzt: {self.get_size(svmem.used)}")
        self.swap_total_label.configure(text=f"Swap Total: {self.get_size(swap.total)}")
        self.swap_free_label.configure(text=f"Swap Frei: {self.get_size(swap.free)}")
        self.swap_used_label.configure(text=f"Swap Genutzt: {self.get_size(swap.used)}")

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
        self.desktop_label.configure(
            text=f"Desktop: {get_desktop_environment()} {get_cinnamon_version()}"
        )
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
        from apt_manage import get_deb_count
        from snap_manage import get_snap_package_count

        self.debian_label.configure(text=f"Debian: {get_deb_count()}")
        self.flatpak_label.configure(text=f"Flatpak: {count_flatpaks()}")
        self.snap_label.configure(text=f"Snap: {get_snap_package_count()}")

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
