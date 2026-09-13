import dataclasses
import pathlib

DJANGO_SETTINGS_PATH = pathlib.Path()

DJANGO_SWIFT_CONFIG_FILE = DJANGO_SETTINGS_PATH.parent / "swift.config.yml"


@dataclasses.dataclass
class Setting:
    key: str
    value: str | list | dict | bool | int | float

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
        }


class SettingGroup:
    key: str
    settings: list[Setting]

    def to_dict(self):
        return {
            "key": self.key,
            "settings": self.convert_settings_list_to_dict(),
        }

    def convert_settings_list_to_dict(self) -> list[dict]:
        settings = []

        for setting in self.settings:
            settings.append(setting.to_dict())

        return settings


DEFAULT_SETTINGS = [
    SettingGroup(
        key="core",
        settings=[],
    ),
]
