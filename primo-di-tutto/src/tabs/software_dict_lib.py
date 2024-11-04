from resorcess import *

class SoftwareStore:
    # Descriptions by ????????????
    store_dict = {
        "store_0": {
            "Name": "Gnome Software",  # Name
            "Icon": f"{application_path}/images/apps/gnomesoftware_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Open": "gnome-software"        
        },
        "store_1": {
            "Name": "Synaptic",  # Name
            "Package": "Debian-Paket",  # Paketformat
            "Icon": f"{application_path}/images/apps/synaptic_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Open": "pkexec synaptic"
        },
    }

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
            "Uninstall": "flatpak remove org.zdoom.GZDoom -y",
            "Path": "GZDoom",
        },
        "game_6": {
            "Name": "OpenRA",
            "Package": "Flatpak",
            "Description": "OpenRA ist ein Projekt, das die klassischen Command-&-Conquer-Echtzeit-Strategiespiele neu erschafft und modernisiert.",
            "Icon": f"{application_path}/images/apps/openra_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-openra-thumb.png",
            "Install": "flatpak install flathub net.openra.OpenRA -y",
            "Uninstall": "flatpak remove net.openra.OpenRA -y",
            "Path": "net.openra.OpenRA",
        },

        "game_7": {
            "Name": "Xonotic",
            "Package": "Flatpak",
            "Description": "Xonotic ist ein kostenloser und rasantes First-Person-Shooter, der süchtig machendes Arena-Gameplay mit schneller Bewegung und einer großen Auswahl an Waffen kombiniert.",
            "Icon": f"{application_path}/images/apps/xonotic_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-xonotic-thumb.png",
            "Install": "flatpak install flathub org.xonotic.Xonotic -y",
            "Uninstall": "flatpak remove org.xonotic.Xonotic -y",
            "Path": "org.xonotic.Xonotic",
        },

        "game_8": {
            "Name": "Frogatto & Friends",
            "Package": "Flatpak",
            "Description": "Ein Old-School-2D-Plattformspiel mit einem gewissen eigenwilligen Frosch in der Hauptrolle. *Frogatto* bietet wunderschöne, hochwertige Pixelgrafik, mitreißende Arcade-Soundtracks und das ganze Spielgefühl eines klassischen Konsolentitels. Renne und springe über Abgründe und Gegner. Greife Feinde mit deiner Zunge, verschlucke sie und spucke sie dann als Projektile auf andere Gegner!",
            "Icon": f"{application_path}/images/apps/frogatto_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-frogatto-thumb.png",
            "Install": "flatpak install flathub com.frogatto.Frogatto -y",
            "Uninstall": "flatpak remove com.frogatto.Frogatto -y",
            "Path": "com.frogatto.Frogatto",
        },

        "game_9": {
            "Name": "Bombermaaan",
            "Package": "Flatpak",
            "Description": "Ein klassisches *Bomberman*-Spiel mit Mehrspielerunterstützung, inspiriert von den originalen SNES-Spielen.",
            "Icon": f"{application_path}/images/apps/bombermaaan_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-bombermaaan-thumb.png",
            "Install": "flatpak install flathub com.github.bjaraujo.Bombermaaan -y",
            "Uninstall": "flatpak remove com.github.bjaraujo.Bombermaaan -y",
            "Path": "com.github.bjaraujo.Bombermaaan",
        },

    }


