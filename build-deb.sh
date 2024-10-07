#!/bin/bash



# Define the package name and version
PACKAGE_NAME="primo-di-tutto"
VERSION="0.1"

# Define the dependencies
DEPENDENCIES="python3-dev, python3-psutil, python3-distro, python3-bs4, python3-requests, python3-pil, python3-pil.imagetk, xterm, mpg123, lolcat, wmctrl, gdebi, mousepad, appstream, pkexec | policykit-1"

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

#Copy necessary files
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
 This package is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3.
 .
 This package is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>
 .
 On Debian systems, the complete text of the GNU General
 Public License version 3 can be found in "/usr/share/common-licenses/GPL-3".
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
 It equips Raspberry Pi OS with graphical interfaces for tasks 
 that would otherwise require the terminal.
 PiGro is also optimized for Ubuntu, Ubuntu Mate, and MX Linux.
EOF

# Create the preinst file
cat > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/preinst << 'EOF'
#!/bin/bash

# preinst script

# Save the path of the standard terminal in a temporary file
default_terminal=$(readlink -f /usr/bin/x-terminal-emulator)
echo "$default_terminal" > /tmp/default_terminal_path

# Perform further tasks here before the installation
EOF

# Create the postinst file
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

EOF

# Create the .desktop file
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

chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto/src/main.py

chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/DEBIAN/preinst

find ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/opt/primo-di-tutto/scripts/ -type f -iname "*.sh" -exec chmod +x {} \;

# Create the /bin/primo-di-tutto file
echo "#!/bin/bash" > ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto
echo '/opt/primo-di-tutto/src/main.py "$@"' >>  ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto
chmod +x ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/bin/primo-di-tutto


# Build the package
cd ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/
chmod -R 755 debian
chmod 644 ~/primo-di-tutto/PRIMO-DEBIAN-BUILD-BOX/debian/usr/share/applications/primo-di-tutto.desktop
sudo chown -R root:root debian

dpkg-deb --build -Zxz debian


# Move the package to the current directory
mv debian.deb ~/primo-di-tutto/$PACKAGE_NAME-$VERSION.deb

# Clean up the temporary files
sudo rm -rf debian
