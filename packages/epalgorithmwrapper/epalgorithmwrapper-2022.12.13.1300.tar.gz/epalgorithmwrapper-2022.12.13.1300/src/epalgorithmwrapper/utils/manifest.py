from enum import Enum
from .filesystem_utils import get_file_contents
import json

class Manifest(dict):
    MANIFEST_FILE_PATH = "./manifest.json"

    class Key(Enum):
        MANIFEST_VERSION = "manifest-version"
        IDENTIFIER = "identifier"
        COMMAND = "command"
        DEVELOPMENT = "dev"
        INPUT = "input"
        OUTPUT = "output"
    
    def __init__(self, dict: dict) -> None:
        self.__dict__ = dict

    def __setitem__(self, key, item):
        self.__dict__[key.value] = item

    def __getitem__(self, key):
        return self.__dict__[key.value]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key.value]
    
    def __contains__(self, key) -> bool:
        return key.value in self.__dict__

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k.value in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()   
             
    @staticmethod
    def get_manifest(development=False):
        configuration_str = get_file_contents(Manifest.MANIFEST_FILE_PATH)
        mf: dict = json.loads(configuration_str)
        if "dev" in mf:
            if development:
                dev_vars: dict = mf["dev"]
                for k, v in dev_vars.items():
                    mf[k] = v
            mf.pop("dev")

        return Manifest(mf)