class SoftwareBrowser:
    browser_dict = {
            "browser_0": {
                "Name": "Firefox",
                "Package": "Snap",
                "Description": "Firefox ist ein leistungsstarker und sicherer Webbrowser von Mozilla. Er bietet umfassenden Datenschutz und eine Vielzahl an Erweiterungen, um das Surferlebnis anzupassen. Er ist besonders beliebt für seine benutzerfreundliche Oberfläche und Sicherheit.",
                "Icon": f"{application_path}/images/apps/firefox_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-firefox-thumb.png",
                "Install": "pkexec snap install firefox",
                "Uninstall": "pkexec snap remove firefox",
                "Path": "firefox",
            },
            "browser_1": {
                "Name": "Brave",
                "Package": "Debian-Paket",
                "Description": "Brave ist ein schneller und datenschutzorientierter Browser, der standardmäßig Werbung und Tracker blockiert. Er bietet integrierte Funktionen wie Belohnungen für das Ansehen von Werbung und Tor-Browsing. Brave legt Wert auf Privatsphäre und Geschwindigkeit.",
                "Icon": f"{application_path}/images/apps/brave_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-brave-thumb.png",
                "Install": f"pkexec {application_path}/scripts/install_brave",
                "Uninstall": "pkexec apt remove brave-browser -y",
                "Path": "brave-browser",
            },
            "browser_2": {
                "Name": "Vivaldi",
                "Package": "Flatpak",
                "Description": "Vivaldi ist ein flexibler und anpassbarer Browser, der auf die Bedürfnisse von Power-Usern zugeschnitten ist. Er bietet eine Vielzahl von Funktionen wie Tab-Stapelung und Notizen direkt im Browser. Vivaldi basiert auf Chromium, legt jedoch großen Wert auf Individualisierung und Datenschutz.",
                "Icon": f"{application_path}/images/apps/vivaldi_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-vivaldi-thumb.png",
                "Install": "flatpak install flathub com.vivaldi.Vivaldi -y",
                "Uninstall": "flatpak uninstall com.vivaldi.Vivaldi",
                "Path": "com.vivaldi.Vivaldi",
            },
            "browser_3": {
                "Name": "LibreWolf",
                "Package": "Debian-Paket",
                "Description": "LibreWolf ist eine Datenschutz-orientierte Variante von Firefox ohne Telemetrie und anderen Datenverfolgungsfunktionen. Der Browser ist für Benutzer gedacht, die größtmögliche Kontrolle über ihre Daten und Sicherheit schätzen. LibreWolf setzt auf eine strenge Datenschutzpolitik.",
                "Icon": f"{application_path}/images/apps/librewolf_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-librewolf-thumb.png",
                "Install": f"pkexec {application_path}/scripts/install_librewolf",
                "Uninstall": f"pkexec {application_path}/scripts/uninstall_librewolf",
                "Path": "librewolf",
            },
            "browser_4": {
                "Name": "Chromium",
                "Package": "Snap",
                "Description": "Chromium ist der Open-Source-Browser, der als Grundlage für Google Chrome dient. Er bietet hohe Geschwindigkeit und eine benutzerfreundliche Oberfläche und unterstützt zahlreiche Erweiterungen. Chromium wird oft für Webentwicklung und Tests genutzt.",
                "Icon": f"{application_path}/images/apps/chromium_icon_36.png",
                "Thumbnail": f"{application_path}/images/apps/soft-chromium-thumb.png",
                "Install": "pkexec snap install chromium",
                "Uninstall": "pkexec snap remove chromium",
                "Path": "chromium",
            },
        }

