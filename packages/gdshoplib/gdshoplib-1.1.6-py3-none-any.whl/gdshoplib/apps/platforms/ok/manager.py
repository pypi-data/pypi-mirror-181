from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.ok.settings import Settings


class OkManager(BasePlatform):
    KEY = "OK"
    SETTINGS = Settings
