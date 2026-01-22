# Primo-di-tutto Fehlerbehebung / Troubleshooting

## Problem: Primo startet nicht / keine Fehlermeldung

Das Programm wurde mit umfangreicher Fehlerbehandlung und Logging ausgestattet.

### 1. Primo über die Konsole starten

```bash
cd /pfad/zu/primo-di-tutto
./start.sh
```

Das Start-Script prüft jetzt automatisch:
- Ob GTK4 installiert ist
- Ob alle Dateien vorhanden sind
- Python-Version
- DPI-Einstellungen

### 2. Log-Datei überprüfen

Alle Fehler werden jetzt in einer Log-Datei gespeichert:

```bash
cat ~/.primo/primo.log
```

Die Log-Datei zeigt detailliert:
- Welche Module geladen werden
- Wo genau ein Fehler auftritt
- Komplette Fehlermeldungen mit Stack-Traces

### 3. Direkt mit Python starten (für maximales Debugging)

```bash
cd /pfad/zu/primo-di-tutto
python3 src/main_gtk.py
```

Dies zeigt ALLE Fehlermeldungen direkt in der Konsole.

### 4. Häufige Probleme und Lösungen

#### Problem: "GTK4 ist nicht installiert"

**Lösung:**
```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
```

#### Problem: "Module not found: resorcess" oder andere Tab-Module

**Lösung:** Stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden:
```bash
cd /pfad/zu/primo-di-tutto
pwd  # Sollte das primo-di-tutto Verzeichnis zeigen
```

#### Problem: "No module named 'gi'"

**Lösung:**
```bash
sudo apt install python3-gi python3-gi-cairo
```

### 5. System-Informationen für Bug-Reports

Wenn das Problem weiterhin besteht, sammeln Sie folgende Informationen:

```bash
# Python-Version
python3 --version

# GTK-Pakete prüfen
dpkg -l | grep -E 'gir1.2-gtk|python3-gi|gir1.2-adw'

# Log-Datei komplett ausgeben
cat ~/.primo/primo.log

# Primo direkt starten und Ausgabe speichern
cd /pfad/zu/primo-di-tutto
python3 src/main_gtk.py 2>&1 | tee ~/primo-debug.txt
```

Senden Sie dann die Datei `~/primo-debug.txt` und `~/.primo/primo.log` an den Entwickler.

### 6. Testlauf mit minimalem Setup

Um zu testen, ob GTK4 grundsätzlich funktioniert:

```bash
python3 -c "
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
print('GTK4 und Adwaita funktionieren!')
"
```

Wenn dies einen Fehler zeigt, ist das Problem bei der GTK4-Installation.

## Verbesserte Fehlerausgaben

Das Programm zeigt jetzt:
- ✓ Welche Module geladen werden
- ✓ Wo genau ein Fehler auftritt  
- ✓ Vollständige Fehlermeldungen
- ✓ Hilfreiche Hinweise zur Fehlerbehebung
- ✓ Log-Datei-Speicherort

**Wichtig:** Die Log-Datei `~/.primo/primo.log` enthält ALLE Details zum Start und allen Fehlern!
