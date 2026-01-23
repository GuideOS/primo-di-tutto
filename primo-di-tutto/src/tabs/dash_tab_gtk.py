#!/usr/bin/python3

import gi
from gi.repository import Gtk, GLib
import platform
import psutil
import socket
import os
import threading
import subprocess
from resorcess import application_path
from hwinfo import gpu_info, gpu_memory, gpu_driver

class DashTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # Systemlogo als Gtk.Picture ohne Scrollbar
        logo_path = f"{application_path}/images/icons/logo.png"
        picture = Gtk.Picture.new_for_filename(logo_path)
        picture.set_keep_aspect_ratio(True)
        picture.set_can_shrink(False)
        picture.set_hexpand(False)
        picture.set_vexpand(False)
        # In eine zentrierte Box legen, damit es nicht skaliert
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        logo_box.set_halign(Gtk.Align.CENTER)
        logo_box.set_valign(Gtk.Align.START)
        logo_box.append(picture)
        self.append(logo_box)

        # Hauptgrid
        grid = Gtk.Grid(row_spacing=8, column_spacing=8)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.append(grid)

        # Systemnutzung (oben, über beide Spalten)
        usage_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("utilities-system-monitor")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Systemnutzung")
        label_box.append(label)
        usage_frame.set_label_widget(label_box)
        usage_frame.set_margin_top(8)
        usage_frame.set_margin_bottom(8)
        usage_frame.set_margin_start(8)
        usage_frame.set_margin_end(8)
        usage_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        usage_box.set_margin_top(12)
        usage_box.set_margin_bottom(12)
        usage_box.set_margin_start(12)
        usage_box.set_margin_end(12)
        usage_frame.set_child(usage_box)
        # CPU
        cpu_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        cpu_label = Gtk.Label(label="CPU")
        cpu_label.set_xalign(0.5)
        self.cpu_value_label = Gtk.Label(label="0%")
        self.cpu_value_label.set_xalign(0.5)
        self.cpu_value_label.set_markup('<span size="20000" weight="bold">0%</span>')
        cpu_vbox.append(cpu_label)
        cpu_vbox.append(self.cpu_value_label)
        cpu_vbox.set_hexpand(True)
        usage_box.append(cpu_vbox)

        # RAM
        ram_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        ram_label = Gtk.Label(label="RAM")
        ram_label.set_xalign(0.5)
        self.ram_value_label = Gtk.Label(label="0%")
        self.ram_value_label.set_xalign(0.5)
        self.ram_value_label.set_markup('<span size="20000" weight="bold">0%</span>')
        ram_vbox.append(ram_label)
        ram_vbox.append(self.ram_value_label)
        ram_vbox.set_hexpand(True)
        usage_box.append(ram_vbox)

        # HDD
        hdd_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        hdd_label = Gtk.Label(label="HDD")
        hdd_label.set_xalign(0.5)
        self.hdd_value_label = Gtk.Label(label="0%")
        self.hdd_value_label.set_xalign(0.5)
        self.hdd_value_label.set_markup('<span size="20000" weight="bold">0%</span>')
        hdd_vbox.append(hdd_label)
        hdd_vbox.append(self.hdd_value_label)
        hdd_vbox.set_hexpand(True)
        usage_box.append(hdd_vbox)
        grid.attach(usage_frame, 0, 0, 3, 1)

        # Linke Spalte
        info_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("computer")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Systeminfo")
        label_box.append(label)
        info_frame.set_label_widget(label_box)
        info_frame.set_margin_top(8)
        info_frame.set_margin_bottom(8)
        info_frame.set_margin_start(8)
        info_frame.set_margin_end(8)
        info_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        info_vbox.set_margin_top(12)
        info_vbox.set_margin_bottom(12)
        info_vbox.set_margin_start(12)
        info_vbox.set_margin_end(12)
        info_frame.set_child(info_vbox)
        self.hostname_label = Gtk.Label(label="Hostname: ...")
        self.hostname_label.set_xalign(0)
        self.ip_label = Gtk.Label(label="IP: ...")
        self.ip_label.set_xalign(0)
        self.distro_label = Gtk.Label(label="Distro: ...")
        self.distro_label.set_xalign(0)
        self.kernel_label = Gtk.Label(label="Kernel: ...")
        self.kernel_label.set_xalign(0)
        self.user_label = Gtk.Label(label="User: ...")
        self.user_label.set_xalign(0)
        self.resolution_label = Gtk.Label(label="Resolution: ...")
        self.resolution_label.set_xalign(0)
        self.shell_label = Gtk.Label(label="Shell: ...")
        self.shell_label.set_xalign(0)
        self.desktop_label = Gtk.Label(label="Desktop: ...")
        self.desktop_label.set_xalign(0)
        self.window_manager_label = Gtk.Label(label="Window Manager: ...")
        self.window_manager_label.set_xalign(0)
        info_vbox.append(self.hostname_label)
        info_vbox.append(self.ip_label)
        info_vbox.append(self.distro_label)
        info_vbox.append(self.kernel_label)
        info_vbox.append(self.user_label)
        info_vbox.append(self.resolution_label)
        info_vbox.append(self.shell_label)
        info_vbox.append(self.desktop_label)
        info_vbox.append(self.window_manager_label)
        grid.attach(info_frame, 0, 1, 1, 2)

        theme_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("preferences-desktop-theme")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Erscheinungsbild")
        label_box.append(label)
        theme_frame.set_label_widget(label_box)
        theme_frame.set_margin_top(8)
        theme_frame.set_margin_bottom(8)
        theme_frame.set_margin_start(8)
        theme_frame.set_margin_end(8)
        theme_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        theme_box.set_margin_top(12)
        theme_box.set_margin_bottom(12)
        theme_box.set_margin_start(12)
        theme_box.set_margin_end(12)
        theme_frame.set_child(theme_box)
        self.desktop_theme_label = Gtk.Label(label="Theme: ...")
        self.desktop_theme_label.set_xalign(0)
        self.icon_theme_label = Gtk.Label(label="Icons: ...")
        self.icon_theme_label.set_xalign(0)
        self.cursor_theme_label = Gtk.Label(label="Cursor: ...")
        self.cursor_theme_label.set_xalign(0)
        theme_box.append(self.desktop_theme_label)
        theme_box.append(self.icon_theme_label)
        theme_box.append(self.cursor_theme_label)
        grid.attach(theme_frame, 0, 3, 1, 1)

        # RAM Frame
        ram_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("memory")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Arbeitsspeicher")
        label_box.append(label)
        ram_frame.set_label_widget(label_box)
        ram_frame.set_margin_top(8)
        ram_frame.set_margin_bottom(8)
        ram_frame.set_margin_start(8)
        ram_frame.set_margin_end(8)
        ram_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        ram_box.set_margin_top(12)
        ram_box.set_margin_bottom(12)
        ram_box.set_margin_start(12)
        ram_box.set_margin_end(12)
        ram_frame.set_child(ram_box)
        self.ram_total_label = Gtk.Label(label="RAM Total: ...")
        self.ram_total_label.set_xalign(0)
        self.ram_available_label = Gtk.Label(label="RAM Frei: ...")
        self.ram_available_label.set_xalign(0)
        self.ram_used_label = Gtk.Label(label="RAM Genutzt: ...")
        self.ram_used_label.set_xalign(0)
        ram_box.append(self.ram_total_label)
        ram_box.append(self.ram_available_label)
        ram_box.append(self.ram_used_label)
        grid.attach(ram_frame, 1, 3, 1, 1)

        # Swap Frame
        swap_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("drive-harddisk")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Swap")
        label_box.append(label)
        swap_frame.set_label_widget(label_box)
        swap_frame.set_margin_top(8)
        swap_frame.set_margin_bottom(8)
        swap_frame.set_margin_start(8)
        swap_frame.set_margin_end(8)
        swap_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        swap_box.set_margin_top(12)
        swap_box.set_margin_bottom(12)
        swap_box.set_margin_start(12)
        swap_box.set_margin_end(12)
        swap_frame.set_child(swap_box)
        self.swap_total_label = Gtk.Label(label="Swap Total: ...")
        self.swap_total_label.set_xalign(0)
        self.swap_free_label = Gtk.Label(label="Swap Frei: ...")
        self.swap_free_label.set_xalign(0)
        self.swap_used_label = Gtk.Label(label="Swap Genutzt: ...")
        self.swap_used_label.set_xalign(0)
        swap_box.append(self.swap_total_label)
        swap_box.append(self.swap_free_label)
        swap_box.append(self.swap_used_label)
        grid.attach(swap_frame, 2, 3, 1, 1)

        # Rechte Spalte
        gpu_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("video-display")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Grafikkarte")
        label_box.append(label)
        gpu_frame.set_label_widget(label_box)
        gpu_frame.set_margin_top(8)
        gpu_frame.set_margin_bottom(8)
        gpu_frame.set_margin_start(8)
        gpu_frame.set_margin_end(8)
        gpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        gpu_box.set_margin_top(12)
        gpu_box.set_margin_bottom(12)
        gpu_box.set_margin_start(12)
        gpu_box.set_margin_end(12)
        gpu_frame.set_child(gpu_box)
        self.gpu_name_label = Gtk.Label(label="Modell: ...")
        self.gpu_name_label.set_xalign(0)
        self.gpu_memory_label = Gtk.Label(label="Speicher: ...")
        self.gpu_memory_label.set_xalign(0)
        self.gpu_driver_label = Gtk.Label(label="Treiber: ...")
        self.gpu_driver_label.set_xalign(0)
        gpu_box.append(self.gpu_name_label)
        gpu_box.append(self.gpu_memory_label)
        gpu_box.append(self.gpu_driver_label)
        grid.attach(gpu_frame, 1, 1, 1, 1)

        package_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("package-x-generic")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Pakete")
        label_box.append(label)
        package_frame.set_label_widget(label_box)
        package_frame.set_margin_top(8)
        package_frame.set_margin_bottom(8)
        package_frame.set_margin_start(8)
        package_frame.set_margin_end(8)
        package_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        package_box.set_margin_top(12)
        package_box.set_margin_bottom(12)
        package_box.set_margin_start(12)
        package_box.set_margin_end(12)
        package_frame.set_child(package_box)
        self.debian_label = Gtk.Label(label="Debian: ...")
        self.debian_label.set_xalign(0)
        self.flatpak_label = Gtk.Label(label="Flatpak: ...")
        self.flatpak_label.set_xalign(0)
        self.snap_label = Gtk.Label(label="Snap: ...")
        self.snap_label.set_xalign(0)
        package_box.append(self.debian_label)
        package_box.append(self.flatpak_label)
        package_box.append(self.snap_label)
        grid.attach(package_frame, 1, 2, 1, 1)

        self.update_stats()
        cpu_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("cpu")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="CPU")
        label_box.append(label)
        cpu_frame.set_label_widget(label_box)
        cpu_frame.set_margin_top(8)
        cpu_frame.set_margin_bottom(8)
        cpu_frame.set_margin_start(8)
        cpu_frame.set_margin_end(8)
        cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cpu_box.set_margin_top(12)
        cpu_box.set_margin_bottom(12)
        cpu_box.set_margin_start(12)
        cpu_box.set_margin_end(12)
        cpu_frame.set_child(cpu_box)
        grid.attach(cpu_frame, 2, 1, 1, 1)
        self.cpu_model_label = Gtk.Label(label="Modell: ...")
        self.cpu_model_label.set_xalign(0)
        self.cpu_max_label = Gtk.Label(label="Max: ...")
        self.cpu_max_label.set_xalign(0)
        self.cpu_current_label = Gtk.Label(label="Aktuell: ...")
        self.cpu_current_label.set_xalign(0)
        self.cpu_min_label = Gtk.Label(label="Min: ...")
        self.cpu_min_label.set_xalign(0)
        cpu_box.append(self.cpu_model_label)
        cpu_box.append(self.cpu_max_label)
        cpu_box.append(self.cpu_current_label)
        cpu_box.append(self.cpu_min_label)

        # Netzwerk Sektion
        net_frame = Gtk.Frame()
        label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label_box.set_margin_start(8)
        icon = Gtk.Image.new_from_icon_name("network-workgroup")
        icon.set_pixel_size(24)
        label_box.append(icon)
        label = Gtk.Label(label="Netzwerk")
        label_box.append(label)
        net_frame.set_label_widget(label_box)
        net_frame.set_margin_top(8)
        net_frame.set_margin_bottom(8)
        net_frame.set_margin_start(8)
        net_frame.set_margin_end(8)
        net_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        net_box.set_margin_top(12)
        net_box.set_margin_bottom(12)
        net_box.set_margin_start(12)
        net_box.set_margin_end(12)
        net_frame.set_child(net_box)
        grid.attach(net_frame, 2, 2, 1, 1)
        self.web_label = Gtk.Label(label="Web: ...")
        self.web_label.set_xalign(0)
        self.down_label = Gtk.Label(label="Down: ...")
        self.down_label.set_xalign(0)
        self.up_label = Gtk.Label(label="Up: ...")
        self.up_label.set_xalign(0)
        net_box.append(self.web_label)
        net_box.append(self.down_label)
        net_box.append(self.up_label)

        self.update_stats()

    def update_stats(self):
        def worker():
            while True:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                hdd = psutil.disk_usage("/").percent
                GLib.idle_add(self.cpu_value_label.set_markup, f'<span size="20000" weight="bold">{cpu}%</span>')
                GLib.idle_add(self.ram_value_label.set_markup, f'<span size="20000" weight="bold">{ram}%</span>')
                GLib.idle_add(self.hdd_value_label.set_markup, f'<span size="20000" weight="bold">{hdd}%</span>')
                uname = platform.uname()
                distro_name = self.get_distro_name()
                GLib.idle_add(self.distro_label.set_text, f"Distro: {distro_name}")
                GLib.idle_add(self.kernel_label.set_text, f"Kernel: {uname.release}")
                GLib.idle_add(self.user_label.set_text, f"User: {os.environ.get('USER', '')}")
                GLib.idle_add(self.resolution_label.set_text, f"Resolution: {self.get_resolution()}")
                GLib.idle_add(self.shell_label.set_text, f"Shell: {os.environ.get('SHELL', '')}")
                GLib.idle_add(self.desktop_label.set_text, f"Desktop: {self.get_desktop_environment()}")
                GLib.idle_add(self.window_manager_label.set_text, f"Window Manager: {self.get_window_manager()}")
                hostname = socket.gethostname()
                ip = self.get_local_ip()
                GLib.idle_add(self.hostname_label.set_text, f"Hostname: {hostname}")
                GLib.idle_add(self.ip_label.set_text, f"IP: {ip}")
                GLib.idle_add(self.desktop_theme_label.set_text, f"Theme: {self.get_theme()}")
                GLib.idle_add(self.icon_theme_label.set_text, f"Icons: {self.get_icon_theme()}")
                GLib.idle_add(self.cursor_theme_label.set_text, f"Cursor: {self.get_cursor_theme()}")
                gpu_name = gpu_info().replace("GPU ", "").replace("\n", ", ")
                GLib.idle_add(self.gpu_name_label.set_text, f"Modell: {gpu_name}")
                gpu_mem = gpu_memory().replace("GPU-Memory", "").strip()
                GLib.idle_add(self.gpu_memory_label.set_text, f"Speicher: {gpu_mem}")
                gpu_drv = gpu_driver().replace("GPU driver ", "").replace("GPU-Treiber ", "").replace("\n", ", ")
                GLib.idle_add(self.gpu_driver_label.set_text, f"Treiber: {gpu_drv}")
                GLib.idle_add(self.debian_label.set_text, f"Debian: {self.get_debian_package_count()}")
                GLib.idle_add(self.flatpak_label.set_text, f"Flatpak: {self.get_flatpak_count()}")
                GLib.idle_add(self.snap_label.set_text, f"Snap: {self.get_snap_count()}")
                # CPU Details
                try:
                    cpufreq = psutil.cpu_freq()
                    GLib.idle_add(self.cpu_model_label.set_text, f"Modell: {self.get_cpu_model_name()}")
                    GLib.idle_add(self.cpu_max_label.set_text, f"Max: {cpufreq.max:.0f} MHz")
                    GLib.idle_add(self.cpu_current_label.set_text, f"Aktuell: {cpufreq.current:.0f} MHz")
                    GLib.idle_add(self.cpu_min_label.set_text, f"Min: {cpufreq.min:.0f} MHz")
                except Exception:
                    pass
                # RAM & Swap
                svmem = psutil.virtual_memory()
                swap = psutil.swap_memory()
                GLib.idle_add(self.ram_total_label.set_text, f"RAM Total: {self.get_size(svmem.total)}")
                GLib.idle_add(self.ram_available_label.set_text, f"RAM Frei: {self.get_size(svmem.available)}")
                GLib.idle_add(self.ram_used_label.set_text, f"RAM Genutzt: {self.get_size(svmem.used)}")
                GLib.idle_add(self.swap_total_label.set_text, f"Swap Total: {self.get_size(swap.total)}")
                GLib.idle_add(self.swap_free_label.set_text, f"Swap Frei: {self.get_size(swap.free)}")
                GLib.idle_add(self.swap_used_label.set_text, f"Swap Genutzt: {self.get_size(swap.used)}")
                # Netzwerk
                lan_ip, down_rate, up_rate, web_state = self.get_network_info()
                GLib.idle_add(self.web_label.set_text, f"Web: {web_state}")
                GLib.idle_add(self.down_label.set_text, f"Down: {down_rate} MB/s")
                GLib.idle_add(self.up_label.set_text, f"Up: {up_rate} MB/s")
                import time; time.sleep(3)
        threading.Thread(target=worker, daemon=True).start()

    def get_size(self, bytes, suffix="B"):
        """Scale bytes to its proper format."""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
        return f"{bytes:.2f}P{suffix}"

    def get_cpu_model_name(self):
        command = "lscpu | grep -E 'Model name|Modellname' | awk -F ': ' '{gsub(/^[ \t]+|[ \t]+$/, \"\", $2); print $2}'"
        try:
            output = subprocess.check_output(
                command, shell=True, universal_newlines=True
            )
            return output.strip()
        except Exception:
            return "N/A"

    def get_network_info(self):
        try:
            local_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            local_ip.settimeout(1)  # 1 Sekunde Timeout
            local_ip.connect(("8.8.8.8", 80))
            lan_ip = local_ip.getsockname()[0]
            local_ip.close()
            net_io_counters = psutil.net_io_counters()
            down_rate = round(net_io_counters.bytes_recv / 1024 / 1024, 2)
            up_rate = round(net_io_counters.bytes_sent / 1024 / 1024, 2)
            web_state = "Verbunden"
        except (socket.error, socket.gaierror, socket.timeout):
            lan_ip = None
            down_rate = "-"
            up_rate = "-"
            web_state = "Nicht verbunden"
        return lan_ip, down_rate, up_rate, web_state
    
    def get_local_ip(self):
        """Ermittelt die lokale IP-Adresse des PCs."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)  # 1 Sekunde Timeout
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "N/A"
    def get_theme(self):
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface gtk-theme",
                shell=True,
                universal_newlines=True,
            )
            return output.strip().strip("'")
        except Exception:
            return "N/A"

    def get_icon_theme(self):
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface icon-theme",
                shell=True,
                universal_newlines=True,
            )
            return output.strip().strip("'")
        except Exception:
            return "N/A"

    def get_cursor_theme(self):
        try:
            output = subprocess.check_output(
                "gsettings get org.cinnamon.desktop.interface cursor-theme",
                shell=True,
                universal_newlines=True,
            )
            return output.strip().strip("'")
        except Exception:
            return "N/A"


    def get_debian_package_count(self):
        try:
            output = subprocess.check_output("dpkg-query -f '.\n' -W | wc -l", shell=True, universal_newlines=True)
            return output.strip()
        except Exception:
            return "N/A"

    def get_flatpak_count(self):
        try:
            output = subprocess.check_output("flatpak list | wc -l", shell=True, universal_newlines=True)
            return output.strip()
        except Exception:
            return "N/A"

    def get_snap_count(self):
        try:
            output = subprocess.check_output("snap list | wc -l", shell=True, universal_newlines=True, stderr=subprocess.DEVNULL)
            return output.strip()
        except Exception:
            return "N/A"

    def get_desktop_environment(self):
        return os.environ.get("XDG_CURRENT_DESKTOP", "N/A")

    def get_window_manager(self):
        try:
            result = subprocess.run([
                "wmctrl", "-m"], capture_output=True, text=True, check=True
            )
            output_lines = result.stdout.strip().split("\n")
            for line in output_lines:
                if line.startswith("Name: "):
                    return line.split("Name: ")[1]
        except Exception:
            return "N/A"

    def get_resolution(self):
        try:
            import Xlib.display
            display = Xlib.display.Display()
            screen = display.screen()
            return f"{screen.width_in_pixels}x{screen.height_in_pixels}"
        except Exception:
            return "?"
    
    def get_distro_name(self):
        """Liest die Distro-Version aus /etc/guideos-version aus."""
        try:
            with open("/etc/guideos-version", "r") as f:
                return f.read().strip()
        except Exception:
            # Fallback auf platform.uname() wenn die Datei nicht existiert
            return platform.uname().system
