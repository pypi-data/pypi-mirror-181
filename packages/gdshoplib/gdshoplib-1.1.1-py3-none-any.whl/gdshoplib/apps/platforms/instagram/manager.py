from gdshoplib.apps.platforms.vk.settings import Settings
from gdshoplib.core.base.base_platform import BasePlatform


class InstagramManager(BasePlatform):
    DESCRIPTION_TEMPLATE = "instagram.txt"
    KEY = "INSTAGRAM"
    SETTINGS = Settings
