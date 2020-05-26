from typing import Optional, TypeVar, Generic
import abc


TConfig = TypeVar('TConfig')


class Sensor(Generic[TConfig]):
    
    def __init__(self, name: str, config: Optional[TConfig]):
        """
        @param name: The name of this sesnor. Must be unique to all sensors
        @param config: The config object for this sensor
        """
        self.name: str = name
        self._config: Optional[TConfig] = config

    @property
    @abc.abstractmethod
    def is_active(self) -> bool:
        """
        Determine if the device the sensor is attached to is currently active.
        :return: True if active, False if not.
        """
        raise NotImplementedError('is_active not implemented.')

    @abc.abstractmethod
    def poll_sensor(self):
        """
        Do something to get input from a sensor.
        :return: True if the sensor has a signal, otherwise return False
        """
        raise NotImplementedError('poll_sensor not implemented.')
