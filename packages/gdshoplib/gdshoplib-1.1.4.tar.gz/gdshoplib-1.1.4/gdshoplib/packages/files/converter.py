# Конвертируем контент
from PIL import Image


class BaseConverter:
    def __init__(self, file, *args, **kwargs) -> None:
        ...

    @classmethod
    def get_converter(cls, media_type):
        for converter in cls.__subclasses__():
            if converter.MEDIA_TYPE == media_type:
                return converter

    @property
    def need_convert(self):
        raise NotImplementedError

    @property
    def need_mark(self):
        raise NotImplementedError


class ImageConverter(BaseConverter):
    MEDIA_TYPE = "image"
    ACCEPTED_FORMATS = (
        "jpg",
        "jpeg",
        "png",
    )

    def __init__(self, file, *args, **kwargs):
        self.image = Image.open(file)
        super().__init__(self, file, *args, **kwargs)

    @property
    def need_convert(self):
        ...

    @property
    def need_mark(self):
        ...

    def convert(self):
        # return self.disk.save(content, **self.disk.get_media_path(product, media))
        ...

    def mark(self):
        # return self.disk.save(content, **self.disk.get_media_path(product, media))
        ...


class VideoConverter(BaseConverter):
    MEDIA_TYPE = "video"

    def __init__(self, file, *args, **kwargs):
        self.image = Image.open(file)
        super().__init__(self, file, *args, **kwargs)

    @property
    def need_convert(self):
        ...

    @property
    def need_mark(self):
        ...

    def convert(self):
        # return self.disk.save(content, **self.disk.get_media_path(product, media))
        ...

    def mark(self):
        # return self.disk.save(content, **self.disk.get_media_path(product, media))
        ...
