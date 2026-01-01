import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import subprocess

class DevicesTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        # USB-Geräte Section
        usb_frame = Gtk.Frame()
        usb_frame.set_label("USB-Geräte")
        usb_frame.set_margin_bottom(10)
        usb_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        usb_vbox.set_margin_top(10)
        usb_vbox.set_margin_bottom(10)
        usb_vbox.set_margin_start(10)
        usb_vbox.set_margin_end(10)
        usb_frame.set_child(usb_vbox)
        self.append(usb_frame)

        self.usb_store = Gtk.TreeStore(str, str, str)  # Name, ID, Speed
        self.usb_tree = Gtk.TreeView(model=self.usb_store)
        renderer = Gtk.CellRendererText()
        col_name = Gtk.TreeViewColumn("Name", renderer, text=0)
        col_id = Gtk.TreeViewColumn("ID", renderer, text=1)
        col_speed = Gtk.TreeViewColumn("Speed", renderer, text=2)
        self.usb_tree.append_column(col_name)
        self.usb_tree.append_column(col_id)
        self.usb_tree.append_column(col_speed)
        usb_scroll = Gtk.ScrolledWindow()
        usb_scroll.set_child(self.usb_tree)
        usb_scroll.set_vexpand(True)
        usb_vbox.append(usb_scroll)

        # PCI-Geräte Section
        pci_frame = Gtk.Frame()
        pci_frame.set_label("PCI-Geräte")
        pci_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        pci_vbox.set_margin_top(10)
        pci_vbox.set_margin_bottom(10)
        pci_vbox.set_margin_start(10)
        pci_vbox.set_margin_end(10)
        pci_frame.set_child(pci_vbox)
        self.append(pci_frame)

        self.pci_store = Gtk.ListStore(str, str)  # Slot, Typ
        self.pci_tree = Gtk.TreeView(model=self.pci_store)
        pci_col_slot = Gtk.TreeViewColumn("Slot", renderer, text=0)
        pci_col_type = Gtk.TreeViewColumn("Typ", renderer, text=1)
        self.pci_tree.append_column(pci_col_slot)
        self.pci_tree.append_column(pci_col_type)
        pci_scroll = Gtk.ScrolledWindow()
        pci_scroll.set_child(self.pci_tree)
        pci_scroll.set_vexpand(True)
        pci_vbox.append(pci_scroll)

        # Refresh Button
        btn = Gtk.Button(label="Aktualisieren")
        btn.connect("clicked", self.refresh_all_devices)
        self.append(btn)

        self.refresh_all_devices()

    def get_usb_data(self):
        devices_by_bus = {}
        try:
            result = subprocess.run(["lsusb"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if not line.strip() or "Bus" not in line:
                    continue
                id_pos = line.find(" ID ")
                if id_pos == -1:
                    continue
                bus_dev_part = line[:id_pos].strip()
                id_and_name = line[id_pos + 4 :].strip()
                try:
                    bus_num = bus_dev_part.split("Bus")[1].split("Device")[0].strip()
                    dev_num = bus_dev_part.split("Device")[1].strip().rstrip(":")
                except:
                    continue
                parts = id_and_name.split(" ", 1)
                device_id = parts[0] if parts else "N/A"
                device_name = parts[1] if len(parts) > 1 else "Unknown Device"
                if bus_num not in devices_by_bus:
                    devices_by_bus[bus_num] = {"hub": None, "devices": []}
                if dev_num == "001":
                    devices_by_bus[bus_num]["hub"] = {"name": device_name, "id": device_id, "dev_num": dev_num}
                else:
                    devices_by_bus[bus_num]["devices"].append({"name": device_name, "id": device_id, "dev_num": dev_num})
        except Exception as e:
            print(f"Error parsing lsusb: {e}")
        return devices_by_bus

    def get_device_speed(self, bus_num, dev_num):
        try:
            result = subprocess.run(["lsusb", "-t"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            in_correct_bus = False
            for line in lines:
                if line.startswith("/:"):
                    if f"Bus {bus_num.zfill(3)}" in line:
                        in_correct_bus = True
                        if dev_num == "001":
                            parts = line.split(",")
                            speed = parts[-1].strip() if parts else "N/A"
                            return self.convert_speed_to_mbps(speed)
                    else:
                        in_correct_bus = False
                elif in_correct_bus and "|__" in line:
                    if f"Dev {dev_num.zfill(3)}" in line:
                        parts = line.split(",")
                        speed = parts[-1].strip() if parts else "N/A"
                        return self.convert_speed_to_mbps(speed)
        except Exception as e:
            print(f"Error getting speed: {e}")
        return "N/A"

    def convert_speed_to_mbps(self, speed_str):
        if not speed_str or speed_str == "N/A":
            return "N/A"
        try:
            if "M" in speed_str:
                speed_value = speed_str.replace("M", "").strip()
                return f"{speed_value} Mbps"
            elif "k" in speed_str.lower():
                speed_value = speed_str.lower().replace("k", "").strip()
                return f"{speed_value} Mbps"
        except:
            pass
        return speed_str

    def refresh_usb_devices(self):
        self.usb_store.clear()
        devices_by_bus = self.get_usb_data()
        for bus_num in sorted(devices_by_bus.keys()):
            bus_data = devices_by_bus[bus_num]
            hub = bus_data.get("hub")
            if hub:
                speed = self.get_device_speed(bus_num, "001")
                bus_name = f"Bus {bus_num}: {hub['name']}"
            else:
                bus_name = f"Bus {bus_num}"
                speed = "N/A"
            bus_iter = self.usb_store.append(None, [bus_name, "", speed])
            for device in bus_data["devices"]:
                dev_speed = self.get_device_speed(bus_num, device["dev_num"])
                self.usb_store.append(bus_iter, [device["name"], device["id"], dev_speed])

    def get_pci_devices(self):
        devices = []
        try:
            result = subprocess.run(["lspci"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    slot = parts[0]
                    device_type = parts[1].rstrip(":")
                    device_name = parts[2]
                    full_description = f"{device_type}: {device_name}"
                    devices.append({"slot": slot, "type": full_description})
        except Exception as e:
            print(f"Error parsing lspci: {e}")
        return devices

    def refresh_pci_devices(self):
        self.pci_store.clear()
        devices = self.get_pci_devices()
        for device in devices:
            self.pci_store.append([device["slot"], device["type"]])

    def refresh_all_devices(self, *args):
        self.refresh_usb_devices()
        self.refresh_pci_devices()
