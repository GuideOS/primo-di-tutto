from resorcess import *

class SoftwareOffice:
    # Descriptions by ????????????
    office_dict = {
        "office_0": {
            "Name": "LibreOffice",  # Name
            "Package": "Debian-Paket",  # Paketformat
            "Description": "Ein Office oder so",  # Beschreibung in 3 Sätzen
            "Icon": f"{application_path}/images/apps/libreoffice_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Thumbnail": f"{application_path}/images/apps/soft-libreoffice-thumb.png",  # Miniaturbild / Maximiert / Max. 742x389
            "Install": "pkexec apt install -y libreoffice-base-core libreoffice-calc libreoffice-common libreoffice-core libreoffice-draw libreoffice-gnome libreoffice-gtk3 libreoffice-help-common libreoffice-help-de libreoffice-help-en-gb libreoffice-help-en-us libreoffice-impress libreoffice-l10n-de libreoffice-l10n-en-gb libreoffice-l10n-en-za libreoffice-math libreoffice-style-colibre libreoffice-style-elementary libreoffice-style-yaru libreoffice-uiconfig-calc libreoffice-uiconfig-common libreoffice-uiconfig-draw libreoffice-uiconfig-impress libreoffice-uiconfig-math libreoffice-uiconfig-writer libreoffice-writer",
            "Uninstall": "pkexec apt autoremove --purge libreoffice* -y",  # Exakter Befehl
            "Path": "libreoffice-core",  # Name im Verwaltungs-Index
        },
    }

class SoftwareGame:
    # Descriptions by @evilware666
    game_dict = {
        "game_0": {
            "Name": "Steam",
            "Package": "DEB",
            "Description": "Steam ist eine Plattform zum Herunterladen, Kaufen und Spielen von Spielen.",
            "Icon": f"{application_path}/images/apps/steam_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-steam-thumb.png",
            "Install": "pkexec apt install neofetch -y",
            "Uninstall": "pkexec apt remove neofetch -y",
            "Path": "neofetch",
        },
        "game_1": {
            "Name": "Lutris",
            "Package": "Debian-Paket",
            "Description": "Lutris ist ein Programm, mit dem man Spiele aus verschiedenen Quellen verwalten und starten kann. Das geht auch (teilweise) mit Windows-Games.",
            "Icon": f"{application_path}/images/apps/lutris_logo_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-lutris-thumb.png",
            "Install": f"{application_path}/scripts/install_lutris",
            "Uninstall": "pkexec apt remove lutris",
            "Path": "lutris",
        },
        "game_2": {
            "Name": "Heroic",
            "Package": "Flatpak",
            "Description": "Der Heroic-Game-Launcher ist ein Programm zum Starten, Verwalten und Spielen von Epic- und GOG-Games.",
            "Icon": f"{application_path}/images/apps/heroic_icon_36.png",
            "Install": "flatpak install flathub com.heroicgameslauncher.hgl -y",
            "Thumbnail": f"{application_path}/images/apps/soft-steam-thumb.png",
            "Uninstall": "flatpak remove com.heroicgameslauncher.hgl -y",
            "Path": "com.heroicgameslauncher.hgl",
        },
        "game_3": {
            "Name": "ProtonUp-Qt",
            "Package": "Flatpak",
            "Description": "ProtonUp-Qt ist ein Programm für Proton-Versionen und andere Kompatibilitätsschichten wie Wine-GE für Steam und Lutris.",
            "Icon": f"{application_path}/images/apps/proton_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-protonqt-thumb.png",
            "Install": "flatpak install flathub net.davidotek.pupgui2 -y",
            "Uninstall": "flatpak remove net.davidotek.pupgui2 -y",
            "Path": "ProtonUp-Qt",
        },
        "game_4": {
            "Name": "ProtonDB",
            "Package": "Website",
            "Description": "ProtonDB ist eine Community-Datenbank, in der Tipps und Empfehlungen zur Konfiguration von Windows-Spielen unter Linux gesammelt werden.",
            "Icon": f"{application_path}/images/apps/protondb_icon_36.png",
            "Install": "",
            "Path": "https://www.protondb.com/",
        },
        "game_5": {
            "Name": "GZDoom",
            "Package": "Flatpak",
            "Description": "GZDoom ist ein moderner Source-Port, der aktuelle Hardware und Betriebssysteme unterstützt und eine Vielzahl an Einstellungsmöglichkeiten bietet. Neben Doom unterstützt GZDoom auch Heretic, Hexen, Strife, Chex Quest und von Fans erstellte Spiele wie Harmony und Hacx.",
            "Icon": f"{application_path}/images/apps/gzdoom_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-gzdoom-thumb.png",
            "Install": "flatpak install flathub org.zdoom.GZDoom -y",
            "Uninstall": "flatpak remove flathub org.zdoom.GZDoom -y",
            "Path": "GZDoom",
        },
        "game_6": {
            "Name": "OpenRA",
            "Package": "Flatpak",
            "Description": "OpenRA ist ein Projekt, das die klassischen Command-&-Conquer-Echtzeit-Strategiespiele neu erschafft und modernisiert.",
            "Icon": f"{application_path}/images/apps/openra_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-openra-thumb.png",
            "Install": "flatpak install flathub net.openra.OpenRA",
            "Uninstall": "flatpak remove flathub net.openra.OpenRA -y",
            "Path": "net.openra.OpenRA",
        },

        "game_7": {
            "Name": "Xonotic",
            "Package": "Flatpak",
            "Description": "Xonotic ist ein kostenloser und rasantes First-Person-Shooter, der süchtig machendes Arena-Gameplay mit schneller Bewegung und einer großen Auswahl an Waffen kombiniert.",
            "Icon": f"{application_path}/images/apps/xonotic_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-xonotic-thumb.png",
            "Install": "flatpak install flathub org.xonotic.Xonotic -y",
            "Uninstall": "flatpak remove flathub org.xonotic.Xonotic -y",
            "Path": "org.xonotic.Xonotic",
        },

        "game_8": {
            "Name": "Frogatto & Friends",
            "Package": "Flatpak",
            "Description": "Ein Old-School-2D-Plattformspiel mit einem gewissen eigenwilligen Frosch in der Hauptrolle. *Frogatto* bietet wunderschöne, hochwertige Pixelgrafik, mitreißende Arcade-Soundtracks und das ganze Spielgefühl eines klassischen Konsolentitels. Renne und springe über Abgründe und Gegner. Greife Feinde mit deiner Zunge, verschlucke sie und spucke sie dann als Projektile auf andere Gegner!",
            "Icon": f"{application_path}/images/apps/frogatto_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-frogatto-thumb.png",
            "Install": "flatpak install flathub com.frogatto.Frogatto -y",
            "Uninstall": "flatpak remove flathub com.frogatto.Frogatto -y",
            "Path": "com.frogatto.Frogatto",
        },

        "game_9": {
            "Name": "Bombermaaan",
            "Package": "Flatpak",
            "Description": "Ein klassisches *Bomberman*-Spiel mit Mehrspielerunterstützung, inspiriert von den originalen SNES-Spielen.",
            "Icon": f"{application_path}/images/apps/bombermaaan_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-bombermaaan-thumb.png",
            "Install": "flatpak install flathub com.github.bjaraujo.Bombermaaan -y",
            "Uninstall": "flatpak remove flathub com.github.bjaraujo.Bombermaaan -y",
            "Path": "com.github.bjaraujo.Bombermaaan",
        },

    }


