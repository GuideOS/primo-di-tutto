#!/usr/bin/python3

import os
import subprocess
from tkinter import *
from tkinter import ttk
from resorcess import *


class DevicesTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # USB Section
        usb_frame = ttk.LabelFrame(self, text="USB-Geräte", padding=20)
        usb_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

        # Treeview frame with scrollbar
        usb_tree_frame = ttk.Frame(usb_frame)
        usb_tree_frame.pack(fill=BOTH, expand=True)

        # Treeview - show tree column for hierarchy
        columns = ("ID", "Speed")
        self.usb_tree = ttk.Treeview(
            usb_tree_frame, columns=columns, show="tree headings", height=8
        )

        # Scrollbar
        usb_scrollbar = ttk.Scrollbar(
            usb_tree_frame, orient=VERTICAL, command=self.usb_tree.yview
        )
        self.usb_tree.configure(yscrollcommand=usb_scrollbar.set)

        # Define headings
        self.usb_tree.heading("#0", text="Name")
        self.usb_tree.heading("ID", text="ID")
        self.usb_tree.heading("Speed", text="Speed")

        # Define column widths
        self.usb_tree.column("#0", width=500)
        self.usb_tree.column("ID", width=150)
        self.usb_tree.column("Speed", width=100)

        # Pack widgets
        self.usb_tree.pack(side=LEFT, fill=BOTH, expand=True)
        usb_scrollbar.pack(side=RIGHT, fill=Y)

        # PCI Section
        pci_frame = ttk.LabelFrame(self, text="PCI-Geräte", padding=20)
        pci_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 10))

        # Treeview frame with scrollbar
        pci_tree_frame = ttk.Frame(pci_frame)
        pci_tree_frame.pack(fill=BOTH, expand=True)

        # Scrollbar
        pci_scrollbar = ttk.Scrollbar(pci_tree_frame, orient=VERTICAL)
        pci_scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        pci_columns = ("Slot", "Type")
        self.pci_tree = ttk.Treeview(
            pci_tree_frame,
            columns=pci_columns,
            show="headings",
            yscrollcommand=pci_scrollbar.set,
            height=8,
        )
        pci_scrollbar.config(command=self.pci_tree.yview)

        # Define headings
        self.pci_tree.heading("Slot", text="Slot")
        self.pci_tree.heading("Type", text="Typ")

        # Define column widths
        self.pci_tree.column("Slot", width=120)
        self.pci_tree.column("Type", width=630)

        self.pci_tree.pack(fill=BOTH, expand=True)

        # Refresh button frame at bottom
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=(0, 20))

        # Refresh button
        refresh_btn = ttk.Button(
            button_frame, text="Aktualisieren", command=self.refresh_all_devices
        )
        refresh_btn.pack()

        # Load devices
        self.refresh_all_devices()

    def get_usb_data(self):
        """Parse lsusb output and organize by bus"""
        devices_by_bus = {}

        try:
            # Get device list with names
            result = subprocess.run(["lsusb"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")

            for line in lines:
                # Parse: Bus 001 Device 002: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle
                if not line.strip() or "Bus" not in line:
                    continue

                # Find the position of "ID " in the line
                id_pos = line.find(" ID ")
                if id_pos == -1:
                    continue

                # Everything before " ID " contains bus and device info
                bus_dev_part = line[:id_pos].strip()
                # Everything after " ID " contains the ID and device name
                id_and_name = line[id_pos + 4 :].strip()  # +4 to skip " ID "

                # Extract bus and device numbers
                # "Bus 001 Device 002:"
                try:
                    bus_num = bus_dev_part.split("Bus")[1].split("Device")[0].strip()
                    dev_num = (
                        bus_dev_part.split("Device")[1].strip().rstrip(":")
                    )  # Remove trailing colon
                except:
                    continue

                # Extract ID and device name
                # "0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle"
                parts = id_and_name.split(" ", 1)
                device_id = parts[0] if parts else "N/A"
                device_name = parts[1] if len(parts) > 1 else "Unknown Device"

                # Initialize bus dict if needed
                if bus_num not in devices_by_bus:
                    devices_by_bus[bus_num] = {"hub": None, "devices": []}

                # Device 001 is the root hub
                if dev_num == "001":
                    devices_by_bus[bus_num]["hub"] = {
                        "name": device_name,
                        "id": device_id,
                        "dev_num": dev_num,
                    }
                else:
                    devices_by_bus[bus_num]["devices"].append(
                        {"name": device_name, "id": device_id, "dev_num": dev_num}
                    )

        except Exception as e:
            print(f"Error parsing lsusb: {e}")

        return devices_by_bus

    def get_device_speed(self, bus_num, dev_num):
        """Get speed from lsusb -t and convert to Mbps"""
        try:
            result = subprocess.run(["lsusb", "-t"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")

            in_correct_bus = False

            for line in lines:
                # Bus line starts with /:
                if line.startswith("/:"):
                    # Check if this is our bus
                    if f"Bus {bus_num.zfill(3)}" in line:
                        in_correct_bus = True
                        # If looking for device 001 (root hub)
                        if dev_num == "001":
                            parts = line.split(",")
                            speed = parts[-1].strip() if parts else "N/A"
                            return self.convert_speed_to_mbps(speed)
                    else:
                        in_correct_bus = False

                # Device line starts with |__
                elif in_correct_bus and "|__" in line:
                    # Check if this is our device
                    if f"Dev {dev_num.zfill(3)}" in line:
                        parts = line.split(",")
                        speed = parts[-1].strip() if parts else "N/A"
                        return self.convert_speed_to_mbps(speed)

        except Exception as e:
            print(f"Error getting speed: {e}")

        return "N/A"

    def convert_speed_to_mbps(self, speed_str):
        """Convert speed string (e.g., '480M', '5000M', '12M') to 'XXX Mbps'"""
        if not speed_str or speed_str == "N/A":
            return "N/A"

        try:
            # Extract number from string like "480M" or "5000M"
            if "M" in speed_str:
                speed_value = speed_str.replace("M", "").strip()
                return f"{speed_value} Mbps"
            elif "k" in speed_str.lower():
                # Handle kbps if present (e.g., "1.5k" -> "1.5 Mbps")
                speed_value = speed_str.lower().replace("k", "").strip()
                return f"{speed_value} Mbps"
        except:
            pass

        return speed_str

    def refresh_usb_devices(self):
        """Refresh the USB devices tree"""
        # Clear existing items
        for item in self.usb_tree.get_children():
            self.usb_tree.delete(item)

        # Get all USB data
        devices_by_bus = self.get_usb_data()

        # Build tree
        for bus_num in sorted(devices_by_bus.keys()):
            bus_data = devices_by_bus[bus_num]
            hub = bus_data.get("hub")

            # Create bus item
            if hub:
                speed = self.get_device_speed(bus_num, "001")
                bus_name = f"Bus {bus_num}: {hub['name']}"
            else:
                bus_name = f"Bus {bus_num}"
                speed = "N/A"

            bus_item = self.usb_tree.insert(
                "", END, text=bus_name, values=("", speed), open=True
            )

            # Add devices to this bus
            for device in bus_data["devices"]:
                dev_speed = self.get_device_speed(bus_num, device["dev_num"])

                self.usb_tree.insert(
                    bus_item, END, text=device["name"], values=(device["id"], dev_speed)
                )

    def get_pci_devices(self):
        """Get PCI devices from lspci"""
        devices = []

        try:
            result = subprocess.run(["lspci"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")

            for line in lines:
                if not line.strip():
                    continue

                # Parse: 00:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    slot = parts[0]  # 00:00.0
                    device_type = parts[1].rstrip(":")  # Host bridge
                    device_name = parts[
                        2
                    ]  # Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex

                    # Combine type and name
                    full_description = f"{device_type}: {device_name}"

                    devices.append({"slot": slot, "type": full_description})
        except Exception as e:
            print(f"Error parsing lspci: {e}")

        return devices

    def refresh_pci_devices(self):
        """Refresh the PCI devices list"""
        # Clear existing items
        for item in self.pci_tree.get_children():
            self.pci_tree.delete(item)

        # Get PCI devices
        devices = self.get_pci_devices()

        # Populate tree
        for device in devices:
            self.pci_tree.insert("", END, values=(device["slot"], device["type"]))

    def refresh_all_devices(self):
        """Refresh both USB and PCI devices"""
        self.refresh_usb_devices()
        self.refresh_pci_devices()
