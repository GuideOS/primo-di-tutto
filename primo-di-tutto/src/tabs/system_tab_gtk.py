
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import os
from tabs.system_dict_lib import CinnamonLook, CinnamonSettings, SystemManagement, DeviceSettings

class SystemTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)


        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        self.append(scroll)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        scroll.set_child(vbox)

        # Info-Label außerhalb der Scrollbox
        self.sys_info_label = Gtk.Label(label="", wrap=True, xalign=0)
        self.sys_info_label.set_margin_top(10)
        self.sys_info_label.set_margin_bottom(10)
        self.sys_info_label.set_margin_start(10)
        self.sys_info_label.set_margin_end(10)
        self.append(self.sys_info_label)

        def add_tile_grid(parent, title, items, on_click, on_hover, icon_name=None):
            frame = Gtk.Frame()
            if icon_name:
                label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                label_box.set_margin_start(8)
                icon = Gtk.Image.new_from_icon_name(icon_name)
                icon.set_pixel_size(24)
                label_box.append(icon)
                label = Gtk.Label(label=title)
                label_box.append(label)
                frame.set_label_widget(label_box)
            else:
                frame.set_label(title)
            frame.set_margin_bottom(10)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            box.set_margin_top(10)
            box.set_margin_bottom(10)
            box.set_margin_start(10)
            box.set_margin_end(10)
            frame.set_child(box)
            parent.append(frame)
            grid = Gtk.Grid()
            grid.set_column_spacing(24)
            grid.set_row_spacing(24)
            grid.set_column_homogeneous(True)
            grid.set_row_homogeneous(True)
            box.append(grid)
            max_columns = 4
            for i, (key, info) in enumerate(items.items()):
                row = i // max_columns
                col = i % max_columns
                tile = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
                tile.set_hexpand(True)
                # Icon
                icon_name = info.get("Icon", "dialog-information")
                icon = Gtk.Image.new_from_icon_name(icon_name)
                icon.set_pixel_size(48)
                tile.append(icon)
                # Text
                label = Gtk.Label(label=info["Name"], wrap=True, xalign=0.5)
                tile.append(label)
                # Button
                btn = Gtk.Button()
                btn.set_child(tile)
                btn.set_hexpand(True)
                btn.connect("clicked", lambda b, k=key: on_click(k))
                # Hover-Effekt mit EventControllerMotion
                motion = Gtk.EventControllerMotion()
                motion.connect("enter", lambda c, x, y, k=key: on_hover(k))
                motion.connect("leave", lambda c: self.on_leave())
                btn.add_controller(motion)
                grid.attach(btn, col, row, 1, 1)
            return frame

        # Look
        def look_btn_action(look_key):
            command = CinnamonLook.cinna_look_dict[look_key]["Action"]
            os.popen(command)
        def on_hover_look(key):
            self.sys_info_label.set_label(CinnamonLook.cinna_look_dict[key]["Description"])
        add_tile_grid(vbox, "Erscheinungsbild", CinnamonLook.cinna_look_dict, look_btn_action, on_hover_look, "preferences-desktop-theme")

        # Settings
        def sett_btn_action(sett_key):
            command = CinnamonSettings.cinna_sett_dict[sett_key]["Action"]
            os.popen(command)
        def on_hover_sett(key):
            self.sys_info_label.set_label(CinnamonSettings.cinna_sett_dict[key]["Description"])
        add_tile_grid(vbox, "Einstellungen", CinnamonSettings.cinna_sett_dict, sett_btn_action, on_hover_sett, "preferences-system")

        # Geräte
        def device_sett_btn_action(device_sett_key):
            command = DeviceSettings.device_sett_dict[device_sett_key]["Action"]
            os.popen(command)
        def on_hover_device(key):
            self.sys_info_label.set_label(DeviceSettings.device_sett_dict[key]["Description"])
        add_tile_grid(vbox, "Geräte", DeviceSettings.device_sett_dict, device_sett_btn_action, on_hover_device, "computer")

        # Systemverwaltung
        def sys_mgmt_btn_action(sys_mgmt_key):
            command = SystemManagement.sys_mgmt_dict[sys_mgmt_key]["Action"]
            os.popen(command)
        def on_hover_sys(key):
            self.sys_info_label.set_label(SystemManagement.sys_mgmt_dict[key]["Description"])
        add_tile_grid(vbox, "Systemverwaltung", SystemManagement.sys_mgmt_dict, sys_mgmt_btn_action, on_hover_sys, "preferences-system-privacy")

        # Info-Label ist jetzt außerhalb der Scrollbox

    def on_leave(self):
        self.sys_info_label.set_label("")
