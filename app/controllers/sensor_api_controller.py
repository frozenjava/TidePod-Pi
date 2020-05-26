from typing import List
from flask import jsonify

from app import app
from app.sensors import provide_sensors, Sensor

@app.route('/api/sensors')
@provide_sensors
def get_sensors(sensors: List[Sensor]):
    sensor_data = [ { 'name': s.name, 'is_active': s.is_active } for s in sensors ]
    return jsonify(sensor_data)


@app.route('/api/sensors/<string:name>')
@provide_sensors
def get_sensor(name: str, sensors: List[Sensor]):
    filtered: List[Sensor] = list(filter(lambda s: s.name == name, sensors))

    if len(filtered) == 0:
        return 'Unable to find sensor with that name.', 404
    elif len(filtered) > 1:
        return 'Too many sensors found by that name.', 500
    else:
        sensor = filtered[0]
        sensor_data = {'name': sensor.name, 'is_active': sensor.is_active }
        return jsonify(sensor_data)
