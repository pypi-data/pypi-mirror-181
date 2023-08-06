import json


class Settings:
    timeout = 1800

    @classmethod
    def set_config(cls, config):
        for k in config:
            setattr(cls, k, config[k])

    @classmethod
    def __repr__(cls):
        d = {a: getattr(Settings, a) for a in dir(Settings) if not a.startswith("__")}
        d.pop("set_config")
        return json.dumps(d)
