from functools import wraps
from typing import List
import importlib

import dacite

from app.sensors.sensor import Sensor
from app import config


_sensors: List[Sensor] = []


def build_sensors() -> List[Sensor]:
    """
    For each sensor in the config.sensors list of MetaSensor this should do the following:
    * Attempt to find the class of the sensor from MetaSensor.sensor_script
    * Attempt to find the generic type for the sensors config object
    * Attempt to deserialize the config object from MetaSensor.config to the generic type
    * Attempt to instanciate the Sensor, passing in the name from MetaSensor.name and deserialized config object
    @return: The list of instanciated Sensor objects.
    """
    global _sensors

    _sensors = []

    for meta_sensor in config.sensors:
        class_name = meta_sensor.sensor_script.split('.')[-1]
        module_name = '.'.join(meta_sensor.sensor_script.split('.')[:-1])
        module = importlib.import_module(module_name)
        clazz = getattr(module, class_name)

        if clazz is None:
            raise TypeError(f'Could not find class for sensor_script {config.sensor_script}')

        sensor_config_clazz = clazz.__orig_bases__[0].__args__[0]

        sensor_config = dacite.from_dict(sensor_config_clazz, meta_sensor.config)

        sensor = clazz(meta_sensor.name, sensor_config)
        _sensors.append(sensor)

    return _sensors


def provide_sensors(func):
    """
    Use this decorator to inject a list of all instanciated sensors into a function.
    Sensors will be injected with the kwarg 'sensors'.
    """
    global _sensors

    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs.update({'sensors': _sensors})
        return func(*args, **kwargs)

    return wrapper
