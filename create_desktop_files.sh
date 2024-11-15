#!/bin/bash

# Sicherstellen, dass die Verzeichnisse existieren
mkdir -p debian/primo-di-tutto/usr/share/applications
mkdir -p debian/primo-di-tutto/usr/share/applications/autostart

# Erstellen der ersten .desktop-Datei
cat > debian/primo-di-tutto/usr/share/applications/primo-di-tutto.desktop <<EOL
[Desktop Entry]
Version=2.1
Exec=primo-di-tutto
Name=Primo Di Tutto
GenericName=Primo
Encoding=UTF-8
Terminal=false
StartupWMClass=Primo
Type=Application
Categories=System
Icon=primo-di-tutto-logo
Path=/opt/primo-di-tutto/
EOL

# Erstellen der Autostart .desktop-Datei
cat > debian/primo-di-tutto/usr/share/applications/autostart/primo-di-tutto-autostart.desktop <<EOL
[Desktop Entry]
Version=2.1
Exec=primo-di-tutto
Name=Primo Di Tutto
GenericName=Primo
Encoding=UTF-8
Terminal=false
StartupWMClass=Primo
Type=Application
Categories=System
Icon=primo-di-tutto-logo
Path=/opt/primo-di-tutto/
X-GNOME-Autostart-enabled=true
EOL