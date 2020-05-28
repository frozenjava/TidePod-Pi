# TidePod-Pi
A Flask project to connect your washer and dryer to the network.

This project allows you to easly monitor values from sensors. You can see values by hitting an API endpoint or even register Event Handlers that will be triggered on a state change from a sensor. This makes integration with things such as Home Assistant incredibly easy.

# Setup
TidePod-Pi requires Python 3.7 or newer.

* Check your python version
```bash
python3 -V
```

* Clone the repository
```bash
git clone https://github.com/frozenjava/TidePod-Pi
```

* Change to the directory
```bash
cd TidePod-Pi
```

* Install Requirements
```bash
pip3 install -r requirements
```

* Create config file

You'll need to create a file called `config.json` (Note: You can use a different file name, just make sure to store the file name in an environment variable called TIDEPOD-PI-CONFIG. Ex: export TIDEPOD-PI-CONFIG=dev_config.json).
The basic structure of the config file should look like this:

```json
{
    "environment": "development",
    "sensors": [...],
    "eventhandlers": [...]
}
```

* Run the app
```bash
python3 -m app
```

# API Endpoints

## GET `http://<host:port>/api/sensors`
Returns a list of sensors and their current status. Example Response:

```json
[
    { "name": "Washing_Machine", "is_active": true },
    { "name": "Dryer", "is_active": false }
]
```

## GET `http://<host:port>/api/sensors/<sensor_name>`
Returns information about a single sensor by its name. Be sure to replae `<sensor_name>` with the actual name of your sensor (ex: `Dryer`). Example Response:

```json
{
    "name": "Dryer", 
    "is_active": false
}
```

# Sensors

## Sensors in config.json
To use a specific sensor, add a json object to the `sensors` array in your JSON config file. The basic structure of this object should look like this:

```json
[
    ...
    {
        "sensor_script": "app.sensors.my_sensor.MySensor",
        "sensor_name": "Washing Machine",
        "config": {
            "gpio_pin": 4,
            "gpio_mode": "input"
        }
    }
    ...
]
```

A description of the components:
* `sensor_script`: The path to the class of the sensor script you want to use. In the example we are using the MySensor we created below.
* `sensor_name`: This name can be whatever you want but should be descriptive of the device the sensor is attached too.
* `config`: A json object representation of the config object the sensor script is expecting. In this example MySensor expects MySensorConfig that has values for `gpio_pin` and `gpio_mode`

It should be noted that you can use as many sensors as you need. You can even use different sensor scripts at the same time.

## Create a new sensor
Sensors should live under `app.sensors.<sensor_name>` and extend `app.sensors.sensor.Sensor`. The sensor can optionally take an instance of a configuration object that is passed into the constructor. This configuration object should be a `dataclass`

### Example Sensor Configuration Object
```python
from dataclasses import dataclass

@dataclass
class MySensorConfig:
    gpio_pin: int
    gpio_mode: str
```

### Example Sensor
```python
from dataclasses import dataclass
from app.sensors.sensor import Sensor

class MySensor(Sensor[MySensorConfig]):

    def __init__(self, name: str, config: MySensorConfig):
        super().__init__(name, config)
        self._is_active: bool = False

    @property
    def is_active(self):
        return self._is_active

    def poll_sensor(self):
        """
        Do something like read from raspberry pi GPIO pin here.
        You can access the instance of MySensorConfig with self._config
        ex: self._config.gpio_pin | self._config.gpio_mode
        """

```

## Existing Sensor Scripts

### Sensor: `app.sensors.ads1115_piezo_sensor.py`

This sensor is built to be used with a [Piezo Transducer](https://www.amazon.com/Prewired-Elements-Buzzer-Sounder-Trigger/dp/B01N5HN94S/) connected to an [ADS1115](https://www.amazon.com/Converter-Programmable-Amplifier-Development-Raspberry/dp/B07TGB6KF8/) connected to a Raspberry Pi

#### Wiring Raspberry Pi to ADS1115:
Pi: Ground -> ADS1115: GND
Pi: 3.3V -> ADS1115: VDD
Pi: SDA -> ADS1115: SDA
Pi: SCL -> ADS1115: SCL

#### Wiring Piezo Transducer to ADS1115
Transducer: Ground -> ADS1115: GND
Transducer: Signal -> ADS1115: A1-A3

#### Additional Pi Configuration

Make sure SPI is enabled on your Raspberry Pi.

```bash
sudo raspi-config
```
Interfacing Options -> SPI -> Finish

Also, make sure the adafruit-ads1x15 python module is installed.

```bash
pip3 install adafruit-ads1x15
```

#### Configuration

This script expects an instance of `app.sensors.ads1115_piezo_sensor.ADS1115PiezoSensor` which has the following properties:

* `channel`: The A0-A3 channel the transducer is connected to
* `gain`: The gain for the ADS1115
* `time_interval`: The ammount of time between calculating input average (in seconds)
* `gate_threshold`: The amount of vibration it takes to regeister as valid input.

To use this script on your pi add the following you the `sensors` list in your json config file.

```json
{
    ...
    "sensors": [
        ,,,
        {
            "sensor_script": "app.sensors.ads1115_piezo_sensor.ADS1115PiezoSensor",
            "sensor_name": "Washing Machine",
            "config": {
                "channel": "<your_channel [0-3]>",
                "gain": 1,
                "time_interval": 30,
                "gate_threshold": 10000
            }
        }
        ...
    ]
    ...
}
```

# Event Handlers

Event handlers are callbacks that get triggered anytime a state change happens from a sensor (ex: `off` -> `on` or `on` -> `off`). This can be incredibly useful to integrate with Home Assistant, send push notifications to phones, or whatever else you can think of.

Docs comming soon...
