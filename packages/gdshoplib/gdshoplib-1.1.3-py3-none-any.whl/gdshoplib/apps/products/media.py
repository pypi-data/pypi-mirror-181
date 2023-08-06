import re
from enum import Enum
from typing import Optional

import requests
from pydantic import BaseModel

from gdshoplib.packages.files.disk import Disk
from gdshoplib.services.notion.notion import Notion


class ProductMedia:
    def __init__(self, block):
        self.notion = Notion()
        url = block[block["type"]]["file"]["url"]
        self.data = ProductMediaModel(
            key=self.notion.get_capture(block) or f"{block['type']}_general",
            type=block["type"],
            url=url,
            block_id=block["id"],
        )

        self.data.name = ProductMediaModel.parse_name(self.data.url)
        self.data.format = ProductMediaModel.parse_format(self.data.url)

    def product_update(self, sku):
        product = self.notion_manager.get_product(sku, format="model")
        self.save(product)

    def save(self, product):
        """Сохранить фотки продукта"""
        for media in product.media:
            content = media.get_content()
            self.disk.save(content, **self.disk.get_media_path(product, media))
            # self.notion_manager.set_comment(
            #     parent={"type": "page_id", "page_id": media.block_id},
            #     discussion_id=media.discussion_id,
            #     rich_text={"text": {"content": media.url, "link": {"type": "url", "url": media.url}}}
            # )
            # converter = BaseConverter.get_converter(media.type)(original)

            # converter.convert() if converter.need_convert else original
            # converter.mark() if converter.need_mark else original


class MediaEnum(str, Enum):
    video = "video"
    image = "image"


class ProductMediaModel(BaseModel):
    block_id: str
    discussion_id: Optional[str]
    key: str
    name: Optional[str]
    type: MediaEnum
    url: str
    format: Optional[str]
    content: Optional[bytes]
    md5: Optional[str]

    @staticmethod
    def parse_format(url):
        pattern = re.compile(r"\/.*\.(\w+)(\?|$)")
        r = re.findall(pattern, url)
        return r[0][0] if r else None

    @staticmethod
    def parse_name(url):
        # Не знаю как сделать красивее
        pattern1 = re.compile(r".*\/(?P<name>.*)")
        r = re.findall(pattern1, url)
        if not r or not r[0]:
            return None
        return r[0].split("?")[0]

    def get_content(self):
        if self.content is None:
            response = requests.get(self.url)
            self.content = response.content
            self.md5 = Disk.get_md5(self.content)
        return self.content
