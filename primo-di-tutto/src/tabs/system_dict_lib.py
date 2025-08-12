from resorcess import *

class CinnamonLook:
    cinna_look_dict = {
        "look_0": {
            "Name": "Effekte",
            "Description": "Öffnet die Einstellungen für die Desktop-Effekte von Cinnamon.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/plasmagik.png",
            "Action": "cinnamon-settings effects",
            "Path": "Cinnamon Settings",
        },
        "look_1": {
            "Name": "Hintergrund",
            "Description": "Öffnet die Einstellungen für den Desktop-Hintergrund.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-wallpaper.png",
            "Action": "cinnamon-settings background",
            "Path": "Cinnamon Settings",
        },
        "look_2": {
            "Name": "Schriftarten",
            "Description": "Öffnet die Einstellungen für die Schriftarten von Cinnamon.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-font.png",
            "Action": "cinnamon-settings fonts",
            "Path": "Cinnamon Settings",
        },
    } 

class CinnamonSettings:
    cinna_sett_dict = {
        "sett_0": {
            "Name": "Hotcorner",
            "Description": "Öffnet die Einstellungen für die Hotcorner von Cinnamon.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-overview.png",
            "Action": "cinnamon-settings hotcorner",
            "Path": "Cinnamon Settings",
        },
        "sett_1": {
            "Name": "Allgemeine Einstellungen",
            "Description": "Öffnet die allgemeinen Einstellungen von Cinnamon.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/applets-template.png",
            "Action": "cinnamon-settings general",
            "Path": "Cinnamon Settings",
        },
        "sett_2": {
            "Name": "Applets",
            "Description": "Öffnet die Einstellungen für die Applets von Cinnamon.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-applets.png",
            "Action": "cinnamon-settings applets",
            "Path": "Cinnamon Settings",
        },
        "sett_3": {
            "Name": "Barrierefreiheit",
            "Description": "Öffnet die Einstellungen für die Barrierefreiheit.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-accessibility.png",
            "Action": "cinnamon-settings universal-access",
            "Path": "Cinnamon Settings",
        },
        "sett_4": {
            "Name": "Standardprogramme",
            "Description": "Öffnet die Einstellungen für Standardprogramme.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-default-applications.png",
            "Action": "cinnamon-settings default",
            "Path": "Cinnamon Settings",
        },
        "sett_5": {
            "Name": "Bildschirmschoner",
            "Description": "Öffnet die Einstellungen für den Bildschirmschoner.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/xfce-system-lock.png",
            "Action": "cinnamon-settings screensaver",
            "Path": "Cinnamon Settings",
        },
        "sett_6": {
            "Name": "Datenschutz",
            "Description": "Öffnet die Datenschutzeinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-privacy.png",
            "Action": "cinnamon-settings privacy",
            "Path": "Cinnamon Settings",
        },
        "sett_7": {
            "Name": "Datum & Zeit",
            "Description": "Öffnet die Einstellungen für den Kalender.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-time.png",
            "Action": "cinnamon-settings calendar",
            "Path": "Cinnamon Settings",
        },
        "sett_8": {
            "Name": "Desklets",
            "Description": "Öffnet die Einstellungen für die Desklets.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/mynotes.png",
            "Action": "cinnamon-settings desklets",
            "Path": "Cinnamon Settings",
        },
        "sett_9": {
            "Name": "Erweiterungen",
            "Description": "Öffnet die Einstellungen für die Erweiterungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-plugin.png",
            "Action": "cinnamon-settings extensions",
            "Path": "Cinnamon Settings",
        },
        "sett_10": {
            "Name": "Fenster",
            "Description": "Öffnet die Einstellungen für Fenster.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-windows.png",
            "Action": "cinnamon-settings windows",
            "Path": "Cinnamon Settings",
        },
        "sett_11": {
            "Name": "Fenster-Tiling",
            "Description": "Öffnet die Einstellungen für das Fenster-Tiling.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-windows-move.png",
            "Action": "cinnamon-settings tiling",
            "Path": "Cinnamon Settings",
        },
        "sett_12": {
            "Name": "Online-Konten",
            "Description": "Öffnet die Einstellungen für Online-Konten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-online-accounts.png",
            "Action": "gnome-online-accounts-gtk",
            "Path": "Cinnamon Settings",
        },
        "sett_13": {
            "Name": "Benutzer",
            "Description": "Öffnet die Einstellungen für Benutzer.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/system-users.png",
            "Action": "cinnamon-settings user",
            "Path": "Cinnamon Settings",
        },
        "sett_14": {
            "Name": "Panel",
            "Description": "Öffnet die Einstellungen für das Panel.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-panel.png",
            "Action": "cinnamon-settings panel",
            "Path": "Cinnamon Settings",
        },
        "sett_15": {
            "Name": "Benachrichtigungen",
            "Description": "Öffnet die Einstellungen für Benachrichtigungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-notifications.png",
            "Action": "cinnamon-settings notifications",
            "Path": "Cinnamon Settings",
        },
        "sett_16": {
            "Name": "Desktop",
            "Description": "Öffnet die Einstellungen für den Desktop.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-desktop.png",
            "Action": "cinnamon-settings desktop",
            "Path": "Cinnamon Settings",
        },
        "sett_17": {
            "Name": "Autostart",
            "Description": "Öffnet die Einstellungen für Autostart-Programme.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-startup-programs.png",
            "Action": "cinnamon-settings startup",
            "Path": "Cinnamon Settings",
        },
    }

