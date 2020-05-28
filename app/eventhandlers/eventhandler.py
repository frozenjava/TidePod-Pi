from typing import Optional, TypeVar, Generic
import abc


TConfig = TypeVar('TConfig')


class EventHandler(Generic[TConfig]):
    
    def __init__(self, name: str, config: Optional[TConfig]):
        """
        @param name: The name of this event handler.
        @param config: The config object for this event handler
        """
        self.name: str = name
        self._config: Optional[TConfig] = config

    @abc.abstractmethod
    def on_state_change(self, sensor_name: str, new_state: bool):
        """
        @param sesnor_name: The name of the sensor
        @param new_state: The active state of the sensor
        """
        raise NotImplementedError('on_state_changed not implemented.')
