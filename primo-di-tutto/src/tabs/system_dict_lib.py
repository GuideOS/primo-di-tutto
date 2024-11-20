from resorcess import *

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
        "sys_8": {
            "Name": "Anmeldefenster",
            "Description": "Öffnet die Einstellungen für das Anmeldefenster (LightDM).",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "lightdm-gtk-greeter-settings-pkexec",
            "Path": "System Settings",
        },
        "sys_9": {
            "Name": "Benutzer",
            "Description": "Öffnet die Benutzerverwaltung, um Benutzerkonten zu verwalten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "cinnamon-settings-users",
            "Path": "System Settings",
        },
        "sys_10": {
            "Name": "Systemmonitor",
            "Description": "Zeigt die Systemressourcen und die aktuelle Systemauslastung in Echtzeit an.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png",
            "Action": "gnome-system-monitor",
            "Path": "System Utilities",
        },
        "sys_11": {
            "Name": "Energieverwaltung",
            "Description": "Ermöglicht die Überwachung und Verwaltung von Energieverbrauch und Akkustand.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png",
            "Action": "cinnamon-settings power",
            "Path": "System Utilities",
        },
        "sys_12": {
            "Name": "Applet-Einstellungen",
            "Description": "Ermöglicht die Verwaltung und Anpassung von Cinnamon-Applets.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/com.github.cassidyjames.palette.png",
            "Action": "cinnamon-settings applets",
            "Path": "Cinnamon Settings",
        },
        "sys_13": {
            "Name": "Barrierefreiheit",
            "Description": "Zugang zu Einstellungen, die die Barrierefreiheit des Systems verbessern.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "cinnamon-settings accessibility",
            "Path": "Cinnamon Settings",
        },
        "sys_14": {
            "Name": "Erweiterungen",
            "Description": "Ermöglicht die Verwaltung und Installation von Cinnamon-Erweiterungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/org.gnome.Extensions.png",
            "Action": "cinnamon-settings extensions",
            "Path": "Cinnamon Settings",
        },
        "sys_15": {
            "Name": "Laufwerke",
            "Description": "Öffnet das Verwaltungstool für Festplatten und Partitionen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/blivet-gui.png",
            "Action": "gnome-disks",
            "Path": "System Utilities",
        },
        "sys_16": {
            "Name": "Startprogramme",
            "Description": "Verwalte Programme, die beim Systemstart ausgeführt werden.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/cs-startup-programs.png",
            "Action": "cinnamon-settings startup",
            "Path": "Cinnamon Settings",
        },
        "sys_17": {
            "Name": "Netzwerkeinstellungen",
            "Description": "Ermöglicht die Verwaltung von Netzwerkverbindungen und -einstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/blueman-server.png",
            "Action": "cinnamon-settings network",
            "Path": "Cinnamon Settings",
        },
        "sys_18": {
            "Name": "Standardprogramme",
            "Description": "Ermöglicht die Änderung der Standardprogramme für bestimmte Aktionen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/gnome-todo.png",
            "Action": "cinnamon-settings default",
            "Path": "Cinnamon Settings",
        },
        "sys_19": {
            "Name": "Allgemeine Einstellungen",
            "Description": "Zugang zu allgemeinen Systemeinstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/kcontrol.png",
            "Action": "cinnamon-settings general",
            "Path": "Cinnamon Settings",
        },
        "sys_20": {
            "Name": "Menu Editor",
            "Description": "Ermöglicht die Bearbeitung von Menüeinträgen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/kcontrol.png",
            "Action": "/usr/bin/menulibre",
            "Path": "Cinnamon Settings",
        },
    }

    


