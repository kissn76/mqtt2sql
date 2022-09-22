# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

class Device:
    def __init__(self, device_id, device_type, location=None):
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
