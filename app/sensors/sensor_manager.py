from threading import Thread
from typing import List, Callable, Dict

from app.sensors.sensor import Sensor
from app.sensors.sensor_factory import provide_sensors
from app.eventhandlers import EventHandler


class SensorManager(Thread):

    def __init__(self, sensors: List[Sensor], eventhandlers: List[EventHandler]):
        super().__init__()
        self._sensors: List[Sensor] = sensors
        self._eventhandlers: List[EventHandler] = eventhandlers
        self.running: bool = False

    def run(self) -> None:
        """
        Loop over all of the sensors and poll them.
        If the 'is_active' status of the sensor has changed from the previous recorded value,
        notify all of the registered callbacks of the change.
        :return:
        """

        self.running = True

        # Build a dictionary to track values.
        sensor_values: Dict[str, bool] = {sensor.name: sensor.is_active for sensor in self._sensors}

        while self.running:
            for sensor in self._sensors:
                sensor.poll_sensor()
                previous_value = sensor_values[sensor.name]
                current_value = sensor.is_active
                if current_value != previous_value:
                    sensor_values[sensor.name] = current_value
                    for eventhandler in self._eventhandlers:
                        eventhandler.on_state_change(sensor.name, current_value)
