from resorcess import *

class SoftwareGame:
    game_dict = {
            "game_0": {
                "Name": "Steam",
                "Package": "DEB",
                "Description": "Steam ist ein Programm zum herunterladen, kaufen und spielen von Games unter Linux ",
                "Icon": f"{application_path}/images/apps/steam_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-steam-thumb.png",
                "Install": "pkexec apt install neofetch -y",
                "Uninstall":  "pkexec apt remove neofetch -y",
                "Path": "neofetch"
            },
            "game_1": {
                "Name": "Lutris",
                "Package": "Debian-Paket",
                "Description": "Bundle das Wine und Lutris installiert",
                "Icon": f"{application_path}/images/apps/lutris_logo_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-lutris-thumb.png",
                "Install":  f"{application_path}/scripts/install_lutris",
                "Uninstall":  "pkexec apt remove lutris",
                "Path": "lutris"
            },
            "game_2": {
                "Name": "Heroic",
                "Package": "Flatpak",
                "Description": "Ein Tool zum Zocken",
                "Icon": f"{application_path}/images/apps/heroic_icon_36.png",
                "Install": "flatpak install flathub com.heroicgameslauncher.hgl -y",
                "Thumbnail": f"{application_path}/images/apps/soft-steam-thumb.png",
                "Uninstall": "flatpak remove com.heroicgameslauncher.hgl -y",
                "Path": "com.heroicgameslauncher.hgl"
            },
            "game_3": {
                "Name": "ProtonUp-Qt",
                "Package": "Flatpak",
                "Description": "Ein Tool zum Zocken",
                "Icon": f"{application_path}/images/apps/proton_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-protonqt-thumb.png",
                "Install": "flatpak install flathub net.davidotek.pupgui2 -y",
                "Uninstall": "flatpak remove net.davidotek.pupgui2 -y",
                "Path": "ProtonUp-Qt"
            },
            "game_4": {
                "Name": "ProtonDB",
                "Package": "Website",
                "Description": "Ein Tool zum Zocken",
                "Icon": f"{application_path}/images/apps/protondb_icon_36.png",
                "Install":  "",
                "Path": "https://www.protondb.com/"
            },
    }






class Update_Tab_Buttons:
    # Contrib by @staryvyr
    up_button_dict = {
        "Paketliste erneuern": "Liste der verfügbaren, aktuellen Pakete auf den neuesten Stand bringen.",
        "Pakete erneuern": "Paketliste aktualisieren und alte Pakete durch aktuelle Pakete ersetzen.",
        "Aktualisierbarkeit": "Aktualisierbare Pakete auflisten.",
        "Vervollständigen": "Fehlende Abhängigkeiten/Pakete ergänzen.",
        "Reparieren": "Defekte Pakete reparieren.",
        "Aufräumen": "Automatisch installierte Pakete, die nicht mehr gebraucht werden, löschen.",
        "Konfigurieren": "Entpackte, aber nicht konfigurierte Pakete konfigurieren.",
        ".DEB installieren": "Ein Paket mit Hilfe einer lokalen Datei mit der Endung .deb installieren.",
    }


class SystemTabDict:
    commands_dict = {
        "Bash History": "View and manage the command history in the Bash shell.",
        "Cron Job": "Schedule and automate tasks using cron jobs.",
        "DeskpiPro Control": "Control and configure the DeskpiPro hardware.",
        "dmesg --follow": "Display kernel messages in real-time.",
        "dmesg": "Display kernel ring buffer messages.",
        "Edit Config.txt": "Edit the configuration file for system settings.",
        "FM God Mode": "Access advanced file management features.",
        "Gnome Extensions": "Manage and configure extensions for the Gnome desktop environment.",
        "Gnome Settings": "Access general settings for the Gnome desktop environment.",
        "Gnome Software\nUpdates": "Manage and install software updates in Gnome.",
        "Gnome Tweaks": "Customize and tweak various Gnome desktop settings.",
        "Gnome Update\nSettings": "Configure update settings for the Gnome desktop environment.",
        "Gparted": "Graphical partition editor for managing disk partitions.",
        "Menu Settings\nAlacart": "Configure menu settings using Alacart.",
        "NeoFetch": "Display system information and logo in the terminal.",
        "Raspi Appearance\nSettings": "Configure appearance settings on a Raspberry Pi.",
        "Raspi Bookshelf": "Access the bookshelf application on a Raspberry Pi.",
        "Raspi-Config CLI": "Configure Raspberry Pi settings via the command line.",
        "Raspi-Config GUI": "Configure Raspberry Pi settings using the graphical interface.",
        "Raspi Diagnostics": "Run diagnostics and check the health of a Raspberry Pi.",
        "Raspi Mouse & Keyboard": "Configure mouse and keyboard settings on a Raspberry Pi.",
        "Raspi Printer Settings": "Configure printer settings on a Raspberry Pi.",
        "Raspi Screen Settings": "Adjust screen settings on a Raspberry Pi.",
        "Raspi SD Card Copier": "Copy the contents of a Raspberry Pi SD card to another.",
        "Raspi Recommended Software": "View and install recommended software for a Raspberry Pi.",
        "Reconfigure Keyboard": "Reconfigure keyboard layout settings.",
        "Reconfigure Locales": "Reconfigure system locales and language settings.",
        "Update-Alternatives": "Manage symbolic links determining default commands.",
        "Xfce Settings": "Access settings for the Xfce desktop environment.",
    }

    # Beispielaufruf:
    # Beschreibung für den Befehl "Bash History"
    # print(commands_dict["Bash History"])
