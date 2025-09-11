from abc import ABC, abstractmethod
from constants import AppPackage
from flatpak_manage import refresh_flatpak_installs
from apt_manage import get_installed_apt_pkgs
from snap_manage import get_installed_snaps


class InstallableApp:
    def __init__(
        self,
        name,
        icon,
        description,
        path,
        thumbnail,
        install_command,
        uninstall_command,
    ):
        self.name = name
        self.icon = icon
        self.description = description
        self.path = path
        self.thumbnail = thumbnail
        self.install_command = install_command
        self.uninstall_command = uninstall_command

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_icon(self):
        return self.icon

    def get_path(self):
        return self.path

    def get_thumbnail(self):
        return self.thumbnail

    def get_type(self):
        raise NotImplementedError

    def is_installed(self):
        raise NotImplementedError

    def get_install_command(self):
        return self.install_command

    def get_uninstall_command(self):
        return self.uninstall_command


class InstallableAppFactory:
    registry = {}

    @classmethod
    def register(cls, type: str):
        def decorator(subclass):
            cls.registry[type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, type: AppPackage, **kwargs) -> InstallableApp:
        return cls.registry[type](**kwargs)


@InstallableAppFactory.register(AppPackage.FLATPAK)
class FlatpakApp(InstallableApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_type(self):
        return AppPackage.FLATPAK.value

    def is_installed(self):
        flatpak_installs = refresh_flatpak_installs()

        return self.get_path() in flatpak_installs.values()


@InstallableAppFactory.register(AppPackage.DEB)
class DebianApp(InstallableApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_type(self):
        return AppPackage.DEB.value

    def is_installed(self):
        return self.get_path() in get_installed_apt_pkgs()


@InstallableAppFactory.register(AppPackage.SNAP)
class SnapApp(InstallableApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_type(self):
        return AppPackage.SNAP.value

    def is_installed(self):
        return self.get_path() in get_installed_snaps()
