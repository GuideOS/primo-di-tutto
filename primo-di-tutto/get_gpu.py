import subprocess
import re

def get_graphics_card_info():
    try:
        inxi_output = subprocess.check_output(["inxi", "-G"], encoding="utf-8")

        for line in inxi_output.splitlines():
            if "Device-1:" in line:
                match = re.search(r'Device-1:\s*(.*?)(?=\s*driver:)', line)
                if match:
                    model = match.group(1).strip()
                    return model
        
        return "Keine Grafikkarte gefunden"
    
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Abrufen der Grafikkarten-Informationen: {e}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

print(get_graphics_card_info())

def get_graphics_driver_info():
    try:
        inxi_output = subprocess.check_output(["inxi", "-G"], encoding="utf-8")

        for line in inxi_output.splitlines():
            if "Device-1:" in line:
                match = re.search(r'driver:\s*(\S+)', line)
                if match:
                    driver = match.group(1).strip()
                    return driver
        
        return "Kein Treiber gefunden"
    
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Abrufen der Treiberinformationen: {e}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

print(get_graphics_driver_info())

def open_software_properties():
    try:
        subprocess.run(["/usr/bin/software-properties-gtk", "--open-tab=4"], check=True)
        return "Software-Einstellungen wurden geöffnet."
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Öffnen der Software-Einstellungen: {e}"
    except FileNotFoundError:
        return "Der Befehl wurde nicht gefunden. Ist 'software-properties-gtk' installiert?"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"


open_software_properties()