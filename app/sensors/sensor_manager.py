from threading import Thread
from typing import List, Callable, Dict

from app.sensors.sensor import Sensor
from app.sensors.sensor_factory import provide_sensors


class SensorManager(Thread):

    def __init__(self, sensors: List[Sensor]):
        super().__init__()
        self._callbacks: List[Callable[[str, bool], None]] = list()
        self._sensors: List[Sensor] = sensors

    def register_callback(self, callback: Callable[[str, bool], None]) -> None:
        """
        Register a new callback. This will get called when the sensor emits a new value.
        If the callback is already registered, it will not be added again.
        :param callback: A function that takes a bool as input. This value will be True if there is sensory input,
            or False if it does not.
        :return: None
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[str, bool], None]) -> None:
        """
        Remove an existing callback
        :param callback: A previously registered callback
        :return: None
        """
        self._callbacks.remove(callback)

    def run(self) -> None:
        """
        Loop over all of the sensors and poll them.
        If the 'is_active' status of the sensor has changed from the previous recorded value,
        notify all of the registered callbacks of the change.
        :return:
        """
        # Build a dictionary to track values.
        sensor_values: Dict[str, bool] = {sensor.name: sensor.is_active for sensor in self._sensors}

        while True:
            for sensor in self._sensors:
                sensor.poll_sensor()
                previous_value = sensor_values[sensor.name]
                current_value = sensor.is_active
                if current_value != previous_value:
                    sensor_values[sensor.name] = current_value
                    for callback in self._callbacks:
                        callback(sensor.name, current_value)
