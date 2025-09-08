#!/bin/bash

# Sicherstellen, dass die Verzeichnisse existieren
mkdir -p debian/primo-di-tutto/usr/share/applications
mkdir -p debian/primo-di-tutto/etc/xdg/autostart

# Erstellen der ersten .desktop-Datei
cat > debian/primo-di-tutto/usr/share/applications/primo-di-tutto.desktop <<EOL
[Desktop Entry]
Version=2.1
Exec=primo-di-tutto
Name=GuideOS Einstellungen (Primo)
GenericName=GuideOS-Einstellungen
Encoding=UTF-8
Terminal=false
StartupWMClass=Primo
Type=Application
Categories=GuideOS;
Icon=primo-di-tutto-logo
Path=/opt/primo-di-tutto/
EOL

# Erstellen der ersten .desktop-Datei
cat > debian/primo-di-tutto/usr/share/applications/gos-menu.desktop <<EOL
[Desktop Entry]
Name=gos-menu
GenericName=Application Launcher
Comment=Lightweight, look nice and powerful application launcher
Categories=GuideOS;
Exec=io.github.libredeb.lightpad
Icon=guide-os-logo-symbolic-dark
Terminal=false
Type=Application
NoDisplay=false
StartupNotify=false
EOL


# Erstellen der Autostart .desktop-Datei
cat > debian/primo-di-tutto/etc/xdg/autostart/primo-di-tutto.desktop <<EOL
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Exec=python3 /opt/primo-di-tutto/src/main.py
X-GNOME-Autostart-enabled=true
NoDisplay=false
Hidden=false
Name[de_DE]=primo-di-tutto.desktop
Comment[de_DE]=Keine Beschreibung
X-GNOME-Autostart-Delay=0
EOL


# Erstellen der Autostart .desktop-Datei
cat > debian/primo-di-tutto/etc/xdg/autostart/plank.desktop <<EOL
[Desktop Entry]
Name=Plank
GenericName=Dock
Categories=Utility;
Type=Application
Exec=plank
Icon=plank
Terminal=false
NoDisplay=false
X-GNOME-Autostart-enabled=false
Hidden=false
Name[de_DE]=Plank
Comment[de_DE]=Lächerlich einfach.
X-GNOME-Autostart-Delay=0
EOL