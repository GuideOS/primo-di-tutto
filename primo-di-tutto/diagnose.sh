#!/bin/bash
# Diagnose-Script für Primo-di-tutto
# Dieses Script prüft alle Abhängigkeiten und zeigt detaillierte Informationen

echo "=========================================="
echo "PRIMO-DI-TUTTO DIAGNOSE"
echo "=========================================="
echo ""

# 1. System-Informationen
echo "1. System-Informationen:"
echo "   OS: $(uname -s)"
echo "   Kernel: $(uname -r)"
echo "   Distribution: $(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unbekannt')"
echo ""

# 2. Python prüfen
echo "2. Python-Installation:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✓ $PYTHON_VERSION"
    PYTHON_PATH=$(which python3)
    echo "   Pfad: $PYTHON_PATH"
else
    echo "   ✗ Python3 nicht gefunden!"
    echo "   Installieren Sie Python3: sudo apt install python3"
fi
echo ""

# 3. Python-Pakete prüfen
echo "3. Python-Pakete:"

check_python_module() {
    if python3 -c "import $1" 2>/dev/null; then
        echo "   ✓ $1"
        return 0
    else
        echo "   ✗ $1 FEHLT!"
        return 1
    fi
}

check_python_module "gi"
check_python_module "pathlib"

# Prüfe GTK4
echo ""
echo "4. GTK4-Bibliotheken:"
if python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "   ✓ GTK 4.0"
    GTK_VERSION=$(python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk; print(f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}')" 2>/dev/null)
    echo "   Version: $GTK_VERSION"
else
    echo "   ✗ GTK 4.0 FEHLT!"
    echo "   Installieren: sudo apt install gir1.2-gtk-4.0"
fi

# Prüfe Adwaita
if python3 -c "import gi; gi.require_version('Adw', '1'); from gi.repository import Adw" 2>/dev/null; then
    echo "   ✓ Adwaita 1.0"
else
    echo "   ✗ Adwaita 1.0 FEHLT!"
    echo "   Installieren: sudo apt install gir1.2-adw-1"
fi
echo ""

# 5. Systemweite Pakete prüfen
echo "5. Installierte Debian-Pakete:"
PACKAGES=("python3-gi" "python3-gi-cairo" "gir1.2-gtk-4.0" "gir1.2-adw-1")
for pkg in "${PACKAGES[@]}"; do
    if dpkg -l "$pkg" 2>/dev/null | grep -q "^ii"; then
        VERSION=$(dpkg -l "$pkg" | grep "^ii" | awk '{print $3}')
        echo "   ✓ $pkg ($VERSION)"
    else
        echo "   ✗ $pkg FEHLT!"
    fi
done
echo ""

# 6. Primo-Dateien prüfen
echo "6. Primo-di-tutto Dateien:"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "   Verzeichnis: $SCRIPT_DIR"

REQUIRED_FILES=(
    "src/main_gtk.py"
    "src/resorcess.py"
    "src/tabs/software_tab_gtk.py"
    "src/tabs/contrib_tab_gtk.py"
    "src/tabs/links_tab_gtk.py"
    "src/tabs/devices_tab_gtk.py"
    "src/tabs/system_tab_gtk.py"
    "src/tabs/large_folders_tab_gtk.py"
    "src/tabs/dash_tab_gtk.py"
    "src/tabs/welcome_tab_gtk.py"
    "src/tabs/expert_tools_gtk.py"
    "src/tabs/look_tab_gtk.py"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file FEHLT!"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done
echo ""

# 7. Log-Datei prüfen
echo "7. Log-Datei:"
LOG_FILE="$HOME/.primo/primo.log"
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(du -h "$LOG_FILE" | cut -f1)
    echo "   ✓ $LOG_FILE ($LOG_SIZE)"
    echo "   Letzte 10 Zeilen:"
    tail -n 10 "$LOG_FILE" | sed 's/^/      /'
else
    echo "   ℹ Noch keine Log-Datei vorhanden"
    echo "   (wird beim ersten Start erstellt)"
fi
echo ""

# Zusammenfassung
echo "=========================================="
echo "ZUSAMMENFASSUNG"
echo "=========================================="

ERRORS=0

if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 fehlt"
    ERRORS=$((ERRORS + 1))
fi

if ! python3 -c "import gi" 2>/dev/null; then
    echo "✗ python3-gi fehlt"
    ERRORS=$((ERRORS + 1))
fi

if ! python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "✗ GTK4 fehlt"
    ERRORS=$((ERRORS + 1))
fi

if ! python3 -c "import gi; gi.require_version('Adw', '1'); from gi.repository import Adw" 2>/dev/null; then
    echo "✗ Adwaita fehlt"
    ERRORS=$((ERRORS + 1))
fi

if [ $MISSING_FILES -gt 0 ]; then
    echo "✗ $MISSING_FILES Primo-Dateien fehlen"
    ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
    echo "✓ Alle Abhängigkeiten sind installiert!"
    echo ""
    echo "Sie können Primo jetzt starten mit:"
    echo "  ./start.sh"
    echo ""
    echo "Oder direkt mit Python:"
    echo "  python3 src/main_gtk.py"
else
    echo ""
    echo "✗ $ERRORS Problem(e) gefunden!"
    echo ""
    echo "Installieren Sie fehlende Pakete mit:"
    echo "  sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1"
fi

echo "=========================================="
