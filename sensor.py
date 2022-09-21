# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

from devices.lywsd03mmc_atc import Lywsd03mmcAtc    # pylint: disable=unused-import
from devices.shellyplug_s import ShellyPlugS        # pylint: disable=unused-import


class Sensor:
    def __init__(self, sensor_id, sensor_type, location=None) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.location = location
        self.sensor_data = globals()[sensor_type]()
        self.description = self.sensor_data.description


    def __repr__(self):
        return self.to_string()


    def __str__(self):
        return self.to_string()


    def keys(self):
        return self.asdict().keys()


    def values(self):
        return self.asdict().values()


    def items(self):
        return self.asdict().items()


    def __getitem__(self, key):
        return self.asdict()[key]


    def asdict(self):
        sensor_d = {
            "id": self.sensor_id,
            "sensorType": self.sensor_type,
            "description": self.description,
            "location": self.location
        }
        last_d = dict(self.sensor_data)
        sensor_d.update(last_d)
        return sensor_d


    def get_unit(self):
        return self.sensor_data.get_unit()


    def get_subtopics(self):
        return self.sensor_data.get_subtopics()


    def reset(self):
        self.sensor_data.reset()


    def is_ready(self):
        return self.sensor_data.is_ready()


    def to_string(self):
        ret = ""
        units = self.get_unit()
        for key, value in self.asdict().items():
            unit = ""
            if key in units:
                unit = units[key]
            if unit is None:
                unit = ""
            if isinstance(value, dict):
                for value_key, value_value in value.items():
                    ret += f"{key}/{value_key}: {value_value}{unit}\n"
            else:
                ret += f"{key}: {value}{unit}\n"

        return ret.strip()
