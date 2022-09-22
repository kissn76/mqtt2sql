# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

class Sensor:
    def __init__(self, sensor_type, sensorname, unit, conversion, location):
        self.type = sensor_type
        self.sensorname = sensorname
        self.unit = unit
        self.conversion = conversion
        self.location = location
