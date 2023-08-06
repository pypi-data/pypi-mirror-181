from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.vk.settings import Settings


class VkManager(BasePlatform):
    KEY = "VK"
    SETTINGS = Settings
