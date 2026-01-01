from resorcess import *


class CinnamonLook:
    cinna_look_dict = {
        "look_0": {
            "Name": "Effekte",
            "Description": "Öffnet die Einstellungen für die Desktop-Effekte von Cinnamon.",
            "Icon": "plasmagik",
            "Action": "cinnamon-settings effects",
            "Path": "Cinnamon Settings",
        },
        "look_1": {
            "Name": "Hintergrund",
            "Description": "Öffnet die Einstellungen für den Desktop-Hintergrund.",
            "Icon": "preferences-desktop-wallpaper",
            "Action": "cinnamon-settings background",
            "Path": "Cinnamon Settings",
        },
        "look_2": {
            "Name": "Schriftarten",
            "Description": "Öffnet die Einstellungen für die Schriftarten von Cinnamon.",
            "Icon": "preferences-desktop-font",
            "Action": "cinnamon-settings fonts",
            "Path": "Cinnamon Settings",
        },
    }


class CinnamonSettings:
    cinna_sett_dict = {
        "sett_0": {
            "Name": "Hotcorner",
            "Description": "Öffnet die Einstellungen für die Hotcorner von Cinnamon.",
            "Icon": "cs-overview",
            "Action": "cinnamon-settings hotcorner",
            "Path": "Cinnamon Settings",
        },
        "sett_1": {
            "Name": "Allgemeine Einstellungen",
            "Description": "Öffnet die allgemeinen Einstellungen von Cinnamon.",
            "Icon": "preferences-system",
            "Action": "cinnamon-settings general",
            "Path": "Cinnamon Settings",
        },
        "sett_2": {
            "Name": "Applets",
            "Description": "Öffnet die Einstellungen für die Applets von Cinnamon.",
            "Icon": "cs-applets",
            "Action": "cinnamon-settings applets",
            "Path": "Cinnamon Settings",
        },
        "sett_3": {
            "Name": "Barrierefreiheit",
            "Description": "Öffnet die Einstellungen für die Barrierefreiheit.",
            "Icon": "preferences-desktop-accessibility",
            "Action": "cinnamon-settings universal-access",
            "Path": "Cinnamon Settings",
        },
        "sett_4": {
            "Name": "Standardprogramme",
            "Description": "Öffnet die Einstellungen für Standardprogramme.",
            "Icon": "preferences-desktop-default-applications",
            "Action": "cinnamon-settings default",
            "Path": "Cinnamon Settings",
        },
        "sett_5": {
            "Name": "Bildschirmschoner",
            "Description": "Öffnet die Einstellungen für den Bildschirmschoner.",
            "Icon": "preferences-desktop-screensaver",
            "Action": "cinnamon-settings screensaver",
            "Path": "Cinnamon Settings",
        },
        "sett_6": {
            "Name": "Datenschutz",
            "Description": "Öffnet die Datenschutzeinstellungen.",
            "Icon": "preferences-system-privacy",
            "Action": "cinnamon-settings privacy",
            "Path": "Cinnamon Settings",
        },
        "sett_7": {
            "Name": "Datum & Zeit",
            "Description": "Öffnet die Einstellungen für den Kalender.",
            "Icon": "preferences-system-time",
            "Action": "cinnamon-settings calendar",
            "Path": "Cinnamon Settings",
        },
        "sett_8": {
            "Name": "Desklets",
            "Description": "Öffnet die Einstellungen für die Desklets.",
            "Icon": "cs-desklets",
            "Action": "cinnamon-settings desklets",
            "Path": "Cinnamon Settings",
        },
        "sett_9": {
            "Name": "Erweiterungen",
            "Description": "Öffnet die Einstellungen für die Erweiterungen.",
            "Icon": "cs-extensions",
            "Action": "cinnamon-settings extensions",
            "Path": "Cinnamon Settings",
        },
        "sett_10": {
            "Name": "Fenster",
            "Description": "Öffnet die Einstellungen für Fenster.",
            "Icon": "preferences-system-windows",
            "Action": "cinnamon-settings windows",
            "Path": "Cinnamon Settings",
        },
        "sett_11": {
            "Name": "Fenster-Tiling",
            "Description": "Öffnet die Einstellungen für das Fenster-Tiling.",
            "Icon": "preferences-system-windows-move",
            "Action": "cinnamon-settings tiling",
            "Path": "Cinnamon Settings",
        },
        "sett_12": {
            "Name": "Online-Konten",
            "Description": "Öffnet die Einstellungen für Online-Konten.",
            "Icon": "preferences-desktop-online-accounts",
            "Action": "gnome-online-accounts-gtk",
            "Path": "Cinnamon Settings",
        },
        "sett_13": {
            "Name": "Benutzer",
            "Description": "Öffnet die Einstellungen für Benutzer.",
            "Icon": "system-users",
            "Action": "cinnamon-settings user",
            "Path": "Cinnamon Settings",
        },
        "sett_14": {
            "Name": "Panel",
            "Description": "Öffnet die Einstellungen für das Panel.",
            "Icon": "cs-panel",
            "Action": "cinnamon-settings panel",
            "Path": "Cinnamon Settings",
        },
        "sett_15": {
            "Name": "Benachrichtigungen",
            "Description": "Öffnet die Einstellungen für Benachrichtigungen.",
            "Icon": "preferences-system-notifications",
            "Action": "cinnamon-settings notifications",
            "Path": "Cinnamon Settings",
        },
        "sett_16": {
            "Name": "Desktop",
            "Description": "Öffnet die Einstellungen für den Desktop.",
            "Icon": "cs-desktop",
            "Action": "cinnamon-settings desktop",
            "Path": "Cinnamon Settings",
        },
        "sett_17": {
            "Name": "Autostart",
            "Description": "Öffnet die Einstellungen für Autostart-Programme.",
            "Icon": "cs-startup-programs",
            "Action": "cinnamon-settings startup",
            "Path": "Cinnamon Settings",
        },
    }


