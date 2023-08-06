from pydantic import BaseSettings


class ProductSettings(BaseSettings):
    PRODUCT_DB: str = "2d1707fb-877d-4d83-8ae6-3c3d00ff5091"


class PriceSettins(BaseSettings):
    PRICE_VAT_RATIO: float = 0.16
    PRICE_NEITRAL_RATIO: float = 0.40
    PRICE_PROFIT_RATIO: float = 0.60
    EURO_PRICE: int = 65


price_settings = PriceSettins()
