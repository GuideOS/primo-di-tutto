#!/bin/bash

# Define the package name and version
PACKAGE_NAME="primo-di-tutto"
VERSION="0.4.7"

# Define the dependencies
DEPENDENCIES="python3-dev, python3-psutil, python3-distro, python3-bs4, python3-requests, python3-pil, python3-pil.imagetk, xterm, mpg123, lolcat, wmctrl, gdebi, mousepad, appstream, libnotify-bin, pkexec | policykit-1"

# Create the necessary directories
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/icons/hicolor/256x256/apps
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/icons/hicolor/scalable/apps
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/metainfo
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/doc/primo-di-tutto/

# Create Autostart directory (to be copied later)
mkdir -p ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/autostart/

# Copy necessary files
rsync -av --exclude='start.sh' --exclude='.vscode' --exclude='src/__pycache__' --exclude='src/tabs/__pycache__' ~/primo-di-tutto/primo-di-tutto/* ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto/

# Copy files to location
cp ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/icon/primo-di-tutto-logo.png ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png
cp ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/icon/primo-di-tutto-logo.svg ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/icons/hicolor/scalable/apps/primo-di-tutto-logo.svg
cp ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/io.github.actionschnitzel.primo-di-tutto.appdata.xml ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/metainfo/io.github.actionschnitzel.primo-di-tutto.appdata.xml
cp ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/LICENSE ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/doc/primo-di-tutto/LICENSE

# Create the copyright file
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/copyright << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: Primo Di Tutto
Source: https://github.com/actionschnitzel/primo-di-tutto

Files: *
Copyright: 2023 Timo Westphal
License: GPL-3
EOF

# Create the control file
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/control << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Architecture: all
Maintainer: Timo Westphal <pigroxtrmo@gmail.com>
Depends: $DEPENDENCIES
Section: misc
Priority: optional
Homepage: https://zestful-pigroxtrmo.wordpress.com/
License: GPL-3.0
Description: A system control tool for Raspberry Pi
 PiGro is a system configuration tool inspired by openSUSE's YaST
 but designed with the user-friendliness of Linux Mint in mind.
EOF

# Create the preinst file
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/preinst << 'EOF'
#!/bin/bash
# preinst script

# Save the path of the standard terminal in a temporary file
default_terminal=$(readlink -f /usr/bin/x-terminal-emulator)
echo "$default_terminal" > /tmp/default_terminal_path

EOF

# Create the postinst file and handle Autostart
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/postinst << 'EOF'
#!/bin/bash
# postinst script

# Read the saved path from the temporary file
default_terminal_path=$(cat /tmp/default_terminal_path)

# Check and restore the path
if [ ! -z "$default_terminal_path" ] && [ "$(readlink -f /usr/bin/x-terminal-emulator)" != "$default_terminal_path" ]; then
   # Restore the previous selection
   update-alternatives --set x-terminal-emulator "$default_terminal_path"
fi

# Clean up: Remove temporary file
rm -f /tmp/default_terminal_path

# Autostart section
USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
AUTOSTART_DIR="$USER_HOME/.config/autostart"
if [ ! -d "$AUTOSTART_DIR" ]; then
    mkdir -p "$AUTOSTART_DIR"
fi

# Copy Autostart file to the user's autostart directory
cp /usr/share/applications/autostart/primo-di-tutto-autostart.desktop "$AUTOSTART_DIR/"
chmod +x "$AUTOSTART_DIR/primo-di-tutto-autostart.desktop"

EOF

# Create the .desktop file for desktop shortcut
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/primo-di-tutto.desktop << EOL
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

# Create the .desktop file for desktop shortcut
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/gos-menu.desktop << EOL
[Desktop Entry]
Name=GOS Menu
GenericName=Application Launcher
Comment=Lightweight, look nice and powerful application launcher
Categories=GNOME;GTK;Utility;
Exec=com.github.libredeb.lightpad
Icon=guide-os-logo-symbolic-dark
Terminal=false
Type=Application
NoDisplay=true
StartupNotify=false
EOL


# Create the Autostart .desktop file
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/autostart/primo-di-tutto-autostart.desktop << EOL
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

# Set the necessary permissions
chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto/src/main.py
chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/preinst
chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/postinst

# Ensure executable scripts
find ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto/scripts/ -type f -iname "*.sh" -exec chmod +x {} \;

# Create the /bin/primo-di-tutto file
echo "#!/bin/bash" > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto
echo '/opt/primo-di-tutto/src/main.py "$@"' >>  ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto
chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto

# Build the package
cd ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/
chmod -R 755 debian
chmod 644 ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/primo-di-tutto.desktop
chmod 644 ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/gos-menu.desktop
chmod 644
sudo chown -R root:root debian

dpkg-deb --build -Zxz debian

# Move the package to the current directory
mv debian.deb ~/primo-di-tutto/$PACKAGE_NAME-$VERSION.deb

# Clean up the temporary files
sudo rm -rf debian

