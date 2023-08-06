from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):
    YADISK_PATH: DirectoryPath = "/Users/p141592/Yandex.Disk.localized/gdshop/gdlib"
    MEDIA_PATH_PATTERN: str = "{sku}/"
    FILENAME_PATTERN: str = "{key}_{stage}_{md5}.{format}"