class SoftwareSys:
    sys_dict = {
        "sys_0": {
            "Name": "Bash History",
            "Description": "Öffnet die Datei `.bash_history` im HOME-Verzeichnis. Eine Auflistung aller ausgeführten Befehle wird angezeigt.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/bash.png",
            "Action": f"xdg-open {home}/.bash_history",
            "Path": "Bash History",
        },
        "sys_1": {
            "Name": "Cron Job",
            "Description": "Ein Cron-Job ist ein geplanter Task, der auf Unix- oder Linux-Systemen automatisch zu festgelegten Zeiten oder Intervallen ausgeführt wird. Cron-Jobs werden mithilfe des `cron`-Dienstes und der `crontab`-Datei eingerichtet. Sie sind nützlich für regelmäßige Aufgaben wie Backups, Updates oder das Ausführen von Skripten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/mousepad.png",
            "Action": f"{permit} mousepad /etc/crontab",
            "Path": "Cron Jobs",
        },
        "sys_2": {
            "Name": "dmesg --follow",
            "Description": "'dmesg --follow' zeigt neue Kernel-Meldungen in Echtzeit an. Es ist nützlich, um aktuelle Systemereignisse oder Fehler direkt zu überwachen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/deepin-log-viewer.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg --follow; exec bash\"'",
            "Path": "Kernel Logs",
        },
        "sys_3": {
            "Name": "dmesg",
            "Description": "'dmesg' zeigt die Systemmeldungen des Kernels an, die beim Hochfahren und während des Betriebs gesammelt werden. Diese Meldungen helfen, Hardware- oder Systemprobleme zu diagnostizieren und geben Einblick in den aktuellen Systemstatus.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/deepin-log-viewer.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg; exec bash\"'",
            "Path": "Kernel Logs",
        },
        "sys_4": {
            "Name": "FM God Mode",
            "Description": "Öffnet den Dateimanager mit erhöhten Rechten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/folder-yellow.png",
            "Action": f"{permit} nemo",
            "Path": "File Manager",
        },
        "sys_10": {
            "Name": "Systemmonitor",
            "Description": "Zeigt die Systemressourcen und die aktuelle Systemauslastung in Echtzeit an.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png",
            "Action": "gnome-system-monitor",
            "Path": "System Utilities",
        },
        "sys_20": {
            "Name": "Menu Editor",
            "Description": "Ermöglicht die Bearbeitung von Menüeinträgen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/kcontrol.png",
            "Action": "/usr/bin/alacarte",
            "Path": "Cinnamon Settings",
        },
        "sys_21": {
            "Name": "Nvidia-\nTreiberinstallation",
            "Description": "Installiere den proprietären Nvidia-Treiber aus dem Repository.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/nvidia.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec /usr/bin/ddm-mx -i nvidia; exec bash\"'",
            "Path": "ddm-mx",
        },
    }