class SoftwareBrowser:
    # Descriptions by ????????????
    browser_dict = {
        "browser_0": {
            "Name": "Firefox",  # Name
            "Package": "Snap",  # Paketformat
            "Description": "Ein Browser oder so",  # Beschreibung in 3 Sätzen
            "Icon": f"{application_path}/images/apps/firefox_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Thumbnail": f"{application_path}/images/apps/soft-firefox-thumb.png",  # Miniaturbild / Maximiert / Max. 742x389
            "Install": "pkexec snap install firefox",  # Exakter Befehl
            "Uninstall": "pkexec snap remove firefox",  # Exakter Befehl
            "Path": "firefox",  # Name im Verwaltungs-Index
        },
        "browser_1": {
            "Name": "Brave Browser",
            "Package": "Debian-Paket",
            "Description": "Browser",
            "Icon": f"{application_path}/images/apps/brave_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-brave-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_brave",
            "Uninstall": "pkexec apt remove brave-browser -y",
            "Path": "brave-browser",
        },
        "browser_2": {
            "Name": "",
            "Package": "",
            "Description": "",
            "Icon": f"{application_path}/images/apps/?_logo_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-?-thumb.png",
            "Install": "pkexec -y",
            "Uninstall": "pkexec pkexec -y",
            "Path": "",
        },
        "browser_3": {
            "Name": "",
            "Package": "",
            "Description": "",
            "Icon": f"{application_path}/images/apps/?_logo_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-?-thumb.png",
            "Install": "pkexec -y",
            "Uninstall": "pkexec pkexec -y",
            "Path": "",
        },
        "browser_4": {
            "Name": "",
            "Package": "",
            "Description": "",
            "Icon": f"{application_path}/images/apps/?_logo_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-?-thumb.png",
            "Install": "pkexec -y",
            "Uninstall": "pkexec pkexec -y",
            "Path": "",
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
