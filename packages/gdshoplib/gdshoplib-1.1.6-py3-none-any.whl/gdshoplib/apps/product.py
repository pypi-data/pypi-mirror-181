from typing import Any

from gdshoplib.apps.products.control import ProductControl
from gdshoplib.apps.products.description import ProductDescription
from gdshoplib.apps.products.media import ProductMedia
from gdshoplib.apps.products.price import ProductPrice
from gdshoplib.apps.products.property import ProductProperties
from gdshoplib.apps.products.settings import ProductSettings
from gdshoplib.apps.products.status import ProductStatus
from gdshoplib.services.notion.notion import Notion


class Product:
    """Класс работы с продуктами"""

    SETTINGS = None

    def __init__(self, *args, page=None, **kwargs):
        if not self.SETTINGS:
            self.SETTINGS = ProductSettings()

        self.__page = page
        self.__blocks = []
        self.__properties = None

        self.notion = Notion()
        self.history = {}
        self.filter = kwargs
        self._change_log = {}

        self._platforms = []
        self._status = None
        self._images = []
        self._videos = []
        self._price = None
        self._descriptions = []
        self._settings = None

        self._fetched = False

    def __getattr__(self, name: str) -> Any:
        if name not in ("__dict__", "__page"):
            key = f"_{name}"
            if not self._fetched:
                assert self.__page, "Продукт не проинициализирован страницей"
                self._fetch()

            if key in self.__dict__.keys():
                return self.__dict__.get(key)

            if key in self.__page.keys():
                return self.__page[key]

            return self.__properties[name]

        return super().__getattribute__(name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, __value)

    def __iter__(self):
        self._product_iterator = iter(self.notion.get_pages(self.SETTINGS.PRODUCT_DB))
        return self

    def __next__(self):
        return self.__class__(page=next(self._product_iterator))

    def __fetch_media(self, block):
        if block["type"] in ("video", "image"):
            self.__dict__[f"_{block['type']}s"].append(ProductMedia(block))

    def __fetch_control(self, block):
        if (
            block["type"] == "code"
            and self.notion.get_capture(block) == "base_settings"
        ):
            self._settings = ProductControl(block)

    def __fetch_description(self, block):
        if block["type"] == "code" and "description" in self.notion.get_capture(block):
            self._descriptions.append(ProductDescription(block))

    def __fetch_price(self):
        self._price = ProductPrice(self)

    def __fetch_status(self):
        self._status = ProductStatus(self.__page)

    def __fetch_properties(self):
        self.__properties = ProductProperties(self.__page)

    def _fetch(self):
        # Сценарий выгрузки содержмиого страницы товара
        # - Разобрать параметры и вставить значения
        # - Собрать блоки товара
        for block in self.notion.get_blocks(self.__page["id"]):
            self.__fetch_media(block)
            self.__fetch_control(block)
            self.__fetch_description(block)
            self.__blocks.append(block)
        self.__fetch_status()
        self.__fetch_price()
        self.__fetch_properties()

        self._fetched = True

    def commit(self):
        # Проитерироваться по изменениям и выполнить в Notion
        ...
