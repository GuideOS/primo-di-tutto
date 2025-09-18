#!/usr/bin/python3

import os
from os import popen
from tkinter import *
from tkinter import ttk
from resorcess import *
from apt_manage import *
from tabs.pop_ups import *
from tabs.system_dict_lib import (
    CinnamonLook,
    CinnamonSettings,
    SystemManagement,
    DeviceSettings,
)


class SystemTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.update_interval = 1000

        # Frame für Canvas und Scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas-Container für sys_btn_frame
        canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollen mit dem Mausrad ermöglichen
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )
        canvas.bind(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )  # Linux spezifisch
        canvas.bind(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )  # Linux spezifisch

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

        # Look Settings
        look_btn_frame = ttk.LabelFrame(
            scrollable_frame, text="Erscheinungsbild", padding=20
        )
        look_btn_frame.pack(fill="both", expand=tk.TRUE)

        look_btn_frame.grid_columnconfigure(0, weight=2)
        look_btn_frame.grid_columnconfigure(1, weight=2)
        look_btn_frame.grid_columnconfigure(2, weight=2)
        look_btn_frame.grid_columnconfigure(3, weight=1)
        look_btn_frame.grid_columnconfigure(4, weight=2)

        look_btn_frame.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )
        look_btn_frame.bind(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )  # Linux spezifisch
        look_btn_frame.bind(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )  # Linux spezifisch

        def look_btn_action(look_key):
            # SoftwareSys.sys_dict[sys_key]["Action"]
            command = CinnamonLook.cinna_look_dict[look_key]["Action"]
            print(command)
            os.popen(command)

        self.look_btn_icons = []

        for i, (look_key, look_info) in enumerate(CinnamonLook.cinna_look_dict.items()):
            icon = tk.PhotoImage(file=look_info["Icon"])
            self.look_btn_icons.append(icon)

        max_columns = 4

        for i, (look_key, look_info) in enumerate(CinnamonLook.cinna_look_dict.items()):
            row = i // max_columns
            column = i % max_columns

            look_button = ttk.Button(
                look_btn_frame,
                text=look_info["Name"],
                image=self.look_btn_icons[i],
                command=lambda key=look_key: look_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            look_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            look_button.bind(
                "<Enter>", lambda event, key=look_key: self.on_hover_look(event, key)
            )
            look_button.bind("<Leave>", self.on_leave)
            look_button.bind(
                "<MouseWheel>",
                lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
            )
            look_button.bind(
                "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
            )  # Linux spezifisch
            look_button.bind(
                "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
            )  # Linux spezifisch

        # Settings Buttons
        sett_btn_frame = ttk.LabelFrame(
            scrollable_frame, text="Einstellungen", padding=20
        )
        sett_btn_frame.pack(fill="both", expand=tk.TRUE)

        sett_btn_frame.grid_columnconfigure(0, weight=2)
        sett_btn_frame.grid_columnconfigure(1, weight=2)
        sett_btn_frame.grid_columnconfigure(2, weight=2)
        sett_btn_frame.grid_columnconfigure(3, weight=1)
        sett_btn_frame.grid_columnconfigure(4, weight=2)

        sett_btn_frame.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )
        sett_btn_frame.bind(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )  # Linux spezifisch
        sett_btn_frame.bind(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )  # Linux spezifisch

        def sett_btn_action(sett_key):
            # CinnamonSettings.cinna_sett_dict[sett_key]["Action"]
            command = CinnamonSettings.cinna_sett_dict[sett_key]["Action"]
            print(command)
            os.popen(command)

        self.sett_btn_icons = []

        for i, (sett_key, sett_info) in enumerate(
            CinnamonSettings.cinna_sett_dict.items()
        ):
            icon = tk.PhotoImage(file=sett_info["Icon"])
            self.sett_btn_icons.append(icon)

        max_columns = 5

        for i, (sett_key, sett_info) in enumerate(
            CinnamonSettings.cinna_sett_dict.items()
        ):
            row = i // max_columns
            column = i % max_columns

            sett_button = ttk.Button(
                sett_btn_frame,
                text=sett_info["Name"],
                image=self.sett_btn_icons[i],
                command=lambda key=sett_key: sett_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            sett_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sett_button.bind(
                "<Enter>", lambda event, key=sett_key: self.on_hover_sett(event, key)
            )
            sett_button.bind("<Leave>", self.on_leave)
            sett_button.bind(
                "<MouseWheel>",
                lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
            )
            sett_button.bind(
                "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
            )  # Linux spezifisch
            sett_button.bind(
                "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
            )  # Linux spezifisch
        # Device Settings Buttons
        device_sett_btn_frame = ttk.LabelFrame(
            scrollable_frame, text="Geräte", padding=20
        )
        device_sett_btn_frame.pack(fill="both", expand=tk.TRUE)

        device_sett_btn_frame.grid_columnconfigure(0, weight=2)
        device_sett_btn_frame.grid_columnconfigure(1, weight=2)
        device_sett_btn_frame.grid_columnconfigure(2, weight=2)
        device_sett_btn_frame.grid_columnconfigure(3, weight=1)
        device_sett_btn_frame.grid_columnconfigure(4, weight=2)

        device_sett_btn_frame.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )
        device_sett_btn_frame.bind(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )  # Linux spezifisch
        device_sett_btn_frame.bind(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )  # Linux spezifisch

        def device_sett_btn_action(device_sett_key):
            # SystemManagement.sys_mgmt_dict[sett_key]["Action"]
            command = DeviceSettings.device_sett_dict[device_sett_key]["Action"]
            print(command)
            os.popen(command)

        self.device_sett_btn_icons = []

        for i, (device_sett_key, device_sett_info) in enumerate(
            DeviceSettings.device_sett_dict.items()
        ):
            icon = tk.PhotoImage(file=device_sett_info["Icon"])
            self.device_sett_btn_icons.append(icon)

        max_columns = 5

        for i, (device_sett_key, device_sett_info) in enumerate(
            DeviceSettings.device_sett_dict.items()
        ):
            row = i // max_columns
            column = i % max_columns

            device_sett_button = ttk.Button(
                device_sett_btn_frame,
                text=device_sett_info["Name"],
                image=self.device_sett_btn_icons[i],
                command=lambda key=device_sett_key: device_sett_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            device_sett_button.grid(
                row=row, column=column, padx=3, pady=3, sticky="nesw"
            )

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            device_sett_button.bind(
                "<Enter>",
                lambda event, key=device_sett_key: self.on_hover_device(event, key),
            )
            device_sett_button.bind("<Leave>", self.on_leave)
            device_sett_button.bind(
                "<MouseWheel>",
                lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
            )
            device_sett_button.bind(
                "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
            )  # Linux spezifisch
            device_sett_button.bind(
                "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
            )  # Linux spezifisch

        # System Management Buttons
        sys_mgmt_btn_frame = ttk.LabelFrame(
            scrollable_frame, text="Systemverwaltung", padding=20
        )
        sys_mgmt_btn_frame.pack(fill="both", expand=tk.TRUE)

        sys_mgmt_btn_frame.grid_columnconfigure(0, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(1, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(2, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(3, weight=1)
        sys_mgmt_btn_frame.grid_columnconfigure(4, weight=2)

        sys_mgmt_btn_frame.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
        )
        sys_mgmt_btn_frame.bind(
            "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
        )  # Linux spezifisch
        sys_mgmt_btn_frame.bind(
            "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
        )  # Linux spezifisch

        def sys_mgmt_btn_action(sys_mgmt_key):
            # DeviceSettings.sys_mgmt_dict[sett_key]["Action"]
            command = SystemManagement.sys_mgmt_dict[sys_mgmt_key]["Action"]
            print(command)
            os.popen(command)

        self.sys_mgmt_btn_icons = []

        for i, (sys_mgmt_key, sys_mgmt_info) in enumerate(
            SystemManagement.sys_mgmt_dict.items()
        ):
            icon = tk.PhotoImage(file=sys_mgmt_info["Icon"])
            self.sys_mgmt_btn_icons.append(icon)

        max_columns = 5

        for i, (sys_mgmt_key, sys_mgmt_info) in enumerate(
            SystemManagement.sys_mgmt_dict.items()
        ):
            row = i // max_columns
            column = i % max_columns

            sys_mgmt_button = ttk.Button(
                sys_mgmt_btn_frame,
                text=sys_mgmt_info["Name"],
                image=self.sys_mgmt_btn_icons[i],
                command=lambda key=sys_mgmt_key: sys_mgmt_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19,
            )
            sys_mgmt_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_mgmt_button.bind(
                "<Enter>", lambda event, key=sys_mgmt_key: self.on_hover_sys(event, key)
            )
            sys_mgmt_button.bind("<Leave>", self.on_leave)
            sys_mgmt_button.bind(
                "<MouseWheel>",
                lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"),
            )
            sys_mgmt_button.bind(
                "<Button-4>", lambda e: canvas.yview_scroll(-1, "units")
            )  # Linux spezifisch
            sys_mgmt_button.bind(
                "<Button-5>", lambda e: canvas.yview_scroll(1, "units")
            )  # Linux spezifisch

        sys_info_frame = ttk.LabelFrame(self, text="Info", padding=20)
        sys_info_frame.pack(pady=20, padx=20, fill="both")

        # Label für die Anzeige der Beschreibung
        self.sys_info_label = tk.Label(sys_info_frame, justify="left", wraplength=900)
        self.sys_info_label.pack(anchor="w")

    # Funktion für das Hover-Ereignis
    def on_hover_look(self, event, key):
        self.sys_info_label.configure(
            text=CinnamonLook.cinna_look_dict[key]["Description"]
        )

    # Funktion für das Hover-Ereignis
    def on_hover_sett(self, event, key):
        self.sys_info_label.configure(
            text=CinnamonSettings.cinna_sett_dict[key]["Description"]
        )

    # Funktion für das Hover-Ereignis
    def on_hover_device(self, event, key):
        self.sys_info_label.configure(
            text=DeviceSettings.device_sett_dict[key]["Description"]
        )

    # Funktion für das Hover-Ereignis
    def on_hover_sys(self, event, key):
        self.sys_info_label.configure(
            text=SystemManagement.sys_mgmt_dict[key]["Description"]
        )

    # Funktion für das Verlassen des Buttons
    def on_leave(self, event):
        self.sys_info_label.configure(text="")
