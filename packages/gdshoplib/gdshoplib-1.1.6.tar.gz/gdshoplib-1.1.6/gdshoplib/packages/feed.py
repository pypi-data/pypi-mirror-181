from lxml import etree, objectify

from gdshoplib.core.settings import settings


class Feed:
    def __init__(self):
        self.root = self.get_root()

    def get_root(self):
        root = etree.Element("yml_catalog")
        objectify.deannotate(root, cleanup_namespaces=True, xsi_nil=True)
        # TODO: Получить по дате последнего измененного товара
        root.attrib["date"] = "2017-02-05 17:22"
        return root

    def get_shop(self):
        shop = objectify.Element("shop")

        shop.name = settings.SHOP_NAME
        shop.company = settings.COMPANY_NAME
        shop.url = settings.SHOP_URL
        currencies = objectify.Element("currencies")
        currency = etree.Element("currency")
        currency.attrib["id"] = "RUB"
        currency.attrib["rate"] = "1"
        objectify.deannotate(currency, cleanup_namespaces=True, xsi_nil=True)
        objectify.deannotate(currencies, cleanup_namespaces=True, xsi_nil=True)
        currencies.append(currency)
        shop.currencies = currencies
        objectify.deannotate(shop, cleanup_namespaces=True, xsi_nil=True)

        return shop

    def get_offers(self, products):
        offers = etree.Element("offers")
        objectify.deannotate(offers, cleanup_namespaces=True, xsi_nil=True)
        for product in products:
            offers.append(self.get_offer(product))

        return offers

    def get_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.address = settings.ADDRESS
        appt.price = int(round(product.price.now, 0))
        appt.phone = settings.PHONE
        appt.name = product.name
        appt.description = product.description
        appt.managerName = settings.MANAGER_NAME
        for image in product.images:
            appt.addattr("picture", image.data.url)

        objectify.deannotate(appt, cleanup_namespaces=True, xsi_nil=True)
        return appt

    def get_feed(self, products):
        self.root.append(self.get_shop())
        self.root.append(self.get_offers(products))
        return etree.tostring(
            self.root, pretty_print=True, encoding="utf-8", xml_declaration=True
        )
