from pydantic import BaseSettings


class Settings(BaseSettings):
    meta_column_name: str = "标记"


class ProxySettings:
    _obj: Settings

    def __init__(self):
        self.reload_settings({})

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key == "_obj":
            self.__dict__[key] = value
        else:
            setattr(self._obj, key, value)

    def reload_settings(self, d):

        self._obj = Settings(**d)


settings: Settings = ProxySettings()