class SoftwareSys:
    sys_dict = {
        "sys_0": {
            "Name": "Bash History",
            "Description": "Öffnet die Datei `.bash_history` im HOME-Verzeichnis. Eine Auflistung aller ausgeführten Befehle wird angezeigt.",
            "Icon": "utilities-terminal",
            "Action": f"xdg-open {home}/.bash_history",
            "Path": "Bash History",
        },
        "sys_1": {
            "Name": "Cron Job",
            "Description": "Ein Cron-Job ist ein geplanter Task, der auf Unix- oder Linux-Systemen automatisch zu festgelegten Zeiten oder\nIntervallen ausgeführt wird. Cron-Jobs werden mithilfe des `cron`-Dienstes\nund der `crontab`-Datei eingerichtet. Sie sind nützlich für regelmäßige Aufgaben wie Backups,\nUpdates oder das Ausführen von Skripten.",
            "Icon": "text-editor",
            "Action": f"{permit} mousepad /etc/crontab",
            "Path": "Cron Jobs",
        },
        "sys_2": {
            "Name": "dmesg --follow",
            "Description": "'dmesg --follow' zeigt neue Kernel-Meldungen in Echtzeit an. Es ist nützlich, um aktuelle Systemereignisse oder\nFehler direkt zu überwachen.",
            "Icon": "utilities-system-monitor",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg --follow; exec bash\"'",
            "Path": "Kernel Logs",
        },
        "sys_3": {
            "Name": "dmesg",
            "Description": "'dmesg' zeigt die Systemmeldungen des Kernels an, die beim Hochfahren und während des Betriebs gesammelt werden.\nDiese Meldungen helfen, Hardware- oder Systemprobleme zu diagnostizieren\nund geben Einblick in den aktuellen Systemstatus.",
            "Icon": "utilities-system-monitor",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg; exec bash\"'",
            "Path": "Kernel Logs",
        },
        "sys_4": {
            "Name": "FM God Mode",
            "Description": "Öffnet den Dateimanager mit erhöhten Rechten.",
            "Icon": "folder",
            "Action": f"{permit} nemo",
            "Path": "File Manager",
        },
        "sys_10": {
            "Name": "Systemmonitor",
            "Description": "Zeigt die Systemressourcen und die aktuelle Systemauslastung in Echtzeit an.",
            "Icon": "utilities-system-monitor",
            "Action": "gnome-system-monitor",
            "Path": "System Utilities",
        },
        "sys_20": {
            "Name": "Menu Editor",
            "Description": "Ermöglicht die Bearbeitung von Menüeinträgen.",
            "Icon": "alacarte",
            "Action": "/usr/bin/alacarte",
            "Path": "Cinnamon Settings",
        },
        "sys_21": {
            "Name": "Nvidia-\nTreiberinstallation",
            "Description": "Installiere den proprietären Nvidia-Treiber aus dem Repository.",
            "Icon": "video-display",
            "Action": "x-terminal-emulator -e 'pkexec /usr/bin/debian-nvidia-installer'",
            "Path": "ddm-mx",
        },
    }


