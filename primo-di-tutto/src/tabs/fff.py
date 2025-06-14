        # sett_btn_frame in das scrollbare Frame einfügen
        sys_mgmt_btn_frame = ttk.LabelFrame(scrollable_frame, text="Systemverwaltung", padding=20)
        sys_mgmt_btn_frame.pack(fill="both", expand=tk.TRUE)

        sys_mgmt_btn_frame.grid_columnconfigure(0, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(1, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(2, weight=2)
        sys_mgmt_btn_frame.grid_columnconfigure(3, weight=1)
        sys_mgmt_btn_frame.grid_columnconfigure(4, weight=2)
 
        def sys_mgmt_btn_action(sys_mgmt_key):
            # DeviceSettings.sys_mgmt_dict[sett_key]["Action"]
            command = DeviceSettings.sys_mgmt_dict[sys_mgmt_key]["Action"]
            print(command)
            os.popen(command)

        self.sys_mgmt_btn_icons = []

        for i, (sys_mgmt_key, sys_mgmt_info) in enumerate(DeviceSettings.sys_mgmt_dict.items()):
            icon = tk.PhotoImage(file=sys_mgmt_info["Icon"])
            self.sys_mgmt_btn_icons.append(icon)

        max_columns = 5

        for i, (sys_mgmt_key, sys_mgmt_info) in enumerate(DeviceSettings.sys_mgmt_dict.items()):
            row = i // max_columns
            column = i % max_columns

            sys_mgmt_button = ttk.Button(
                sys_mgmt_btn_frame,
                text=sys_mgmt_info["Name"],
                image=self.sys_mgmt_btn_icons[i],
                command=lambda key=sys_mgmt_key: sys_mgmt_btn_action(key),
                compound=tk.TOP,
                style="Custom.TButton",
                width=19
            )
            sys_mgmt_button.grid(row=row, column=column, padx=3, pady=3, sticky="nesw")

            # Hover- und Leave-Ereignisse für diesen Button hinzufügen
            sys_mgmt_button.bind("<Enter>", lambda event, key=sys_mgmt_key: self.on_hover(event, key))
            sys_mgmt_button.bind("<Leave>", self.on_leave)