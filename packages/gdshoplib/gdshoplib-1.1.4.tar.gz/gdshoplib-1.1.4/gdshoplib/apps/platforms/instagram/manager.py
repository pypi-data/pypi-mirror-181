from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.vk.settings import Settings


class InstagramManager(BasePlatform):
    DESCRIPTION_TEMPLATE = "instagram.txt"
    KEY = "INSTAGRAM"
    SETTINGS = Settings
