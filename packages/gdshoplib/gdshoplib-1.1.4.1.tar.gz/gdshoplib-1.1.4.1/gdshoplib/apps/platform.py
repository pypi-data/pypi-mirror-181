from gdshoplib.apps.platforms import BasePlatform
from gdshoplib.apps.product import Product


class Platform:
    def __init__(self, key, *args, **kwargs):
        self.platform = BasePlatform.get_platform_class(key)(*args, **kwargs)

    def feed(self):
        return self.platform.get_feed(Product())
