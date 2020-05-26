from dataclasses import dataclass
from typing import List, Generic
from datetime import datetime

import Adafruit_ADS1x15

from app.sensors.sensor import Sensor


@dataclass
class ADS1115PiezoConfig:
    channel: int
    gain: int
    time_interval: int
    gate_threshold: int


class ADS1115PiezoSensor(Sensor[ADS1115PiezoConfig]):

    def __init__(self, name: str, config: ADS1115PiezoConfig):
        super().__init__(name, config)

        self._adc = Adafruit_ADS1x15.ADS1115()              # The ADS1115 Sensor
        self._values: List[int] = []                        # Record values emitted
        self._is_active: bool = False                       # The last known active status from the sensor
        self._last_average: datetime = datetime.utcnow()    # Last time the average activity was calculated

    @property
    def is_active(self) -> bool:
        return self._is_active

    def _record_value(self, value: int):
        """
        Record values emitted by the sensor.
        If the value is equal to or above the gate_threshold in the config, record a 1.
        If it is less than the gate_threshold, record a 0
        @param value: An integer value emitted by the sensor.
        """
        if value >= self._config.gate_threshold:
            self._values.append(1)
        else:
            self._values.append(0)

    def _update_active_status(self):
        """
        Calculate the average of self._values every self._config.time_interval seconds.
        If the average is greater than or equal to 0.5 then consider the device active.
        """
        if (datetime.utcnow() - self._last_average).total_seconds() >= self._config.time_interval:
            average = sum(self._values) / len(self._values)
            self._values = []
            self._last_average = datetime.utcnow()
            self._is_active = average >= 0.5

    def poll_sensor(self):
        """
        Poll the sensor and get the latest value, track it, and determine if the device is active.
        """
        value = self._adc.read_adc(self._config.channel, self._config.gain)
        self._record_value(value)
        self._update_active_status()
