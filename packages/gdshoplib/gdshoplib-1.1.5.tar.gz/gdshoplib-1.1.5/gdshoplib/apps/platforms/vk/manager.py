from lxml import etree, objectify

from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.vk.settings import Settings
from gdshoplib.core.settings import settings


class VkManager(BasePlatform):
    KEY = "VK"
    SETTINGS = Settings

    @property
    def base_xml(self):
        root = etree.Element("yml_catalog")
        root.attrib["date"] = "2017-02-05 17:22"
        root.append(objectify.Element("shop"))
        root.append(objectify.Element("offers"))
        return root

    def feed(self, products):
        root = self.base_xml
        for product in products:
            root.append(self.create_offer(product))
        return etree.tostring(root, pretty_print=True, xml_declaration=True)

    def create_offer(self, product):
        appt = objectify.Element("offer")
        appt.attrib["id"] = product.sku
        appt.youlaCategoryId = self.settings.CATEGORY_ID
        appt.youlaSubcategoryId = self.settings.SUBCATEGORY_ID
        appt.tovary_vid_zhivotnogo = 10463
        appt.address = "Москва ул Крупской 4к1"
        appt.price = product.price_now
        appt.phone = settings.PHONE
        appt.name = product.name
        appt.description = product.description
        appt.managerName = "Менеджер магазина"
        for image in product.images:
            appt.addattr("picture", image.data.url)

        return appt
