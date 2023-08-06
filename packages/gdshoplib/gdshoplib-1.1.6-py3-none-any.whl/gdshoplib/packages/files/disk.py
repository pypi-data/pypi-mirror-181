import hashlib
from pathlib import Path

from gdshoplib.packages.files.settings import Settings


class Disk:
    def __init__(self):
        self.settings = Settings()

    @staticmethod
    def get_md5(content):
        md5Hash = hashlib.md5(content)
        return md5Hash.hexdigest()

    def create_full_path(self, path):
        current = Path("/")
        for p in str(path.resolve()).split("/"):
            _path = current / p
            if not _path.exists():
                _path.mkdir()
            current = _path

    def _save(self, content, *args, path, filename):
        _path = Path(path) / filename
        with open(_path, "wb") as f:
            f.write(content)
        return _path

    def absolute_path(func):
        def wrap(self, *args, **kwargs):
            kwargs["path"] = (
                Path(self.settings.YADISK_PATH) / kwargs["path"]
            ).resolve()
            return func(self, *args, **kwargs)

        return wrap

    @absolute_path
    def save(self, *args, path, filename, **kwargs):
        if not path.exists():
            self.create_full_path(path)

        if not path.is_dir():
            raise DiskArgsException

        if (path / filename).exists():
            return path / filename

        return self._save(*args, path, filename, **kwargs)

    def get_media_path(self, product, media, *, stage="original"):
        """Получить полный путь файла, каким он должен быть"""
        # MEDIA_PATH_PATTERN: str = "{sku}/{key}/"
        # FILENAME_PATTERN: str = "{stage}_{md5}.{format}"
        return dict(
            path=self.settings.MEDIA_PATH_PATTERN.format(
                **self.get_keys(product, media, stage=stage)
            ),
            filename=self.settings.FILENAME_PATTERN.format(
                **self.get_keys(product, media, stage=stage)
            ),
        )

    def get_keys(self, product, media, *args, stage):
        return dict(
            sku=product.dict()["sku"],
            key=media.key,
            stage=stage,
            md5=media.md5,
            format=media.format,
        )


class DiskArgsException(BaseException):
    ...
