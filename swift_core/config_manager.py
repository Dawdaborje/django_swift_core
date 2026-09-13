from swift_core import DJANGO_SWIFT_CONFIG_FILE


class ConfigManager:
    @classmethod
    def initialize():
        with open(DJANGO_SWIFT_CONFIG_FILE, "w"):
            pass
