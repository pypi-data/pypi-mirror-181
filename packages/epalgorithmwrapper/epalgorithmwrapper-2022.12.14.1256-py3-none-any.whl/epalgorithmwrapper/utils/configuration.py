from enum import Enum
import json
import asset

class Configuration(dict):
    CONFIGURATION_FILE_PATH = "epalgorithmwrapper:configuration.json"

    class Key(Enum):
        INPUT_DIRECTORY="input-directory"
        OUTPUT_DIRECTORY="output-directory"
        OUTPUT_REPORT_LOCATION="output-report-location"
        REPORT_TEMPLATE_LOCATION="report-template-location"
        RABBITMQ_STATUS_UPDATE_EXCHANGE="rabbitmq-status-update-exchange"
        RABBITMQ_STATUS_UPDATE_ROUTING="rabbitmq-status-update-routing"

    
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
    def get_configuration():
        configuration_str = asset.load(Configuration.CONFIGURATION_FILE_PATH).read()
        return Configuration(json.loads(configuration_str))