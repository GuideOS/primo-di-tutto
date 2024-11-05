from resorcess import *

class SoftwareSys:
    sys_dict = {

        "sys_0": {
            "Name": "Bash History",
            "Description": "Öffnet die Datei bash_history in deinem HOME-Verzeichnis. Es wird eine Auflisting aller ausgeführen Befehle angezeigt.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/bash.png",
            "Action": f"xdg-open {home}/.bash_history",
            "Path": "Bash History",
        },
        "sys_1": {
            "Name": "Cron Job",
            "Description": "Ein Cron Job ist ein geplanter Task, der auf Unix- oder Linux-Systemen automatisch zu festgelegten Zeiten oder Intervallen ausgeführt wird. Cron Jobs werden mithilfe des `cron`-Dienstes und der `crontab`-Datei eingerichtet und sind nützlich für regelmäßige Aufgaben wie Backups, Updates oder das Ausführen von Skripten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/mousepad.png",
            "Action": f"{permit} mousepad /etc/crontab",
            "Path": "Bash History",
        },
        "sys_2": {
            "Name": "dmesg --follow",
            "Description": "'dmesg --follow' zeigt neue Kernel-Meldungen in Echtzeit an. Es ist nützlich, um laufend aktuelle Systemereignisse oder Fehler direkt zu überwachen.",            
            "Icon": f"{application_path}/images/icons/papirus/48x48/deepin-log-viewer.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg --follow; exec bash\"'",
            "Path": "Bash History",
        },
        "sys_3": {
            "Name": "dmesg",
            "Description": "'dmesg' zeigt die Systemmeldungen des Kernels an, die beim Hochfahren und während des Betriebs gesammelt werden. Diese Meldungen helfen, Probleme mit der Hardware oder dem System zu diagnostizieren und geben Einblick in den aktuellen Systemstatus.",            
            "Icon": f"{application_path}/images/icons/papirus/48x48/deepin-log-viewer.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dmesg; exec bash\"'",
            "Path": "Bash History",
        },
        "sys_4": {
            "Name": "FM God Mode",
            "Description": "Öffnet den File-Browser mit erhöhten Rechten.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/folder-yellow.png",
            "Action": f"{permit} nemo",
            "Path": "Bash History",
        },
        "sys_5": {
            "Name": "Gparted",
            "Description": "Ein schneller, sicherheitsorientierter Browser, der Werbung blockiert und Tracker blockiert. Basiert auf Chromium und fokussiert auf Datenschutz. Unterstützt eine Vielzahl an Erweiterungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/bash.png",
            "Action": "",
            "Path": "Bash History",
        },
        "sys_6": {
            "Name": "Reconfigure Keyboard",
            "Description": "Es wird der befehlt 'dpkg-reconfigure keyboard-configuration' ausgeführt. Hiermit lässt sich die Tastaturbelegung anpassen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/gnome-settings-keybinding.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dpkg-reconfigure keyboard-configuration; exec bash\"'",
            "Path": "Bash History",
        },
        "sys_7": {
            "Name": "Reconfigure Locales",
            "Description": "Es wird der befehlt 'dpkg-reconfigure locales' ausgeführt. Hiermit lässt sich die System-Sprache ändern.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "x-terminal-emulator -e 'bash -c \"pkexec dpkg-reconfigure locales; exec bash\"'",
            "Path": "Bash History",
        },
        "sys_8": {
            "Name": "Anmeldefenster",
            "Description": "Es wird der befehlt 'dpkg-reconfigure locales' ausgeführt. Hiermit lässt sich die System-Sprache ändern.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "pkexec lightdm-settings",
            "Path": "Bash History",
        },
        "sys_9": {
            "Name": "Benutzer",
            "Description": "Es wird der befehlt 'dpkg-reconfigure locales' ausgeführt. Hiermit lässt sich die System-Sprache ändern.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "cinnamon-settings-users",
            "Path": "Bash History",
        },
        "sys_10": {
            "Name": "Systemmonitor",
            "Description": "Zeigt die Systemressourcen und -auslastung in Echtzeit an.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png",
            "Action": "gnome-system-monitor",
            "Path": "System Utilities",
        },
        "sys_11": {
            "Name": "Energieverwaltung",
            "Description": "Verwalte und überwache den Energieverbrauch und Akkustand.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/appimagekit-gqrx.png",
            "Action": "gnome-power-statistics",
            "Path": "System Utilities",
        },
        "sys_12": {
            "Name": "Applet-Einstellungen",
            "Description": "Verwalte und passe Cinnamon-Applets an.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/com.github.cassidyjames.palette.png",
            "Action": "cinnamon-settings applets",
            "Path": "Cinnamon Settings",
        },
        "sys_13": {
            "Name": "Barrierefreiheit",
            "Description": "Einstellungen zur Verbesserung der Barrierefreiheit im System.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/desktop-effects.png",
            "Action": "cinnamon-settings accessibility",
            "Path": "Cinnamon Settings",
        },
        "sys_14": {
            "Name": "Erweiterungen",
            "Description": "Verwalte und installiere Cinnamon-Erweiterungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/org.gnome.Extensions.png",
            "Action": "cinnamon-settings extensions",
            "Path": "Cinnamon Settings",
        },
        "sys_15": {
            "Name": "Laufwerke",
            "Description": "Verwaltungstool für Festplatten und Partitionen.",
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
            "Description": "Verwalte Netzwerkverbindungen und -einstellungen.",
            "Icon": f"{application_path}/images/icons/papirus/48x48/blueman-server.png",
            "Action": "cinnamon-settings network",
            "Path": "Cinnamon Settings",
        },
        "sys_18": {
            "Name": "Standardprogramme",
            "Description": "Ändere die Standardprogramme für bestimmte Aktionen.",
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
        }
    }
    


