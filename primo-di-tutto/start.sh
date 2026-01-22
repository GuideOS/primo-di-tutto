
#!/bin/bash
set -e  # Beende bei Fehlern

echo "=========================================="
echo "PRIMO-DI-TUTTO STARTET"
echo "=========================================="

# Automatische DPI-Erkennung unter X11
XFT_DPI=$(xrdb -query 2>/dev/null | awk '/Xft.dpi/ {print $2}')
if [ -n "$XFT_DPI" ]; then
	# Standard-DPI von Tkinter ist 72
	SCALE=$(echo "$XFT_DPI/72" | bc -l)
	# GDK_SCALE bleibt meist 1, GDK_DPI_SCALE wird gesetzt
	export GDK_SCALE=1
	export GDK_DPI_SCALE=$SCALE
	echo "DPI-Skalierung: $SCALE (XFT_DPI: $XFT_DPI)"
else
	# Fallback: Standardwerte
	export GDK_SCALE=1
	export GDK_DPI_SCALE=1
	echo "Verwende Standard-DPI"
fi

# Wechsle ins Script-Verzeichnis
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "Arbeitsverzeichnis: $(pwd)"

# Prüfe ob main_gtk.py existiert
if [ ! -f "src/main_gtk.py" ]; then
    echo "FEHLER: src/main_gtk.py nicht gefunden!"
    echo "Bitte stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden."
    exit 1
fi

# Prüfe Python-Version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python-Version: $PYTHON_VERSION"

# Prüfe ob GTK4 installiert ist
if ! python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo ""
    echo "=========================================="
    echo "FEHLER: GTK4 ist nicht installiert!"
    echo "=========================================="
    echo "Bitte installieren Sie folgende Pakete:"
    echo "  sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1"
    echo "=========================================="
    exit 1
fi

echo "GTK4 gefunden"
echo ""
echo "Starte Anwendung..."
echo "Log-Datei: ~/.primo/primo.log"
echo ""

# Starte die GTK4-Version
LOG_LEVEL=INFO python3 src/main_gtk.py

EXIT_CODE=$?
echo ""
echo "Anwendung beendet mit Exit-Code: $EXIT_CODE"

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "=========================================="
    echo "Die Anwendung wurde mit einem Fehler beendet!"
    echo "Weitere Details finden Sie in: ~/.primo/primo.log"
    echo "=========================================="
fi

exit $EXIT_CODE


