
def send_notification(title, message, icon_path=None, urgency="normal"):
    command = ["notify-send", title, message, "-u", urgency]
    if icon_path:
        command.extend(["-i", icon_path])
    subprocess.run(command)

# Beispielaufruf mit Icon und hoher Dringlichkeit
send_notification("Achtung!", "Wichtige Nachricht", icon_path="/usr/share/icons/hicolor/256x256/apps/primo-di-tutto-logo.png", urgency="critical")