class DeviceSettings:
    device_sett_dict = {
        "device_0": {
            "Name": "Bildschirm",
            "Description": "Öffnet die Einstellungen für die Bildschirmanzeige.",
            "Icon": "preferences-desktop-display",
            "Action": "cinnamon-settings display",
            "Path": "Device Settings",
        },
        "device_1": {
            "Name": "Drucker",
            "Description": "Öffnet die Druckereinstellungen.",
            "Icon": "printer",
            "Action": "system-config-printer",
            "Path": "Device Settings",
        },
        "device_2": {
            "Name": "Energieverwaltung",
            "Description": "Öffnet die Energieverwaltungseinstellungen.",
            "Icon": "preferences-system-power",
            "Action": "cinnamon-settings power",
            "Path": "Device Settings",
        },
        "device_3": {
            "Name": "Farbverwaltung",
            "Description": "Öffnet die Einstellungen für die Farbverwaltung.",
            "Icon": "preferences-desktop-color",
            "Action": "cinnamon-settings color",
            "Path": "Device Settings",
        },
        "device_4": {
            "Name": "Wacom",
            "Description": "Öffnet die Einstellungen für Wacom-Geräte.",
            "Icon": "input-tablet",
            "Action": "cinnamon-settings wacom",
            "Path": "Device Settings",
        },
        "device_5": {
            "Name": "Sound",
            "Description": "Öffnet die Klangeinstellungen.",
            "Icon": "multimedia-volume-control",
            "Action": "cinnamon-settings sound",
            "Path": "Device Settings",
        },
        "device_6": {
            "Name": "Laufwerke",
            "Description": "Öffnet das Verwaltungstool für Festplatten und Partitionen.",
            "Icon": "gnome-disks",
            "Action": "gnome-disks",
            "Path": "Device Settings",
        },
        "device_7": {
            "Name": "Maus und Touchpad",
            "Description": "Öffnet die Einstellungen für Maus und Touchpad.",
            "Icon": "input-mouse",
            "Action": "cinnamon-settings mouse",
            "Path": "Device Settings",
        },
        "device_8": {
            "Name": "Netzwerk",
            "Description": "Öffnet die Netzwerkeinstellungen.",
            "Icon": "network-workgroup",
            "Action": "cinnamon-settings network",
            "Path": "Device Settings",
        },
        "device_9": {
            "Name": "Systeminformationen",
            "Description": "Zeigt die Systeminformationen an.",
            "Icon": "computer",
            "Action": "cinnamon-settings info",
            "Path": "Device Settings",
        },
        "device_10": {
            "Name": "Tastatur",
            "Description": "Öffnet die Einstellungen für die Tastatur.",
            "Icon": "input-keyboard",
            "Action": "cinnamon-settings keyboard",
            "Path": "Device Settings",
        },
    }


class SystemManagement:
    sys_mgmt_dict = {
        "sys_mgmt_0": {
            "Name": "Anmeldefenster",
            "Description": "Öffnet die Einstellungen für das Anmeldefenster (LightDM).",
            "Icon": "cs-login",
            "Action": "pkexec lightdm-settings",
            "Path": "System Management",
        },
        "sys_mgmt_1": {
            "Name": "Benutzerverwaltung",
            "Description": "Öffnet die Benutzerverwaltung, um Benutzerkonten zu verwalten.",
            "Icon": "system-users",
            "Action": "cinnamon-settings-users",
            "Path": "System Management",
        },
        "sys_mgmt_2": {
            "Name": "Firewall",
            "Description": "Öffnet die Firewall-Einstellungen (GUFW).",
            "Icon": "network-firewall",
            "Action": "gufw",
            "Path": "System Management",
        },
    }
