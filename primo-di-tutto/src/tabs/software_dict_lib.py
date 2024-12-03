from resorcess import *
import requests
import os


class SoftwareStore:
    store_dict = {
        "store_0": {
            "Name": "Gnome Software",
            "Icon": f"{application_path}/images/apps/gnomesoftware_icon_36.png",
            "Open": "gnome-software",
        },
        "store_1": {
            "Name": "Synaptic",
            "Package": "Debian-Paket",
            "Icon": f"{application_path}/images/apps/synaptic_icon_36.png",
            "Open": "synaptic-pkexec",
        },
    }

class FlatpakStore:
    flatpak_store_dict = {
        "store_0": {
            "Name": "Gnome Software",
            "Icon": f"{application_path}/images/apps/gnomesoftware_icon_36.png",
            "Open": "gnome-software",
        },
        "store_1": {
            "Name": "Synaptic",
            "Package": "Debian-Paket",
            "Icon": f"{application_path}/images/apps/synaptic_icon_36.png",
            "Open": "pkexec synaptic",
        },
    }


class SoftwareOffice:
    office_dict = {
        "office_0": {
            "Name": "LibreOffice",
            "Package": "Debian-Paket",
            "Description": "LibreOffice ist eine leistungsstarke, freie und quelloffene Office-Suite, die Textverarbeitung, Tabellenkalkulation, Präsentationen, Diagramme und mehr unterstützt. Es ist mit Microsoft Office-Dateien kompatibel und bietet eine Vielzahl von Funktionen für professionelle und persönliche Nutzung. Die benutzerfreundliche Oberfläche und hohe Anpassbarkeit machen es zu einer beliebten Wahl für viele Anwender.",
            "Icon": f"{application_path}/images/apps/org.libreoffice.LibreOffice-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.libreoffice.LibreOffice-thumb.png",
            "Install": "pkexec apt install -y libreoffice libreoffice-help-de libreoffice-l10n-de",
            "Uninstall": "pkexec apt autoremove --purge libreoffice* -y",
            "Path": "libreoffice-core",
        },
        "office_1": {
            "Name": "AbiWord",
            "Package": "Debian-Paket",
            "Description": "AbiWord ist ein leichtgewichtiges Textverarbeitungsprogramm, das grundlegende Funktionen für die Erstellung und Bearbeitung von Dokumenten bietet. Es ist für einfache Textverarbeitungsaufgaben ideal und unterstützt eine Vielzahl von Dateiformaten, einschließlich Microsoft Word. Die kompakte Größe und Effizienz machen es zu einer guten Wahl für ältere oder ressourcenschwache Systeme.",
            "Icon": f"{application_path}/images/apps/com.abisource.AbiWord-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.abisource.AbiWord-thumb.png",
            "Install": "pkexec apt install -y abiword",
            "Uninstall": "pkexec apt remove abiword -y",
            "Path": "abiword",
        },
        "office_2": {
            "Name": "Beaver Notes",
            "Package": "Flatpak",
            "Description": "Beaver Notes ist eine Notiz-App, die einfache und übersichtliche Notizfunktionen für den Alltag bietet. Sie ermöglicht das Erstellen, Organisieren und Suchen von Notizen auf eine intuitive Weise. Die App ist minimalistisch gestaltet und richtet sich an Nutzer, die eine fokussierte Umgebung für das Festhalten von Gedanken und Aufgaben wünschen.",
            "Icon": f"{application_path}/images/apps/com.beavernotes.beavernotes-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.beavernotes.beavernotes-thumb.png",
            "Install": "flatpak install flathub com.beavernotes.beavernotes -y",
            "Uninstall": "flatpak remove com.beavernotes.beavernotes -y",
            "Path": "com.beavernotes.beavernotes",
        },
        "office_3": {
            "Name": "Xournal++",
            "Package": "Flatpak",
            "Description": "Xournal++ ist ein digitales Notizbuch und ein Zeichenwerkzeug, das ideal für handschriftliche Notizen und Anmerkungen ist. Die Anwendung unterstützt Stifteingaben und bietet verschiedene Zeichenwerkzeuge, um ein papierähnliches Schreibgefühl zu simulieren. Perfekt für Notizen in Vorlesungen, Meetings oder zum Kommentieren von PDF-Dokumenten.",
            "Icon": f"{application_path}/images/apps/com.github.xournalpp.xournalpp-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.github.xournalpp.xournalpp-thumb.png",
            "Install": "flatpak install flathub com.github.xournalpp.xournalpp -y",
            "Uninstall": "flatpak remove com.github.xournalpp.xournalpp -y",
            "Path": "com.github.xournalpp.xournalpp",
        },
        "office_4": {
            "Name": "Apostrophe",
            "Package": "Flatpak",
            "Description": "Apostrophe ist ein minimalistischer Markdown-Editor, der speziell für fokussiertes Schreiben entwickelt wurde. Die App bietet eine ablenkungsfreie Oberfläche und unterstützt Markdown-Syntax für formatiertes Schreiben. Ideal für Autoren, die einfache und elegante Werkzeuge für Texte ohne viel Ablenkung bevorzugen.",
            "Icon": f"{application_path}/images/apps/org.gnome.gitlab.somas.Apostrophe-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gnome.gitlab.somas.Apostrophe-thumb.png",
            "Install": "flatpak install flathub org.gnome.gitlab.somas.Apostrophe -y",
            "Uninstall": "flatpak remove org.gnome.gitlab.somas.Apostrophe -y",
            "Path": "org.gnome.gitlab.somas.Apostrophe",
        },
        "office_5": {
            "Name": "Paperwork",
            "Package": "Flatpak",
            "Description": "Paperwork ist ein digitales Dokumentenmanagement-Tool, das Ihnen hilft, gescannte Dokumente und Notizen zu organisieren. Die Anwendung bietet eine integrierte Texterkennung und eine Suchfunktion, die das schnelle Auffinden von Dokumenten erleichtert. Ideal für Nutzer, die papierlose Ablagen und digitales Archivieren bevorzugen.",
            "Icon": f"{application_path}/images/apps/work.openpaper.Paperwork-icon.png",
            "Thumbnail": f"{application_path}/images/apps/work.openpaper.Paperwork-thumb.png",
            "Install": "flatpak install flathub work.openpaper.Paperwork -y",
            "Uninstall": "flatpak remove work.openpaper.Paperwork -y",
            "Path": "work.openpaper.Paperwork",
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
            "Install": f"{application_path}/scripts/install_steam",
            "Uninstall": "pkexec apt remove steam-launcher -y",
            "Path": "steam-launcher",
            "AppStream": "com.valvesoftware.Steam",
        },
        "game_1": {
            "Name": "Lutris",
            "Package": "Debian-Paket",
            "Description": "Lutris ist ein Programm, mit dem man Spiele aus verschiedenen Quellen verwalten und starten kann. Das geht auch (teilweise) mit Windows-Games.\n\nDieser Installer installiert auch Wine, damit alles bereit zum spielen ist.",
            "Icon": f"{application_path}/images/apps/net.lutris.Lutris-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.lutris.Lutris-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_lutris",
            "Uninstall": "pkexec apt remove lutris -y",
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
        "game_12": {
            "Name": "Warzone 2100",
            "Package": "Flatpak",
            "Description": "Das klassische 3D-Echtzeit-Strategiespiel von 1999 wurde aktualisiert, aufgerüstet und für die neuesten Plattformen modernisiert! Befehlige die Streitkräfte des Projekts in einem Kampf, die Welt wiederaufzubauen, nachdem die Menschheit fast durch Atomraketen ausgelöscht wurde. Warzone 2100 bietet eine storybasierte Einzelspieler-Kampagne, Online-Multiplayer sowie Einzelspieler-Gefecht-Modi. Ein umfangreicher Technologiebaum mit über 400 verschiedenen Technologien, kombiniert mit einem Einheitendesign-System, ermöglicht eine große Vielfalt an möglichen Einheiten und Taktiken.",
            "Icon": f"{application_path}/images/apps/net.wz2100.wz2100-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.wz2100.wz2100-thumb.png",
            "Install": "flatpak install flathub net.wz2100.wz2100 -y",
            "Uninstall": "flatpak remove net.wz2100.wz2100 -y",
            "Path": "net.wz2100.wz2100",
            "AppStream": "net.wz2100.wz2100",
        },
        "game_13": {
            "Name": "Alien Arena",
            "Package": "Flatpak",
            "Description": "Stehst du auf Old-School-Deathmatch mit modernen Features? Wie wäre es mit einer lebendigen, farbenfrohen Arcade-Atmosphäre? Oder vielleicht...Retro-Sci-Fi? Dann wirst du lieben, was Alien Arena für dich bereithält! Dieses Spiel vereint einige der besten Aspekte von Spielen wie Quake und Unreal und verpackt sie in ein Retro-Alien-Thema, während es eine Menge origineller Ideen hinzufügt, die das Spiel einzigartig machen.",
            "Icon": f"{application_path}/images/apps/org.alienarena.alienarena-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.alienarena.alienarena-thumb.png",
            "Install": "flatpak install flathub org.alienarena.alienarena -y",
            "Uninstall": "flatpak remove org.alienarena.alienarena -y",
            "Path": "org.alienarena.alienarena",
            "AppStream": "org.alienarena.alienarena",
        },
        "game_13": {
            "Name": "AstroMenace",
            "Package": "Flatpak",
            "Description": "AstroMenace ist ein beeindruckender, knallharter Scroll-Shooter, in dem mutige Weltraumkrieger die perfekte Gelegenheit finden, ihre Kampffähigkeiten zu verbessern. Sammle während der Schlacht Geld, um dein Raumschiff in eine ultimative Massenvernichtungswaffe zu verwandeln und Horden von Feinden das Fürchten zu lehren. Genieße die wunderbar gestalteten 3D-Grafiken und hochqualitativen Spezialeffekte sowie die detaillierte Schwierigkeitsanpassung und das benutzerfreundliche Interface von AstroMenace.",
            "Icon": f"{application_path}/images/apps/com.viewizard.AstroMenace-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.viewizard.AstroMenace-thumb.png",
            "Install": "flatpak install flathub com.viewizard.AstroMenace -y",
            "Uninstall": "flatpak remove com.viewizard.AstroMenace -y",
            "Path": "com.viewizard.AstroMenace",
            "AppStream": "com.viewizard.AstroMenace",
        },
        "game_14": {
            "Name": "FreeRCT",
            "Package": "Flatpak",
            "Description": "FreeRCT hat das Ziel, ein freies und quelloffenes Spiel zu sein, das das Aussehen, das Gefühl und das Gameplay der beliebten Spiele RollerCoaster Tycoon 1 und 2 einfängt. Das Spiel befindet sich noch in einem frühen Alpha-Zustand, ist aber bereits spielbar und bietet eine Vielzahl an Features.",
            "Icon": f"{application_path}/images/apps/net.freerct.FreeRCT-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.freerct.FreeRCT-thumb.png",
            "Install": "flatpak install flathub net.freerct.FreeRCT -y",
            "Uninstall": "flatpak remove net.freerct.FreeRCT -y",
            "Path": "net.freerct.FreeRCT",
            "AppStream": "net.freerct.FreeRCT",
        },
        "game_15": {
            "Name": "Stone Kingdom",
            "Package": "Flatpak",
            "Description": "Erlebe den Nervenkitzel des mittelalterlichen Burgenbaus und der Zerstörung in unserem isometrischen, quelloffenen Strategiespiel – eine moderne Neuauflage des Klassikers 'Stronghold' von Firefly Studios. Tauche ein in eine Welt voller Strategie und taktischer Entscheidungen, während du deine eigenen Burgen im mittelalterlichen Europa entwirfst und verteidigst.",
            "Icon": f"{application_path}/images/apps/io.gitlab.stone_kingdoms.StoneKingdoms-icon.png",
            "Thumbnail": f"{application_path}/images/apps/io.gitlab.stone_kingdoms.StoneKingdoms-thumb.png",
            "Install": "flatpak install flathub io.gitlab.stone_kingdoms.StoneKingdoms -y",
            "Uninstall": "flatpak remove io.gitlab.stone_kingdoms.StoneKingdoms -y",
            "Path": "io.gitlab.stone_kingdoms.StoneKingdoms",
            "AppStream": "io.gitlab.stone_kingdoms.StoneKingdoms",
        },
        "game_16": {
            "Name": "Pekka Kana 2",
            "Package": "Flatpak",
            "Description": "Pekka Kana 2 (Pekka the Rooster 2) ist ein Jump-'n'-Run-Spiel, das im Geiste klassischer Plattformspiele wie Super Mario, Sonic the Hedgehog, Jazz Jackrabbit, Super Frog und ähnlicher Titel entwickelt wurde.\n\nDas einfache Ziel in jedem Level besteht darin, das Ausgangsschild zu erreichen – was jedoch meist nicht so einfach ist, wie es klingt, da Gegner, Fallen und knifflige Rätsel den Weg erschweren.",
            "Icon": f"{application_path}/images/apps/net.pistegamez.PekkaKana2-icon.png",
            "Thumbnail": f"{application_path}/images/apps/net.pistegamez.PekkaKana2-thumb.png",
            "Install": "flatpak install flathub net.pistegamez.PekkaKana2 -y",
            "Uninstall": "flatpak remove net.pistegamez.PekkaKana2 -y",
            "Path": "net.pistegamez.PekkaKana2",
            "AppStream": "net.pistegamez.PekkaKana2",
        },
    }


class SoftwareCommunication:
    com_dict = {
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
            "Package": "Debian-Paket",
            "Description": "Ein flexibler und datenschutzorientierter Browser von Mozilla. Unterstützt zahlreiche Add-ons und bietet eine hohe Anpassungsfähigkeit. Verfügbar auf allen gängigen Plattformen.",
            "Icon": f"{application_path}/images/apps/org.mozilla.firefox-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.mozilla.firefox-thumb.png",
            "Install": "pkexec apt install firefox -y",
            "Uninstall": "pkexec apt remove firefox -y",
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
            "Package": "Debian-Paket",
            "Description": "Ein auf Firefox basierender Browser mit Fokus auf Datenschutz und Sicherheit. Entfernt Telemetrie und Werbe-Tracking. Unterstützt Firefox-Add-ons und regelmäßige Updates.",
            "Icon": f"{application_path}/images/apps/io.gitlab.librewolf-community-icon.png",
            "Thumbnail": f"{application_path}/images/apps/io.gitlab.librewolf-community-thumb.png",
            "Install": f"pkexec {application_path}/scripts/install_librewolf",
            "Uninstall": f"pkexec {application_path}/scripts/uninstall_librewolf",
            "Path": "librewolf",
        },
        "com_4": {
            "Name": "Chromium",
            "Package": "Debian-Paket",
            "Description": "Der Open-Source-Browser von Google, der die Basis für Google Chrome bildet. Enthält keine proprietären Google-Komponenten. Wird oft von Entwicklern für Tests genutzt.",
            "Icon": f"{application_path}/images/apps/org.chromium.Chromium-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.chromium.Chromium-thumb.png",
            "Install": "pkexec apt install chromium -y",
            "Uninstall": "pkexec apt remove chromium -y",
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
        "com_6": {
            "Name": "Thunderbird",
            "Package": "Debian-Paket",
            "Description": "Ein leistungsfähiger E-Mail-Client von Mozilla mit Kalender- und Aufgabenfunktion. Unterstützt POP3 und IMAP sowie RSS-Feeds. Plattformübergreifend verfügbar.",
            "Icon": f"{application_path}/images/apps/org.mozilla.Thunderbird-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.mozilla.Thunderbird-thumb.png",
            "Install": "pkexec apt install thunderbird -y",
            "Uninstall": "pkexec apt remove thunderbird -y",
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
    av_dict = {
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
            "Install": "pkexec apt install obs-studio -y",
            "Uninstall": "pkexec apt remove obs-studio -y",
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
        "av_3": {
            "Name": "VLC Media Player",
            "Package": "Debian-Paket",
            "Description": "Ein vielseitiger, plattformübergreifender Medienplayer, der eine Vielzahl an Audio- und Videoformaten unterstützt. Bietet Streaming-Optionen und eine hohe Anpassbarkeit.",
            "Icon": f"{application_path}/images/apps/org.videolan.VLC-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.videolan.VLC-thumb.png",
            "Install": "pkexec apt install vlc  -y",
            "Uninstall": "pkexec apt remove vlc -y ",
            "Path": "vlc",
        },
        "av_4": {
            "Name": "Rhythmbox",
            "Package": "Debian-Paket",
            "Description": "Ein einfacher und benutzerfreundlicher Musik-Player und -Manager für GNOME. Unterstützt eine Vielzahl von Audioformaten und bietet Funktionen wie Playlisten, Internetradio und Podcast-Verwaltung.",
            "Icon": f"{application_path}/images/apps/org.gnome.Rhythmbox3-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gnome.Rhythmbox3-thumb.png",
            "Install": f"pkexec apt install rhythmbox -y",
            "Uninstall": "pkexec apt remove rhythmbox -y",
            "Path": "rhythmbox",
        },
        "av_5": {
            "Name": "Strawberry",
            "Package": "Debian-Paket",
            "Description": "Ein leichter und vielseitiger Video- und Musikplayer, der eine Vielzahl von Formaten unterstützt und fortschrittliche Videooptionen bietet. Anpassbar und effizient.",
            "Icon": f"{application_path}/images/apps/org.strawberrymusicplayer.strawberry-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.strawberrymusicplayer.strawberry-thumb.png",
            "Install": "pkexec apt install strawberry -y",
            "Uninstall": "pkexec apt remove strawberry -y",
            "Path": "strawberry",
        },
        "av_6": {
            "Name": "Clementine",
            "Package": "Debian-Paket",
            "Description": "Ein moderner Musikplayer und -manager, der auf Amarok basiert. Bietet Unterstützung für Playlisten, Online-Dienste wie Spotify und Soundcloud, sowie umfangreiche Bibliotheksverwaltung.",
            "Icon": f"{application_path}/images/apps/org.clementine_player.Clementine-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.clementine_player.Clementine-thumb.png",
            "Install": "pkexec apt install clementine -y",
            "Uninstall": "pkexec apt remove clementine -y",
            "Path": "clementine",
        },
        "av_7": {
            "Name": "Amarok",
            "Package": "Flatpak",
            "Description": "Ein moderner Musikplayer und -manager, der auf Amarok basiert. Bietet Unterstützung für Playlisten, Online-Dienste wie Spotify und Soundcloud, sowie umfangreiche Bibliotheksverwaltung.",
            "Icon": f"{application_path}/images/apps/org.kde.amarok-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.kde.amarok-thumb.png",
            "Install": "flatpak install flathub org.kde.amarok -y",
            "Uninstall": "flatpak remove org.kde.amarok -y",
            "Path": "org.kde.amarok",
        },
        "av_8": {
            "Name": "Cosy",
            "Package": "Flatpak",
            "Description": "Cosy ist ein moderner Hörbuch-Player, der speziell für Hörbücher entwickelt wurde. Die App bietet Funktionen wie Lesezeichen, Fortschrittsverfolgung und Sleep-Timer, um das Hörerlebnis zu verbessern. Ideal für Benutzer, die eine einfache und effektive Möglichkeit suchen, Hörbücher zu genießen.",
            "Icon": f"{application_path}/images/apps/com.github.geigi.cozy-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.github.geigi.cozy-thumb.png",
            "Install": "flatpak install flathub com.github.geigi.cozy -y",
            "Uninstall": "flatpak remove com.github.geigi.cozy -y",
            "Path": "com.github.geigi.cozy",
        },
        "av_9": {
            "Name": "Shortwave",
            "Package": "Flatpak",
            "Description": "Shortwave ist ein Internet-Radio-Player, der den Zugriff auf tausende Radiosender weltweit ermöglicht. Die Anwendung bietet Favoritenlisten, eine Verlaufshistorie und eine einfache Suche, um gewünschte Sender schnell zu finden. Shortwave ist ideal für Radio-Enthusiasten, die eine elegante Möglichkeit suchen, Internet-Radio zu genießen.",
            "Icon": f"{application_path}/images/apps/de.haeckerfelix.Shortwave-icon.png",
            "Thumbnail": f"{application_path}/images/apps/de.haeckerfelix.Shortwave-thumb.png",
            "Install": "flatpak install flathub de.haeckerfelix.Shortwave -y",
            "Uninstall": "flatpak remove de.haeckerfelix.Shortwave -y",
            "Path": "de.haeckerfelix.Shortwave",
        },
        "av_10": {
            "Name": "FreeTube",
            "Package": "Flatpak",
            "Description": "FreeTube ist ein YouTube-Client, der auf Datenschutz fokussiert ist. Die App ermöglicht das Ansehen und Abonnieren von YouTube-Inhalten ohne Werbeanzeigen und Tracking durch Google. Ideal für Nutzer, die ihre Privatsphäre beim Streaming schützen möchten.",
            "Icon": f"{application_path}/images/apps/io.freetubeapp.FreeTube-icon.png",
            "Thumbnail": f"{application_path}/images/apps/io.freetubeapp.FreeTube-thumb.png",
            "Install": "flatpak install flathub io.freetubeapp.FreeTube -y",
            "Uninstall": "flatpak remove io.freetubeapp.FreeTube -y",
            "Path": "io.freetubeapp.FreeTube",
        },
    }


class SoftwareImageEditing:
    img_dict = {
        "img_0": {
            "Name": "GIMP",
            "Package": "Debian-Paket",
            "Description": "Ein freies und leistungsstarkes Bildbearbeitungsprogramm mit vielen Werkzeugen für Retusche, Montage und Bildkomposition. Unterstützt zahlreiche Plugins und Skripte.",
            "Icon": f"{application_path}/images/apps/org.gimp.GIMP-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.gimp.GIMP-thumb.png",
            "Install": "pkexec apt install gimp -y",
            "Uninstall": "pkexec apt remove gimp -y",
            "Path": "gimp",
        },
        "img_1": {
            "Name": "Krita",
            "Package": "Debian-Paket",
            "Description": "Eine professionelle und kostenlose digitale Malsoftware, die sich besonders für Konzeptkunst, Texturen, Comics und Illustrationen eignet. Bietet eine intuitive Benutzeroberfläche und viele Malwerkzeuge.",
            "Icon": f"{application_path}/images/apps/org.kde.krita-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.kde.krita-thumb.png",
            "Install": "pkexec apt install krita krita-l10n -y",
            "Uninstall": "pkexec apt remove krita krita-l10n -y",
            "Path": "krita",
        },
        "img_2": {
            "Name": "Inkscape",
            "Package": "Debian-Paket",
            "Description": "Ein Open-Source-Vektorzeichenprogramm, das sich besonders für Illustrationen, Diagramme und Logos eignet. Unterstützt das SVG-Format und bietet umfangreiche Zeichen- und Bearbeitungsfunktionen.",
            "Icon": f"{application_path}/images/apps/org.inkscape.Inkscape-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.inkscape.Inkscape-thumb.png",
            "Install": "pkexec apt install inkscape -y",
            "Uninstall": "pkexec apt remove inkscape -y",
            "Path": "inkscape",
        },
        "img_3": {
            "Name": "Darktable",
            "Package": "Debian-Paket",
            "Description": "Ein Open-Source-Fotolabor für die Bearbeitung und Verwaltung von RAW-Bildern. Bietet nicht-destruktive Bildbearbeitung und professionelle Farbverwaltung.",
            "Icon": f"{application_path}/images/apps/org.darktable.Darktable-icon.png",
            "Thumbnail": f"{application_path}/images/apps/org.darktable.Darktable-thumb.png",
            "Install": "pkexec apt install darktable -y",
            "Uninstall": "pkexec apt remove darktable -y",
            "Path": "darktable",
        },
        "img_4": {
            "Name": "Pinta",
            "Package": "Flatpak",
            "Description": "Ein einfaches Bildbearbeitungsprogramm für grundlegende Bearbeitungen und Zeichnungen. Bietet grundlegende Bildbearbeitungswerkzeuge und ist besonders benutzerfreundlich.",
            "Icon": f"{application_path}/images/apps/com.github.PintaProject.Pinta-icon.png",
            "Thumbnail": f"{application_path}/images/apps/com.github.PintaProject.Pinta-thumb.png",
            "Install": "flatpak install flathub com.github.PintaProject.Pinta -y",
            "Uninstall": "flatpak remove com.github.PintaProject.Pinta -y",
            "Path": "com.github.PintaProject.Pinta",
        },
    }
