class ProductProperties:
    def __init__(self, page):
        self.page = page

    def __getitem__(self, key):
        return self.__dict__.get(key) or self.__search_content(key)

    def __search_content(self, key):
        for _, prop in self.page["properties"].items():
            if prop["id"] == self.__get_prop_id(key):
                return properties_type_parse_map.get(
                    prop["type"], lambda data: str(data)
                )(prop)
        return ""

    def __get_prop_id(self, key):
        return properties_keys_map[key]["id"]


def list_addon(data):
    if not data:
        return []

    elements = [i.strip().lower() for i in data.split("/")]
    return [element for element in elements if element]


properties_keys_map = {
    "title": dict(name="Name", id="title"),
    "edited_by": dict(name="Last edited by", id="~%7BrF"),
    "price_sale_10": dict(name="Скидка, 10%", id="%7Bh%7D%7B"),
    "price_general": dict(name="Ходовая", id="x%3A%5Ci"),
    "created_time": dict(name="Created time", id="v%5Dsj"),
    "description": dict(name="Короткое описание", id="u_tU"),
    "size": dict(name="Размер", id="taW%3B"),
    "notes": dict(name="Примечания", id="sXND"),
    "price_buy": dict(name="Закупочная", id="pyiW"),
    "quantity": dict(name="Кол-во", id="pXTy"),
    "price_neutral": dict(name="Себестоимость", id="opcQ"),
    "edited_time": dict(name="Last edited time", id="mVEw"),
    "shipments": dict(name="🚚 Закупки", id="fzgM"),
    "sport": dict(name="Вид спорта", id="ePC%5C"),
    "price_sale_20": dict(name="Скидка, 20%", id="cPu~"),
    "brand": dict(name="Бренд", id="%5DZ%3Az"),
    "collection": dict(name="Коллекция", id="W%5BhI"),
    "price_base": dict(name="Безубыточность", id="VmWm"),
    "name": dict(name="Название на русском", id="Tss%5D"),
    "created_by": dict(name="Created by", id="TbyK"),
    "kit": dict(name="Комплект", id="QV%5D%5D"),
    "category": dict(name="Категория товара", id="NEgM"),
    "tags": dict(name="Теги", id="MqdC"),
    "status_description": dict(name="Описание", id="MUl%7C"),
    "color": dict(name="Цвет", id="Jvku"),
    "price_now": dict(name="Текущая цена", id="Ddaz"),
    "specifications": dict(name="Материалы / Характеристики", id="COmf"),
    "status_publication": dict(name="Публикация", id="BeEA"),
    "sku": dict(name="Наш SKU", id="BKOs"),
    "price_sale_15": dict(name="Скидка, 15%", id="BJPc"),
    "sku_s": dict(name="SKU поставщика", id="BHve"),
    "price_eur": dict(name="Цена (eur)", id="AyqD"),
    "platforms": dict(name="Платформы", id="%40Q~A"),
}

properties_type_parse_map = {
    "rich_text": lambda data: " ".join(
        [t.get("plain_text", "") for t in data["rich_text"]]
    )
    or "",
    "number": lambda data: data["number"] or 0,
    "select": lambda data: data.get("select").get("name")
    if data.get("select")
    else None,
    "multi_select": lambda data: data,
    "status": lambda data: data["status"]["name"],
    "date": lambda data: data,
    "formula": lambda data: data["formula"]["number"],
    "relation": lambda data: str(data["relation"]),
    "rollup": lambda data: data,
    "title": lambda data: str(data["title"]),
    "people": lambda data: data,
    "files": lambda data: data,
    "checkbox": lambda data: data,
    "url": lambda data: data["url"],
    "email": lambda data: data,
    "phone_number": lambda data: data,
    "created_time": lambda data: data["created_time"],
    "created_by": lambda data: str(data["created_by"]),
    "last_edited_time": lambda data: data["last_edited_time"],
    "last_edited_by": lambda data: str(data["last_edited_by"]),
    "image": lambda data: data["image"]["file"]["url"],
    "video": lambda data: data["video"]["file"]["url"],
}
