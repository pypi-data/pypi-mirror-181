from .avito.manager import AvitoManager
from .base import BasePlatform
from .instagram.manager import InstagramManager
from .ok.manager import OkManager
from .tg.manager import TgManager
from .ula.manager import UlaManager
from .vk.manager import VkManager
from .yandex_market.manager import YandexMarketManager

__all__ = (
    "AvitoManager",
    "InstagramManager",
    "OkManager",
    "TgManager",
    "UlaManager",
    "VkManager",
    "YandexMarketManager",
    "BasePlatform",
)
