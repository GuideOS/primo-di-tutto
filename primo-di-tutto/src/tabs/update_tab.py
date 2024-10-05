#!/usr/bin/python3

import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from resorcess import *
from apt_manage import *
from snap_manage import *
from flatpak_alias_list import *
from flatpak_manage import *
from tool_tipps import CreateToolTip
from tool_tipps import TipsText
from tabs.pop_ups import *
from tabs.text_dict_lib import Update_Tab_Buttons
from resorcess import pi_identify


class UpdateTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")


        self.folder_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/folder_s_light.png"
        )
        self.up_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_up_s_light.png"
        )
        self.gup_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_upg_s_light.png"
        )
        self.recover_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/recover_s_light.png"
        )
        self.fup_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/pack_fupg_s_light.png"
        )
        self.allow_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/allow_s_light.png"
        )
        self.arm_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/del_s_light.png"
        )
        self.confa_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/confa_s_light.png"
        )
        self.re_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/re_s_light.png"
        )
        self.inst_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/debinst_s_light.png"
        )
        self.term_icon = PhotoImage(
            file=f"{application_path}/images/icons/pigro_icons/terminal_s_light.png"
        )

        self.term_logo = PhotoImage(
            file=f"{application_path}/images/icons/papirus/goterminal.png"
        )
        #self.background = maincolor

        def up_action(text):
            """Passes commands du auto generated buttons"""
            frame_width = self.termf.winfo_width()

            frame_height = self.termf.winfo_height()
            print(
                "The width & height of the label is:",
                frame_width,
                frame_height,
                "pixels",
            )
            if text == "Paketliste erneuern":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt update -y |lolcat && sleep 5 && exit ; exec bash"'
                    % wid
                )
            if text == "Pakete erneuern":
                if pi_identify() == "pi_os":
                    os.popen(
                        f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt update -y |lolcat && {permit} apt upgrade -y |lolcat && sleep 5 && exit ; exec bash"'
                        % wid
                    )
                else:
                    command = (
                        f"xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "
                        "\"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY bash -c 'apt update -y && apt upgrade -y' | lolcat && "
                        'sleep 5 && exit; exec bash"' % wid
                    )
                    os.popen(command)
            if text == "Vervollständigen":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt install --fix-missing |lolcat && sleep 5 && exit; exec bash"'
                    % wid
                )
            if text == "Reparieren":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt --fix-broken install |lolcat && sleep 5 && exit; exec bash"'
                    % wid
                )
            if text == "Dist Upgrade":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt dist-upgrade -y |lolcat && sleep 5 && exit; exec bash"'
                    % wid
                )
            if text == "Aufräumen":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} apt autoremove -y |lolcat && sleep 5 && exit ; exec bash"'
                    % wid
                )
            if text == ".DEB installieren":
                self.filename = filedialog.askopenfilename(
                    initialdir="~",
                    title="Select A File",
                    filetypes=((".deb files", "*.deb"),),
                )
                os.popen(f"gdebi-gtk {self.filename}")

            if text == "Konfigurieren":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} dpkg --configure -a |lolcat && sleep 5 && exit; exec bash"'
                    % wid
                )
            if text == "Aktualisierbarkeit":
                if pi_identify() == "pi_os":
                    subprocess.run(
                        f"xterm -into {wid} -bg Grey11 -geometry {frame_height}x{frame_width} -e \"{permit} apt list --upgradable |lolcat && read -p 'Press Enter to exit.' && exit ; exec bash\"",
                        shell=True,
                    )
                else:
                    os.popen(
                        f"xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "
                        "\"pkexec apt list --upgradable |lolcat && read -p 'Press Enter to exit.' && exit; exec bash\""
                        % wid
                    )

        self.update_btn_frame = ttk.Frame(
            self,
        )
        self.update_btn_frame.pack(padx=20, pady=20, anchor="n", fill="x", side="left")
        #self.update_btn_frame["background"] = frame_color

        self.termf = ttk.LabelFrame(
            self,
            text="Progress"

        )

        self.term_logo_label = Label(
            self.termf, image=self.term_logo, #background=frame_color
        )
        self.term_logo_label.pack(fill=BOTH, expand=True)

        self.termf.pack(fill=BOTH, expand=True, pady=20, padx=20)

        global wid
        wid = self.termf.winfo_id()
        #self.termf["background"] = frame_color

        self.btn_frame = ttk.LabelFrame(
            self.update_btn_frame,
            text="APT Optionen",
            #font=font_16,
            #foreground=label_frame_color,
            #borderwidth=0,
            #relief=GROOVE,
            #highlightthickness=0,
            #background=frame_color,
            #pady=10,
        )
        self.btn_frame.pack(anchor="n")

        up_button_dict = Update_Tab_Buttons.up_button_dict

        up_button_list1 = []
        conf_row = 0
        conf_column = 0

        for up_button, description in up_button_dict.items():
            self.up_button_x = ttk.Button(
                self.btn_frame,
                #justify="left",
                compound="left",
                #anchor="w",
                text=up_button,
                command=lambda text=up_button: up_action(text),
                #borderwidth=0,
                #highlightthickness=0,
                #background=ext_btn,
                #foreground=ext_btn_font,
                width=20,
                
            )

            self.up_button_x.grid(
                row=conf_row, column=conf_column, padx=5, pady=5, sticky="ew"
            )
            up_button_list1.append(self.up_button_x)
            conf_column += 1

            if conf_column == 1:
                conf_row += 1
                conf_column = 0

            if up_button == "Paketliste erneuern":
                self.up_button_x.config(image=self.up_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Aktualisierbarkeit":
                self.up_button_x.config(image=self.up_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Vervollständigen":
                self.up_button_x.config(image=self.up_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Reparieren":
                self.up_button_x.config(image=self.up_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Pakete erneuern":
                self.up_button_x.config(image=self.gup_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Aufräumen":
                self.up_button_x.config(image=self.arm_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == ".DEB installieren":
                self.up_button_x.config(image=self.inst_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)
            elif up_button == "Konfigurieren":
                self.up_button_x.config(image=self.confa_icon)
                self.up_button_x_ttp = CreateToolTip(self.up_button_x, description)




        def flatpak_action(text):
            """Passes commands for auto-generated buttons"""
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            print(
                "The width & height of the label is:",
                frame_width,
                frame_height,
                "pixels",
            )

            if text == "Update":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "flatpak update -y && sleep 5 && exit ; exec bash"'
                    % wid
                )
            elif text == "Tidy Up Unused":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "flatpak uninstall --unused -y && sleep 5 && exit; exec bash"'
                    % wid
                )

        self.flatpak_frame = ttk.LabelFrame(
            self.update_btn_frame,
            text="Flatpak Options",
            #font=font_16,
            #foreground=label_frame_color,
            #borderwidth=0,
            #relief=GROOVE,
            #highlightthickness=0,
            #background=frame_color,
            #pady=10,
        )
        self.flatpak_frame.pack(anchor="n", fill="x")

        self.flatpak_frame.columnconfigure(0, weight=1)
        self.flatpak_frame.rowconfigure(0, weight=1)

        flatpak_button_dict = {
            "Update": {
                "image": self.up_icon,
                "state": NORMAL if flatpak_path else DISABLED,
                "tooltip": TipsText.ttip_flatpak_update,
            },
            "Tidy Up Unused": {
                "image": self.up_icon,
                "state": NORMAL if flatpak_path else DISABLED,
                "tooltip": TipsText.ttip_flatpak_unused,
            },
        }

        flatpak_button_list1 = []
        conf_row = 0
        conf_column = 0

        for flatpak_button, config in flatpak_button_dict.items():
            self.flatpak_button_x = ttk.Button(
                self.flatpak_frame,
                #justify="left",
                compound="left",
                #anchor="w",
                text=flatpak_button,
                command=lambda btn=flatpak_button: flatpak_action(btn),
                #borderwidth=0,
                #highlightthickness=0,
                #background=ext_btn,
                #foreground=ext_btn_font,
                state=config.get("state", NORMAL),
                width=20
            )
            self.flatpak_button_x.grid(
                row=conf_row, column=conf_column, padx=5, pady=5, sticky="ew"
            )
            flatpak_button_list1.append(self.flatpak_button_x)
            conf_column += 1

            if conf_column == 1:
                conf_row += 1
                conf_column = 0

            self.flatpak_button_x.config(image=config["image"], state=config["state"])
            self.flatpak_button_x_ttp = CreateToolTip(
                self.flatpak_button_x, config["tooltip"]
            )

        def snap_action(text):
            """Passes commands for auto-generated buttons"""
            frame_width = self.termf.winfo_width()
            frame_height = self.termf.winfo_height()
            print(
                "The width & height of the label is:",
                frame_width,
                frame_height,
                "pixels",
            )

            if text == "Update":
                os.popen(
                    f'xterm -into %d -bg Grey11 -geometry {frame_height}x{frame_width} -e "{permit} snap refresh && sleep 5 && exit ; exec bash"'
                    % wid
                )

        self.snap_frame = ttk.LabelFrame(
            self.update_btn_frame,
            text="Snap Options",
            #font=font_16,
            #foreground=label_frame_color,
            #borderwidth=0,
            #relief=GROOVE,
            #highlightthickness=0,
            #background=frame_color,
            #pady=10,
        )
        self.snap_frame.pack(anchor="n", fill="x", expand=True)

        self.snap_frame.columnconfigure(0, weight=1)
        self.snap_frame.rowconfigure(0, weight=1)

        snap_button_dict = {
            "Update": {
                "image": self.up_icon,
                "state": NORMAL if is_snap_installed() else DISABLED,
            },
        }

        snap_button_list1 = []
        conf_row = 0
        conf_column = 0

        for snap_button, config in snap_button_dict.items():
            self.snap_button_x = ttk.Button(
                self.snap_frame,
                #justify="left",
                compound="left",
                #anchor="w",
                text=snap_button,
                command=lambda btn=snap_button: snap_action(btn),
                #borderwidth=0,
                #highlightthickness=0,
                #background=ext_btn,
                #foreground=ext_btn_font,
                state=config.get("state", NORMAL),
                width=20
            )
            self.snap_button_x.grid(
                row=conf_row, column=conf_column, padx=5, pady=5, sticky="ew"
            )
            snap_button_list1.append(self.snap_button_x)
            conf_column += 1

            if conf_column == 1:
                conf_row += 1
                conf_column = 0

            self.snap_button_x.config(image=config["image"], state=config["state"])
