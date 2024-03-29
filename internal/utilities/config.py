import os
import yaml
import logging

from internal.utilities.decorators import singleton

@singleton
class Config:
    def __init__(self, file_path):
        try:
            self.file_path = file_path
            self.config = self.load_config()
            self.set_env_variables(self.config)
        except Exception as e:
            logging.log(level=logging.ERROR, msg="config is broken")
    

    def load_config(self):
        with open(self.file_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def get(self, key):
        try:
            return os.environ[f"{key}"]
        except KeyError:
            logging.log(level=logging.ERROR, msg=f'Cant find {key}')

    def set_env_variables(self, items, prefix=""):
        for key, value in items.items():
            if type(value) == dict:
                self.set_env_variables(value, prefix=f"{prefix}{key}")
            else:
                os.environ[f"{prefix}_{key}"] = str(value)
