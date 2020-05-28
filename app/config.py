from dataclasses import dataclass
from typing import List, Optional
import os
import json

import dacite


@dataclass
class MetaSensor:
    sensor_script: str
    name: str
    config: dict


@dataclass
class MetaEventHandler:
    eventhandler_script: str
    name: str
    config: dict


@dataclass
class Config:
    environment: str
    sensors: List[MetaSensor]
    eventhandlers: List[MetaEventHandler]


def load_config() -> Config:
    config_file = os.getenv('TIDEPOD_PI_CONFIG', 'config.json')

    if not os.path.isfile(config_file):
        raise FileNotFoundError()

    with open(config_file, 'r') as f:
        config_dict = json.load(f)

    return dacite.from_dict(data_class=Config, data=config_dict)