class SoftwareCommunication:
    # Descriptions by ????????????
    com_dict = {
        # Browser
        "com_0": {
            "Name": "Brave Browser",
            "Package": "Debian-Paket",
            "Description": "Ein schneller, sicherheitsorientierter Browser, der Werbung blockiert und Tracker blockiert. Basiert auf Chromium und fokussiert auf Datenschutz. Unterstützt eine Vielzahl an Erweiterungen.",
            "Icon": f"{application_path}/images/apps/brave_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-brave-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_brave",
            "Uninstall": "pkexec apt remove brave-browser -y",
            "Path": "brave-browser",
        },
        "com_1": {
            "Name": "Firefox",
            "Package": "Snap",
            "Description": "Ein flexibler und datenschutzorientierter Browser von Mozilla. Unterstützt zahlreiche Add-ons und bietet eine hohe Anpassungsfähigkeit. Verfügbar auf allen gängigen Plattformen.",
            "Icon": f"{application_path}/images/apps/firefox_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-firefox-thumb.png",
            "Install": "pkexec snap install firefox",
            "Uninstall": "pkexec snap remove firefox",
            "Path": "firefox",
        },
        "com_2": {
            "Name": "Vivaldi",
            "Package": "Debian-Paket",
            "Description": "Ein anpassbarer Browser mit Fokus auf Produktivität und Privatsphäre. Enthält viele integrierte Werkzeuge wie Notizen und Screenshots. Basiert auf der Chromium-Engine.",
            "Icon": f"{application_path}/images/apps/vivaldi_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-vivaldi-thumb.png",
            "Install": "pkexec apt install vivaldi-stable -y",
            "Uninstall": "pkexec apt remove vivaldi-stable -y",
            "Path": "vivaldi-stable",
        },
        "com_3": {
            "Name": "LibreWolf",
            "Package": "AppImage",
            "Description": "Ein auf Firefox basierender Browser mit Fokus auf Datenschutz und Sicherheit. Entfernt Telemetrie und Werbe-Tracking. Unterstützt Firefox-Add-ons und regelmäßige Updates.",
            "Icon": f"{application_path}/images/apps/librewolf_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft_librewolf_thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_librewolf",
            "Uninstall": f"pkexec {application_path}/scripts/uninstall_librewolf",
            "Path": "librewolf",
        },
        "com_4": {
            "Name": "Chromium",
            "Package": "Snap",
            "Description": "Der Open-Source-Browser von Google, der die Basis für Google Chrome bildet. Enthält keine proprietären Google-Komponenten. Wird oft von Entwicklern für Tests genutzt.",
            "Icon": f"{application_path}/images/apps/chromium_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-chromium-thumb.png",
            "Install": "snap install chromium",
            "Uninstall": "snap remove chromium",
            "Path": "chromium",
        },
        "com_5": {
            "Name": "Google Chrome",
            "Package": "Flatpak",
            "Description": "Der populäre Browser von Google mit integrierten Google-Diensten. Bietet schnelle Performance und Unterstützung für eine Vielzahl an Erweiterungen. Weltweit am häufigsten genutzter Browser.",
            "Icon": f"{application_path}/images/apps/chrome_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-chrome-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_chrome",
            "Uninstall": "pkexec apt remove google-chrome-stable -y",
            "Path": "google-chrome",
        },
        # E-Mail und Messaging
        "com_6": {
            "Name": "Thunderbird",
            "Package": "Snap",
            "Description": "Ein leistungsfähiger E-Mail-Client von Mozilla mit Kalender- und Aufgabenfunktion. Unterstützt POP3 und IMAP sowie RSS-Feeds. Plattformübergreifend verfügbar.",
            "Icon": f"{application_path}/images/apps/thunderbird_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-thunderbird-thumb.png",
            "Install": "pkexec snap install thunderbird",
            "Uninstall": "pkexec snap remove thunderbird",
            "Path": "thunderbird",
        },
        "com_7": {
            "Name": "Geary",
            "Package": "Debian-Paket",
            "Description": "Ein einfacher und übersichtlicher E-Mail-Client für GNOME. Bietet Unterstützung für IMAP und POP3 und ist intuitiv zu bedienen. Geeignet für den täglichen E-Mail-Verkehr.",
            "Icon": f"{application_path}/images/apps/geary_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-geary-thumb.png",
            "Install": "pkexec apt install geary -y",
            "Uninstall": "pkexec apt remove geary -y",
            "Path": "geary",
        },
        "com_8": {
            "Name": "ZapZap",
            "Package": "Snap",
            "Description": "Eine populäre Messaging-App für Text-, Sprach- und Videoanrufe mit Ende-zu-Ende-Verschlüsselung. Ideal für mobile und Desktop-Kommunikation. Weltweit weit verbreitet.",
            "Icon": f"{application_path}/images/apps/zapzap_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-zapzap-thumb.png",
            "Install": "pkexec snap install whatsapp-for-linux",
            "Uninstall": "pkexec snap remove whatsapp-for-linux",
            "Path": "whatsapp-for-linux",
        },
        "com_9": {
            "Name": "Telegram",
            "Package": "Flatpak",
            "Description": "Ein schneller und sicherer Messenger mit Unterstützung für große Gruppen und Kanäle. Synchronisiert Nachrichten in der Cloud. Beliebt für seine Vielzahl an Funktionen.",
            "Icon": f"{application_path}/images/apps/telegram_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-telegram-thumb.png",
            "Install": "pkexec flatpak install telegram",
            "Uninstall": "pkexec flatpak remove telegram",
            "Path": "telegram",
        },
        "com_10": {
            "Name": "Signal",
            "Package": "Debian-Paket",
            "Description": "Ein Open-Source-Messenger mit starker Ende-zu-Ende-Verschlüsselung für Nachrichten und Anrufe. Fokus auf Datenschutz und Sicherheit. Verfügbar auf Mobilgeräten und Desktop.",
            "Icon": f"{application_path}/images/apps/signal_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-signal-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_signal",
            "Uninstall": "pkexec apt remove signal-desktop -y",
            "Path": "signal-desktop",
        },
        "com_11": {
            "Name": "Element",
            "Package": "Flatpak",
            "Description": "Matrix-basierte Messaging-App für sichere und dezentrale Kommunikation. Bietet Funktionen für Einzel- und Gruppenchats. Für verschiedene Plattformen verfügbar.",
            "Icon": f"{application_path}/images/apps/element_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-element-thumb.png",
            "Install": "pkexec flatpak install element",
            "Uninstall": "pkexec flatpak remove element",
            "Path": "element",
        },
        "com_12": {
            "Name": "Ferdium",
            "Package": "Debian-Paket",
            "Description": "Ein Mehrzweck-Messaging-Manager, der verschiedene Dienste wie WhatsApp, Telegram und Slack kombiniert. Besonders praktisch für Vielnutzer. Plattformübergreifend einsetzbar.",
            "Icon": f"{application_path}/images/apps/ferdium_icon_36.png",
            "Thumbnail": f"{application_path}/images/apps/soft-ferdium-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_ferdium",
            "Uninstall": f"pkexec {application_path}/scripts/uninstall_ferdium",
            "Path": "ferdium",
        },
    }
