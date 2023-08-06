class BasePlatform:
    @classmethod
    def get_platform_class(cls, key):
        for platform in cls.__subclasses__:
            if platform.KEY == key:
                return platform
