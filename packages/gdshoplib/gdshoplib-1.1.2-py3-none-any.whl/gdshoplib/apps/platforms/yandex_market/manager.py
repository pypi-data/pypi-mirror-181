from gdshoplib.apps.platforms.base import BasePlatform

from .settings import Settings


class YandexMarketManager(BasePlatform):
    KEY = "YM"
    SETTINGS = Settings
