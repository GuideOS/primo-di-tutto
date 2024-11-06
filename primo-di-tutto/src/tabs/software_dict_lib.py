from resorcess import *
import requests
import os


class SoftwareStore:
    # Descriptions by ????????????
    store_dict = {
        "store_0": {
            "Name": "Gnome Software",  # Name
            "Icon": f"{application_path}/images/apps/gnomesoftware_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Open": "gnome-software",
        },
        "store_1": {
            "Name": "Synaptic",  # Name
            "Package": "Debian-Paket",  # Paketformat
            "Icon": f"{application_path}/images/apps/synaptic_icon_36.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Open": "pkexec synaptic",
        },
    }


class SoftwareOffice:
    # Descriptions by ????????????
    office_dict = {
        "office_0": {
            "Name": "LibreOffice",  # Name
            "Package": "Debian-Paket",  # Paketformat
            "Description": "Ein Office oder so",  # Beschreibung in 3 Sätzen
            "Icon": f"{application_path}/images/apps/org.libreoffice.LibreOffice-icon.png",  # Symbolpfad / 36x36 / PNG / offiziell o. Wikipedia
            "Thumbnail": f"{application_path}/images/apps/org.libreoffice.LibreOffice-thumb.png",  # Miniaturbild / Maximiert / Max. 742x389
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
            "Icon": f"{application_path}/images/apps/com.valvesoftware.Steam-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.valvesoftware.Steam-thumb.png",
            "Install": "pkexec apt install steam -y",
            "Uninstall": "pkexec apt remove steam -y",
            "Path": "steam",
            "AppStream": "com.valvesoftware.Steam",
        },
        "game_1": {
            "Name": "Lutris",
            "Package": "Debian-Paket",
            "Description": "Lutris ist ein Programm, mit dem man Spiele aus verschiedenen Quellen verwalten und starten kann. Das geht auch (teilweise) mit Windows-Games.",
            "Icon": f"{application_path}/images/apps/net.lutris.Lutris-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.lutris.Lutris-thumb.png",
            "Install": f"{application_path}/scripts/install_lutris",
            "Uninstall": "pkexec apt remove lutris",
            "Path": "lutris",
            "AppStream": "net.lutris.Lutris",
        },
        "game_2": {
            "Name": "Heroic",
            "Package": "Flatpak",
            "Description": "Der Heroic-Game-Launcher ist ein Programm zum Starten, Verwalten und Spielen von Epic- und GOG-Games.",
            "Icon": f"{application_path}/images/apps/com.heroicgameslauncher.hgl-icon.png",
            "Install": "flatpak install flathub com.heroicgameslauncher.hgl -y",
            "Thumbnail": f"{application_path}/images/apps/com.heroicgameslauncher.hgl-thumb.png",
            "Uninstall": "flatpak remove com.heroicgameslauncher.hgl -y",
            "Path": "com.heroicgameslauncher.hgl",
            "AppStream": "com.heroicgameslauncher.hgl",
        },
        "game_3": {
            "Name": "ProtonUp-Qt",
            "Package": "Flatpak",
            "Description": "ProtonUp-Qt ist ein Programm für Proton-Versionen und andere Kompatibilitätsschichten wie Wine-GE für Steam und Lutris.",
            "Icon": f"{application_path}/images/apps/net.davidotek.pupgui2-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.davidotek.pupgui2-thumb.png",
            "Install": "flatpak install flathub net.davidotek.pupgui2 -y",
            "Uninstall": "flatpak remove net.davidotek.pupgui2 -y",
            "Path": "net.davidotek.pupgui2",
            "AppStream": "net.davidotek.pupgui2",
        },
        "game_5": {
            "Name": "GZDoom",
            "Package": "Flatpak",
            "Description": "GZDoom ist ein moderner Source-Port, der aktuelle Hardware und Betriebssysteme unterstützt und eine Vielzahl an Einstellungsmöglichkeiten bietet. Neben Doom unterstützt GZDoom auch Heretic, Hexen, Strife, Chex Quest und von Fans erstellte Spiele wie Harmony und Hacx.",
            "Icon": f"{application_path}/images/apps/org.zdoom.GZDoom-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.zdoom.GZDoom-thumb.png",
            "Install": "flatpak install flathub org.zdoom.GZDoom -y",
            "Uninstall": "flatpak remove org.zdoom.GZDoom -y",
            "Path": "org.zdoom.GZDoom",
            "AppStream": "org.zdoom.GZDoom",
        },
        "game_6": {
            "Name": "OpenRA",
            "Package": "Flatpak",
            "Description": "OpenRA ist ein Projekt, das die klassischen Command-&-Conquer-Echtzeit-Strategiespiele neu erschafft und modernisiert.",
            "Icon": f"{application_path}/images/apps/net.openra.OpenRA-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.openra.OpenRA-thumb.png",
            "Install": "flatpak install flathub net.openra.OpenRA -y",
            "Uninstall": "flatpak remove net.openra.OpenRA -y",
            "Path": "net.openra.OpenRA",
            "AppStream": "net.openra.OpenRA",
        },
        "game_7": {
            "Name": "Xonotic",
            "Package": "Flatpak",
            "Description": "Xonotic ist ein kostenloser und rasantes First-Person-Shooter, der süchtig machendes Arena-Gameplay mit schneller Bewegung und einer großen Auswahl an Waffen kombiniert.",
            "Icon": f"{application_path}/images/apps/org.xonotic.Xonotic-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.xonotic.Xonotic-thumb.png",
            "Install": "flatpak install flathub org.xonotic.Xonotic -y",
            "Uninstall": "flatpak remove org.xonotic.Xonotic -y",
            "Path": "org.xonotic.Xonotic",
            "AppStream": "org.xonotic.Xonotic",
        },
        "game_8": {
            "Name": "Frogatto & Friends",
            "Package": "Flatpak",
            "Description": "Ein Old-School-2D-Plattformspiel mit einem gewissen eigenwilligen Frosch in der Hauptrolle. *Frogatto* bietet wunderschöne, hochwertige Pixelgrafik, mitreißende Arcade-Soundtracks und das ganze Spielgefühl eines klassischen Konsolentitels. Renne und springe über Abgründe und Gegner. Greife Feinde mit deiner Zunge, verschlucke sie und spucke sie dann als Projektile auf andere Gegner!",
            "Icon": f"{application_path}/images/apps/com.frogatto.Frogatto-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.frogatto.Frogatto-thumb.png",
            "Install": "flatpak install flathub com.frogatto.Frogatto -y",
            "Uninstall": "flatpak remove com.frogatto.Frogatto -y",
            "Path": "com.frogatto.Frogatto",
            "AppStream": "com.frogatto.Frogatto",
        },
        "game_9": {
            "Name": "Bombermaaan",
            "Package": "Flatpak",
            "Description": "Ein klassisches *Bomberman*-Spiel mit Mehrspielerunterstützung, inspiriert von den originalen SNES-Spielen.",
            "Icon": f"{application_path}/images/apps/com.github.bjaraujo.Bombermaaan-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.github.bjaraujo.Bombermaaan-thumb.png",
            "Install": "flatpak install flathub com.github.bjaraujo.Bombermaaan -y",
            "Uninstall": "flatpak remove com.github.bjaraujo.Bombermaaan -y",
            "Path": "com.github.bjaraujo.Bombermaaan",
            "AppStream": "com.github.bjaraujo.Bombermaaan",
        },
        "game_10": {
            "Name": "Space Cadet Pinball",
            "Package": "Flatpak",
            "Description": "Reverse Engineering von '3D Pinball for Windows – Space Cadet', einem mit Windows gebündelten Spiel.",
            "Icon": f"{application_path}/images/apps/com.github.k4zmu2a.spacecadetpinball-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.github.k4zmu2a.spacecadetpinball-thumb.png",
            "Install": "flatpak install flathub com.github.k4zmu2a.spacecadetpinball -y",
            "Uninstall": "flatpak remove com.github.bjaraujo.Bombermaaan -y",
            "Path": "com.github.k4zmu2a.spacecadetpinball",
            "AppStream": "com.github.k4zmu2a.spacecadetpinball",
        },
        "game_11": {
            "Name": "Total Chaos",
            "Package": "Flatpak",
            "Description": "Survival-Horror auf einer abgelegenen Insel namens Fort Oasis. Die Insel wurde einst von einer Gemeinschaft von Kohlearbeitern bewohnt, die eines Tages plötzlich verschwand und die verlassene Betonlandschaft zurückließ, um zu verfallen.Offensichtlich ist etwas furchtbar schiefgelaufen an diesem Ort. Bei deiner Ankunft in Fort Oasis empfängst du eine seltsame Funksendung. Jemand möchte gefunden werden. Überlebe in 6 Kapiteln, kämpfe gegen über 8 grausame Kreaturen und nutze dabei eine große Auswahl an Waffen.",
            "Icon": f"{application_path}/images/apps/com.moddb.TotalChaos-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.moddb.TotalChaos-thumb.png",
            "Install": "flatpak install flathub com.moddb.TotalChaos -y",
            "Uninstall": "flatpak remove com.moddb.TotalChaos -y",
            "Path": "com.moddb.TotalChaos",
            "AppStream": "com.moddb.TotalChaos",
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
            "Icon": f"{application_path}/images/apps/com.brave.Browser-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.brave.Browser-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_brave",
            "Uninstall": "pkexec apt remove brave-browser -y",
            "Path": "brave-browser",
        },
        "com_1": {
            "Name": "Firefox",
            "Package": "Snap",
            "Description": "Ein flexibler und datenschutzorientierter Browser von Mozilla. Unterstützt zahlreiche Add-ons und bietet eine hohe Anpassungsfähigkeit. Verfügbar auf allen gängigen Plattformen.",
            "Icon": f"{application_path}/images/apps/org.mozilla.firefox-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.mozilla.firefox-thumb.png",
            "Install": "pkexec snap install firefox",
            "Uninstall": "pkexec snap remove firefox",
            "Path": "firefox",
        },
        "com_2": {
            "Name": "Vivaldi",
            "Package": "Debian-Paket",
            "Description": "Ein anpassbarer Browser mit Fokus auf Produktivität und Privatsphäre. Enthält viele integrierte Werkzeuge wie Notizen und Screenshots. Basiert auf der Chromium-Engine.",
            "Icon": f"{application_path}/images/apps/com.vivaldi.Vivaldi-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.vivaldi.Vivaldi-thumb.png",
            "Install": "flatpak install flathub com.vivaldi.Vivaldi -y",
            "Uninstall": "flatpak remove com.vivaldi.Vivaldi -y",
            "Path": "com.vivaldi.Vivaldi",
        },
        "com_3": {
            "Name": "LibreWolf",
            "Package": "AppImage",
            "Description": "Ein auf Firefox basierender Browser mit Fokus auf Datenschutz und Sicherheit. Entfernt Telemetrie und Werbe-Tracking. Unterstützt Firefox-Add-ons und regelmäßige Updates.",
            "Icon": f"{application_path}/images/apps/io.gitlab.librewolf-community-icon.png",
            "Thumbnail": f"{application_path}/images/apps/io.gitlab.librewolf-community-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_librewolf",
            "Uninstall": f"pkexec {application_path}/scripts/uninstall_librewolf",
            "Path": "librewolf",
        },
        "com_4": {
            "Name": "Chromium",
            "Package": "Snap",
            "Description": "Der Open-Source-Browser von Google, der die Basis für Google Chrome bildet. Enthält keine proprietären Google-Komponenten. Wird oft von Entwicklern für Tests genutzt.",
            "Icon": f"{application_path}/images/apps/org.chromium.Chromium-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.chromium.Chromium-thumb.png",
            "Install": "snap install chromium",
            "Uninstall": "snap remove chromium",
            "Path": "chromium",
        },
        "com_5": {
            "Name": "Google Chrome",
            "Package": "Flatpak",
            "Description": "Der populäre Browser von Google mit integrierten Google-Diensten. Bietet schnelle Performance und Unterstützung für eine Vielzahl an Erweiterungen. Weltweit am häufigsten genutzter Browser.",
            "Icon": f"{application_path}/images/apps/com.google.Chrome-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.google.Chrome-thumb.png",
            "Install": "flatpak install flathub com.google.Chrome -y",
            "Uninstall": "flatpak remove com.google.Chrome -y",
            "Path": "com.google.Chrome",
        },
        # E-Mail und Messaging
        "com_6": {
            "Name": "Thunderbird",
            "Package": "Snap",
            "Description": "Ein leistungsfähiger E-Mail-Client von Mozilla mit Kalender- und Aufgabenfunktion. Unterstützt POP3 und IMAP sowie RSS-Feeds. Plattformübergreifend verfügbar.",
            "Icon": f"{application_path}/images/apps/org.mozilla.Thunderbird-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.mozilla.Thunderbird-thumb.png",
            "Install": "pkexec snap install thunderbird",
            "Uninstall": "pkexec snap remove thunderbird",
            "Path": "thunderbird",
        },
        "com_7": {
            "Name": "Geary",
            "Package": "Debian-Paket",
            "Description": "Ein einfacher und übersichtlicher E-Mail-Client für GNOME. Bietet Unterstützung für IMAP und POP3 und ist intuitiv zu bedienen. Geeignet für den täglichen E-Mail-Verkehr.",
            "Icon": f"{application_path}/images/apps/org.gnome.Geary-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gnome.Geary-thumb.png",
            "Install": "pkexec apt install geary -y",
            "Uninstall": "pkexec apt remove geary -y",
            "Path": "geary",
        },
        "com_8": {
            "Name": "ZapZap",
            "Package": "Snap",
            "Description": "Eine populäre Messaging-App für Text-, Sprach- und Videoanrufe mit Ende-zu-Ende-Verschlüsselung. Ideal für mobile und Desktop-Kommunikation. Weltweit weit verbreitet.",
            "Icon": f"{application_path}/images/apps/com.rtosta.zapzap-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.rtosta.zapzap-thumb.png",
            "Install": "flatpak install flathub com.rtosta.zapzap -y",
            "Uninstall": "flatpak remove com.rtosta.zapzap -y",
            "Path": "com.rtosta.zapzap",
        },
        "com_9": {
            "Name": "Telegram",
            "Package": "Flatpak",
            "Description": "Ein schneller und sicherer Messenger mit Unterstützung für große Gruppen und Kanäle. Synchronisiert Nachrichten in der Cloud. Beliebt für seine Vielzahl an Funktionen.",
            "Icon": f"{application_path}/images/apps/org.telegram.desktop-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.telegram.desktop-thumb.png",
            "Install": "flatpak install flathub org.telegram.desktop -y",
            "Uninstall": "flatpak remove org.telegram.desktop -y",
            "Path": "org.telegram.desktop",
        },
        "com_10": {
            "Name": "Signal",
            "Package": "Debian-Paket",
            "Description": "Ein Open-Source-Messenger mit starker Ende-zu-Ende-Verschlüsselung für Nachrichten und Anrufe. Fokus auf Datenschutz und Sicherheit. Verfügbar auf Mobilgeräten und Desktop.",
            "Icon": f"{application_path}/images/apps/org.signal.Signal-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.signal.Signal-thumb.png",
            "Install": "flatpak install flathub org.signal.Signal -y",
            "Uninstall": "flatpak remove org.signal.Signal -y",
            "Path": "org.signal.Signal",
        },
        "com_11": {
            "Name": "Element",
            "Package": "Flatpak",
            "Description": "Matrix-basierte Messaging-App für sichere und dezentrale Kommunikation. Bietet Funktionen für Einzel- und Gruppenchats. Für verschiedene Plattformen verfügbar.",
            "Icon": f"{application_path}/images/apps/im.riot.Riot-icon.png",
            "Thumbnail": f"{application_path}/images/apps/im.riot.Riot-thumb.png",
            "Install": "flatpak install flathub im.riot.Riot -y",
            "Uninstall": "flatpak remove im.riot.Riot -y",
            "Path": "im.riot.Riot",
        },
        "com_12": {
            "Name": "Ferdium",
            "Package": "Debian-Paket",
            "Description": "Ein Mehrzweck-Messaging-Manager, der verschiedene Dienste wie WhatsApp, Telegram und Slack kombiniert. Besonders praktisch für Vielnutzer. Plattformübergreifend einsetzbar.",
            "Icon": f"{application_path}/images/apps/org.ferdium.Ferdium-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.ferdium.Ferdium-thumb.png",
            "Install": "flatpak install flathub org.ferdium.Ferdium -y",
            "Uninstall": "flatpak remove org.ferdium.Ferdium -y",
            "Path": "org.ferdium.Ferdium",
        },
    }


