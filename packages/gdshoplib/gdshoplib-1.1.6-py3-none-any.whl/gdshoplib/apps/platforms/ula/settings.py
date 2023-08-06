from pydantic import BaseSettings


class Settings(BaseSettings):
    CATEGORY_ID: int = 5
    SUBCATEGORY_ID: int = 507
