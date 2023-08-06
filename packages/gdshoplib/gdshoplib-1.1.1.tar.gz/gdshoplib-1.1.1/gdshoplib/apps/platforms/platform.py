from gdshoplib.services.notion.notion import Notion


class Platform:
    def __init__(self, page):
        self.notion = Notion()
        self.page = page

    def get_platform(self, key):
        ...

    def feed(self):
        """Получение фида"""
