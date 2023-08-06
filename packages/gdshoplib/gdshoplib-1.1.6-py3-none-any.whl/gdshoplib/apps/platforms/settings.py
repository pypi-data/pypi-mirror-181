from pydantic import BaseSettings


class PlatformSettings(BaseSettings):
    PLATFORM_DB: str = ""
