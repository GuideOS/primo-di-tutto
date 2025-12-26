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
Comment[de_DE]=GuideOS Einstellungen (Primo)
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

# Erstellen der Autostart .desktop-Datei
cat > debian/primo-di-tutto/usr/share/applications/plank-settings.desktop <<EOL
#!/usr/bin/env xdg-open
[Desktop Entry]
Name=GuideOS Plank-Manager
GenericName=Dock
Comment[am]=በጣም ቀላል
Comment[ar]=بسيط بغباء.
Comment[bg]=Пределно прост.
Comment[bs]=Glupavo jednostavan.
Comment[ca]=Estúpidament simple.
Comment[cs]=Stupidně jednoduchý.
Comment[da]=Super simpel.
Comment[de]=Hiermit kannst du das Plank-Dock einrichten.
Comment[el]=Βλακωδώς απλό.
Comment[en_AU]=Stupidly simple.
Comment[en_CA]=Stupidly simple.
Comment[en_GB]=Stupidly simple.
Comment[eo]=Stulte simple.
Comment[es]=Estúpidamente simple.
Comment[et]=Hämmastavalt lihtne.
Comment[eu]=Erraza baino errazagoa.
Comment[fi]=Todella yksinkertainen.
Comment[fr]=Stupidement simple.
Comment[ga]=Simplíocht shimplí.
Comment[gd]=Cho furasta 's a ghabhas.
Comment[gl]=Estupidamente simple.
Comment[he]=טפשי עד כמה שזה פשוט
Comment[hr]=Neviđeno jednostavan
Comment[hu]=Nagyszerűen egyszerű.
Comment[id]=Begitu sederhana.
Comment[it]=Stupidamente semplice.
Comment[ja]=超シンプル
Comment[ka]=ძალიან მარტივი აი ძალიან
Comment[ko]=어처구니없으리 만치 단순한.
Comment[lt]=Kvailai paprastas.
Comment[lv]=Muļķīgi vienkārši.
Comment[ml]=അനായാസം.
Comment[ms]=Ringkas la sangat.
Comment[nb]=Uforstandig enkelt.
Comment[ne]=एकदमै सरल
Comment[nl]=Belachelijk eenvoudig.
Comment[nn]=Idiotsikkert
Comment[pl]=Idiotycznie prosty.
Comment[pt]=Estupidamente simples.
Comment[pt_BR]=Estupidamente simples.
Comment[ro]=Stupid de simplu.
Comment[ru]=До безумного прост.
Comment[sk]=Primitívne jednoduchý.
Comment[sl]=Bedasto preprost.
Comment[sma]=dle dan aelhkies.
Comment[sr]=Шашаво једноставно.
Comment[sr@latin]=Glupavo jenostavan.
Comment[sv]=Galet enkelt.
Comment[ta]=மிகவும் எளிது
Comment[te]=చాలా సరళమైనది.
Comment[th]=ง่ายเหี้ยๆ
Comment[tr]=Son derece basit.
Comment[uk]=Просто легкий.
Comment[uz]=Ahmoqona darajada sodda.
Comment[vi]=Cực kì đơn giản.
Comment[zh_CN]=简单得无语。
Comment[zh_TW]=極簡。
Comment=Stupidly simple.
Categories=GuideOS;
Type=Application
Exec=plank  --preferences
Icon=guideos-plank-manager
Terminal=false
NoDisplay=false
EOL
