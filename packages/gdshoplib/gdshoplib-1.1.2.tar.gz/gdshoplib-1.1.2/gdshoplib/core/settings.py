import os
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath

BASEPATH = Path(os.path.dirname(os.path.realpath(__file__))).parent


class Settings(BaseSettings):
    TEMPLATES_PATH: DirectoryPath = (BASEPATH / "templates").resolve()
    PHONE: str = "+7 499 384 44 03"


settings = Settings()
