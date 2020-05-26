from app import app
from app.sensors import SensorManager, build_sensors
from app.controllers.sensor_api_controller import *


if __name__ == '__main__':
    sensors = build_sensors()
    sensor_manager = SensorManager(sensors=sensors)
    sensor_manager.start()
    app.run()
