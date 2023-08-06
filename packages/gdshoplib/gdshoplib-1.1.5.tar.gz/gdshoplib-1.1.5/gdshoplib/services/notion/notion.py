# Менеджер управления Notion
from gdshoplib.services.notion.manager import Manager

from .users import User


class Notion(Manager):
    # TODO: Сделать декоратор для обработки запросов
    def get_user(self, user_id):
        data = self.make_request(f"users/{user_id}", method="get").json()
        if data.get("results"):
            data = data.get("results")[0]
        return User.parse_obj(
            {**data, "email": data.get("person", {}).get("email") or data.get("name")}
        )

    def get_capture(self, block):
        _capture = block[block["type"]].get("caption")
        return _capture[0].get("plain_text") if _capture else ""

    def get_blocks(self, parent_id):
        blocks = []
        for block in self.pagination(f"blocks/{parent_id}/children", method="get")[
            "results"
        ]:
            if not block.get("has_children"):
                blocks.append(block)
            else:
                blocks.extend(self.get_blocks(block.get("id")))
        return blocks

    def get_page(self, page_id):
        return self.make_request(f"pages/{page_id}", method="get")

    def get_pages(self, database_id):
        return self.pagination(
            f"databases/{database_id}/query", method="post", params=None
        )["results"]

    def update_sku(self, product_id, sku):
        # TODO: Переделать в обновление параметра
        _r = self.make_request(
            f"pages/{product_id}",
            method="patch",
            params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}},
        )
        return _r.ok

    def update_block(self, block_id, content):
        # TODO: Сделать объект для записи в блок
        _r = self.make_request(
            f"blocks/{block_id}",
            method="patch",
            params={"code": {"rich_text": [{"text": {"content": content}}]}},
        )
        return _r.ok
