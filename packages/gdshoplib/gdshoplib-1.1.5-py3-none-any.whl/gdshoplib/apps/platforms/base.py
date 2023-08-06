class BasePlatform:
    def __init__(self, *args, **kwargs):
        self.settings = self.SETTINGS()
        super(BasePlatform, self).__init__(*args, **kwargs)

    @classmethod
    def get_platform_class(cls, key=None):
        if not key:
            return cls.__subclasses__()

        for platform in cls.__subclasses__():
            if platform.KEY.lower() == key.lower():
                return platform