class SoftwareAudioVideo:
    # Descriptions by AudioVideoDocumentationTeam
    av_dict = {
        # Audio/Video Editing Tools
        "av_0": {
            "Name": "Audacity",
            "Package": "Debian-Paket",
            "Description": "Ein freier, plattformübergreifender Audio-Editor und -Recorder. Unterstützt Mehrspuraufnahmen und bietet viele Bearbeitungsfunktionen, darunter Effekte und Filter.",
            "Icon": f"{application_path}/images/apps/org.audacityteam.Audacity-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.audacityteam.Audacity-thumb.png",
            "Install": "pkexec apt install audacity -y",
            "Uninstall": "pkexec apt remove audacity -y",
            "Path": "audacity",
        },
        "av_1": {
            "Name": "OBS Studio",
            "Package": "Debian-Paket",
            "Description": "Ein professionelles Open-Source-Tool für Videoaufnahmen und Live-Streaming. Unterstützt mehrere Quellen und Szenen, Echtzeit-Video-/Audio-Mischung und eine große Auswahl an Plugins.",
            "Icon": f"{application_path}/images/apps/com.obsproject.Studio-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.obsproject.Studio-thumb.png",
            "Install": "flatpak install flathub com.obsproject.Studio -y",
            "Uninstall": "flatpak remove com.obsproject.Studio -y",
            "Path": "obs",
        },
        "av_2": {
            "Name": "Kdenlive",
            "Package": "Debian-Paket",
            "Description": "Ein leistungsstarkes, nicht-lineares Open-Source-Videoschnittprogramm. Unterstützt mehrere Spuren, umfangreiche Effekte und Transitions für professionelle Videoerstellungen.",
            "Icon": f"{application_path}/images/apps/org.kde.kdenlive-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.kde.kdenlive-thumb.png",
            "Install": "pkexec apt install kdenlive -y",
            "Uninstall": "pkexec apt remove kdenlive -y",
            "Path": "kdenlive",
        },
        # Audio/Video Player Tools
        "av_3": {
            "Name": "VLC Media Player",
            "Package": "Snap",
            "Description": "Ein vielseitiger, plattformübergreifender Medienplayer, der eine Vielzahl an Audio- und Videoformaten unterstützt. Bietet Streaming-Optionen und eine hohe Anpassbarkeit.",
            "Icon": f"{application_path}/images/apps/org.videolan.VLC-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.videolan.VLC-thumb.png",
            "Install": "pkexec snap install vlc",
            "Uninstall": "pkexec snap remove vlc",
            "Path": "vlc",
        },
        "av_4": {
            "Name": "Rhythmbox",
            "Package": "Debian-Paket",
            "Description": "Ein einfacher und benutzerfreundlicher Musik-Player und -Manager für GNOME. Unterstützt eine Vielzahl von Audioformaten und bietet Funktionen wie Playlisten, Internetradio und Podcast-Verwaltung.",
            "Icon": f"{application_path}/images/apps/org.gnome.Rhythmbox3-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gnome.Rhythmbox3-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_rhythmbox",
            "Uninstall": "pkexec apt remove rhythmbox -y",
            "Path": "rhythmbox",
        },
        "av_5": {
            "Name": "MPV Player",
            "Package": "Flatpak",
            "Description": "Ein leichter und vielseitiger Video- und Musikplayer, der eine Vielzahl von Formaten unterstützt und fortschrittliche Videooptionen bietet. Anpassbar und effizient.",
            "Icon": f"{application_path}/images/apps/io.mpv.Mpv-icon.png",
            "Thumbnail": f"{application_path}/images/apps/io.mpv.Mpv-thumb.png",
            "Install": "flatpak install flathub io.mpv.Mpv -y",
            "Uninstall": "flatpak remove io.mpv.Mpv -y",
            "Path": "mpv",
        },
        "av_6": {
            "Name": "Clementine",
            "Package": "Debian-Paket",
            "Description": "Ein moderner Musikplayer und -manager, der auf Amarok basiert. Bietet Unterstützung für Playlisten, Online-Dienste wie Spotify und Soundcloud, sowie umfangreiche Bibliotheksverwaltung.",
            "Icon": f"{application_path}/images/apps/org.clementine-player.Clementine-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.clementine-player.Clementine-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_clementine",
            "Uninstall": "pkexec apt remove clementine -y",
            "Path": "clementine",
        },
    }