class DeviceSettings:
    device_sett_dict = {
        "device_0": {
            "Name": "Bildschirm",
            "Description": "Öffnet die Einstellungen für die Bildschirmanzeige.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-display.png",
            "Action": "cinnamon-settings display",
            "Path": "Device Settings",
        },
        "device_1": {
            "Name": "Drucker",
            "Description": "Öffnet die Druckereinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/boomaga.png",
            "Action": "system-config-printer",
            "Path": "Device Settings",
        },
        "device_2": {
            "Name": "Energieverwaltung",
            "Description": "Öffnet die Energieverwaltungseinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-system-power.png",
            "Action": "cinnamon-settings power",
            "Path": "Device Settings",
        },
        "device_3": {
            "Name": "Farbverwaltung",
            "Description": "Öffnet die Einstellungen für die Farbverwaltung.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-color.png",
            "Action": "cinnamon-settings color",
            "Path": "Device Settings",
        },
        "device_4": {
            "Name": "Wacom",
            "Description": "Öffnet die Einstellungen für Wacom-Geräte.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/input-tablet.png",
            "Action": "cinnamon-settings wacom",
            "Path": "Device Settings",
        },
        "device_5": {
            "Name": "Sound",
            "Description": "Öffnet die Klangeinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/yast-sound.png",
            "Action": "cinnamon-settings sound",
            "Path": "Device Settings",
        },
        "device_6": {
            "Name": "Laufwerke",
            "Description": "Öffnet das Verwaltungstool für Festplatten und Partitionen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/org.gnome.DiskUtility.png",
            "Action": "gnome-disks",
            "Path": "Device Settings",
        },
        "device_7": {
            "Name": "Maus und Touchpad",
            "Description": "Öffnet die Einstellungen für Maus und Touchpad.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-peripherals.png",
            "Action": "cinnamon-settings mouse",
            "Path": "Device Settings",
        },
        "device_8": {
            "Name": "Netzwerk",
            "Description": "Öffnet die Netzwerkeinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/blueman-server.png",
            "Action": "cinnamon-settings network",
            "Path": "Device Settings",
        },
        "device_9": {
            "Name": "Systeminformationen",
            "Description": "Zeigt die Systeminformationen an.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/hwinfo.png",
            "Action": "cinnamon-settings info",
            "Path": "Device Settings",
        },
        "device_10": {
            "Name": "Tastatur",
            "Description": "Öffnet die Einstellungen für die Tastatur.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/preferences-desktop-keyboard.png",
            "Action": "cinnamon-settings keyboard",
            "Path": "Device Settings",
        },
    }

class SystemManagement:
    sys_mgmt_dict = {
        "sys_mgmt_0": {
            "Name": "Anmeldefenster",
            "Description": "Öffnet die Einstellungen für das Anmeldefenster (LightDM).",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-login.png",
            "Action": "pkexec lightdm-settings",
            "Path": "System Management",
        },
        "sys_mgmt_1": {
            "Name": "Benutzerverwaltung",
            "Description": "Öffnet die Benutzerverwaltung, um Benutzerkonten zu verwalten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/kaddressbook.png",
            "Action": "cinnamon-settings-users",
            "Path": "System Management",
        },
        "sys_mgmt_2": {
            "Name": "Firewall",
            "Description": "Öffnet die Firewall-Einstellungen (GUFW).",
            "Icon": f"{application_path}/images/icons/papirus/48x48/gufw.png",
            "Action": "gufw",
            "Path": "System Management",
        },
    }




