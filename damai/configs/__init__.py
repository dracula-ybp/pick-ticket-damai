import os
import yaml
from typing import Optional

from damai.configs import default_configs


class Configs:

    FILE = "config.yaml"

    def __init__(self, values: Optional[dict] = None):
        self.config = dict(_default_configs())
        if values:
            self.update(values)
        self.load_custom_configs()

    def __getitem__(self, opt_name):
        if opt_name not in self:
            return None
        return self.config[opt_name].value

    def __contains__(self, name):
        return name in self.config

    def __setitem__(self, name, value):
        self.set(name, value)

    def load_custom_configs(self):
        paths = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', self.FILE)),
            os.path.expanduser(f'~/{self.FILE}')
        )
        existing_path = next((p for p in paths if os.path.isfile(p)), None)
        if existing_path:
            self._load_yaml(existing_path)

    def _load_yaml(self, file):
        with open(file) as fp:
            config = yaml.safe_load(fp)
            self.config.update(config)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def update(self, values: dict):
        self.config = {**self.config, **values}


def _default_configs():
    for name in dir(default_configs):
        if name.isupper():
            yield name, getattr(default_configs, name)



