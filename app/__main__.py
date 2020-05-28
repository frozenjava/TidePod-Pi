from app import app
from app.sensors import SensorManager, build_sensors
from app.eventhandlers import build_eventhandlers
from app.controllers.sensor_api_controller import *


if __name__ == '__main__':
    sensors = build_sensors()
    eventhandlers = build_eventhandlers()
    sensor_manager = SensorManager(sensors=sensors, eventhandlers=eventhandlers)
    sensor_manager.start()
    app.run()