class SoftwareImageEditing:
    # Descriptions by ImageEditingDocumentationTeam
    img_dict = {
        # Image Editing Tools
        "img_0": {
            "Name": "GIMP",
            "Package": "Debian-Paket",
            "Description": "Ein freies und leistungsstarkes Bildbearbeitungsprogramm mit vielen Werkzeugen für Retusche, Montage und Bildkomposition. Unterstützt zahlreiche Plugins und Skripte.",
            "Icon": f"{application_path}/images/apps/org.gimp.GIMP-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gimp.GIMP-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_gimp",
            "Uninstall": "pkexec apt remove gimp -y",
            "Path": "gimp",
        },
        "img_1": {
            "Name": "Krita",
            "Package": "Flatpak",
            "Description": "Eine professionelle und kostenlose digitale Malsoftware, die sich besonders für Konzeptkunst, Texturen, Comics und Illustrationen eignet. Bietet eine intuitive Benutzeroberfläche und viele Malwerkzeuge.",
            "Icon": f"{application_path}/images/apps/org.kde.krita-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.kde.krita-thumb.png",
            "Install": "flatpak install flathub org.kde.krita -y",
            "Uninstall": "flatpak remove org.kde.krita -y",
            "Path": "krita",
        },
        "img_2": {
            "Name": "Inkscape",
            "Package": "Snap",
            "Description": "Ein Open-Source-Vektorzeichenprogramm, das sich besonders für Illustrationen, Diagramme und Logos eignet. Unterstützt das SVG-Format und bietet umfangreiche Zeichen- und Bearbeitungsfunktionen.",
            "Icon": f"{application_path}/images/apps/org.inkscape.Inkscape-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.inkscape.Inkscape-thumb.png",
            "Install": "pkexec snap install inkscape",
            "Uninstall": "pkexec snap remove inkscape",
            "Path": "inkscape",
        },
        "img_3": {
            "Name": "Darktable",
            "Package": "Debian-Paket",
            "Description": "Ein Open-Source-Fotolabor für die Bearbeitung und Verwaltung von RAW-Bildern. Bietet nicht-destruktive Bildbearbeitung und professionelle Farbverwaltung.",
            "Icon": f"{application_path}/images/apps/org.darktable.Darktable-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.darktable.Darktable-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_darktable",
            "Uninstall": "pkexec apt remove darktable -y",
            "Path": "darktable",
        },
        "img_4": {
            "Name": "RawTherapee",
            "Package": "Flatpak",
            "Description": "Ein RAW-Bildbearbeitungsprogramm mit einer Vielzahl an Farb- und Belichtungskorrektur-Optionen. Unterstützt verschiedene Kameras und bietet umfangreiche Filtermöglichkeiten.",
            "Icon": f"{application_path}/images/apps/com.rawtherapee.RawTherapee-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.rawtherapee.RawTherapee-thumb.png",
            "Install": "flatpak install flathub com.rawtherapee.RawTherapee -y",
            "Uninstall": "flatpak remove com.rawtherapee.RawTherapee -y",
            "Path": "rawtherapee",
        },
        "img_5": {
            "Name": "Pinta",
            "Package": "Snap",
            "Description": "Ein einfaches Bildbearbeitungsprogramm für grundlegende Bearbeitungen und Zeichnungen. Bietet grundlegende Bildbearbeitungswerkzeuge und ist besonders benutzerfreundlich.",
            "Icon": f"{application_path}/images/apps/com.pinta_project.Pinta-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.pinta_project.Pinta-thumb.png",
            "Install": "pkexec snap install pinta",
            "Uninstall": "pkexec snap remove pinta",
            "Path": "pinta",
        },
    }
