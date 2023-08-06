class BasePlatform:
    @classmethod
    def get_platform_class(cls, key=None):
        if not key:
            return cls.__subclasses__()

        for platform in cls.__subclasses__():
            if platform.KEY == key:
                return platform
