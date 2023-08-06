from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.tg.settings import Settings


class TgManager(BasePlatform):
    KEY = "TG"
    SETTINGS = Settings
