from enum import Enum


class NotificationUrgency:
    LOW = "low"
    NORMAL = "normal"
    CRITICAL = "critical"


class AppPackage(Enum):
    SNAP = "snap"
    FLATPAK = "Flatpak"
    DEB = "Debian-Paket"
    AUR = "aur"
