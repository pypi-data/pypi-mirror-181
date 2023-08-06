from lxml import objectify

from gdshoplib.apps.platforms.base import BasePlatform
from gdshoplib.apps.platforms.ula.settings import Settings
from gdshoplib.packages.feed import Feed


class UlaManager(BasePlatform, Feed):
    KEY = "ULA"
    SETTINGS = Settings

    def get_offer(self, product):
        offer = super(UlaManager, self).get_offer(product)
        offer.youlaCategoryId = self.settings.CATEGORY_ID
        offer.youlaSubcategoryId = self.settings.SUBCATEGORY_ID
        offer.tovary_vid_zhivotnogo = 10463
        objectify.deannotate(offer, cleanup_namespaces=True, xsi_nil=True)
        return offer
