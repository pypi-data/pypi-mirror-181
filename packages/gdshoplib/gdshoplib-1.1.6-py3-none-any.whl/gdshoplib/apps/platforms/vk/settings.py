from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN: Optional[str]
    COMMUNITY_ID: str
    CLIENT_ID: str = "51474001"
    CLIENT_SECRET: str

    REDIRECT_URI: str = "http://localhost:8001"
    GROUP_IDS: List
    DISPLAY: str = "page"
    SCOPE: str
    RESPONSE_TYPE: str = "code"
    V: str = "5.131"
