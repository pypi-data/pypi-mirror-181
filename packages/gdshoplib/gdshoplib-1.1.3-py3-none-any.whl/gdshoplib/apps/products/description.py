# Работа с описаниями товаров
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel

from gdshoplib.core.base.base_manager import BaseManager
from gdshoplib.core.settings import settings
from gdshoplib.services.notion.notion import Notion


class ProductDescription:
    def __init__(self, block):
        self.block = block
        self.notion = Notion()

        content = " ".join(
            [t.get("plain_text", "") for t in block["code"]["rich_text"]]
        )
        platform = self.notion.get_capture(block).split(":")
        platform = platform[-1].upper() if len(platform) > 1 else None
        self.data = ProductDescriptionModel(
            id=block["id"],
            platform=platform if platform else None,
            description=content,
        )

        self.jinja2_env = self.jinja2_env()

    def generate(self, product, platform):
        manager = BaseManager.get_manager(platform)(cache=True)
        return self.render(manager, product)

    def get(self, sku, platform):
        """Получить описание из Notion"""
        product = self.notion.get_product(sku)
        descriptions = product.get("descriptions", {})
        if not descriptions:
            return ""

        if platform in descriptions:
            return descriptions[platform]["description"]
        return descriptions[None]["description"]

    def update(self, sku, platform=None):
        # Обновить описание продукта
        product = self.notion.get_product(sku)

        if platform and product["descriptions"].get(platform):
            self.notion.update_block(
                product["descriptions"].get(platform)["id"],
                self.generate(product, platform),
            )

        for k, v in product["descriptions"].items():
            new_description = self.generate(product, k)
            self.notion.update_block(v["id"], new_description)

    def get_template(self, manager):
        return self.jinja2_env.get_template(manager.DESCRIPTION_TEMPLATE)

    def render(self, manager, params):
        return self.get_template(manager).render(product=params)

    @classmethod
    def jinja2_env(cls):
        return Environment(
            loader=FileSystemLoader(settings.TEMPLATES_PATH),
            autoescape=select_autoescape(),
        )


class ProductDescriptionModel(BaseModel):
    id: str
    platform: Optional[str]
    description: str
