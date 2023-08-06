import os
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class Settings(BaseSettings):
    TEMPLATES_PATH: DirectoryPath = (BASEPATH / "templates").resolve()
    PHONE: str = "+7 499 384 44 03"
    ADDRESS: str = "Москва ул Крупской 4к1"
    MANAGER_NAME: str = "Менеджер магазина"
    SHOP_NAME: str = "Grey Dream Horse Shop (Конный магазин)"
    COMPANY_NAME: str = "GD Horse Shop (Конный магазин)"
    SHOP_URL: str = "https://www.instagram.com/gd_horse_shop/"


settings = Settings()
