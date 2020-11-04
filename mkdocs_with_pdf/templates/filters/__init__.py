from mkdocs.config.base import Config


class _FilterBase:
    def __init__(self, options: object, config: Config):
        self.__options = options
        self.__config = config

    @property
    def options(self):
        return self.__options

    @property
    def config(self):
        return self.__config

    def __call__(self, *args):
        raise "must be overridden"
