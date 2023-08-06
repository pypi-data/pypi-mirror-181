from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    NOTION_SECRET_TOKEN: str
    CACHE_PERIOD: int = 1 * 60 * 60 * 24
    CACHE: bool = True
    CACHE_CLASS: Optional[str]
    CACHE_DSN: Optional[str]
