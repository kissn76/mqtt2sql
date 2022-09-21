# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

import datetime


# pylint: disable=pointless-string-statement
"""
shellies/shellyplug-s-C572BE/relay/0/power 0.57
shellies/shellyplug-s-C572BE/relay/0/energy 6972
shellies/shellyplug-s-C572BE/relay/0 on
shellies/shellyplug-s-C572BE/temperature 28.20
shellies/shellyplug-s-C572BE/overtemperature 0
"""


class ShellyPlugS:
    def __init__(self):
        self.description = "Shelly Plug S"
        self.date_time = None

        self.power = {}
        self.energy = {}
        self.state = {}
        self.temperature = None
        self.overtemperature = None


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
        return {
            "datetime": self.date_time,
            "power": self.power,
            "energy": self.energy,
            "state": self.state,
            "temperature": self.temperature,
            "overtemperature": self.overtemperature
        }


    def get_unit(self):
        return {
            "power": "W",
            "energy": "kWh",
            "state": None,
            "temperature": "°C",
            "overtemperature": None
        }


    def get_subtopics(self):
        return [
            "relay/0/power",
            "relay/0/energy",
            "relay/0",
            "temperature",
            "overtemperature"
        ]


    def reset(self):
        self.date_time = None
        self.power = {}
        self.energy = {}
        self.state = {}
        self.temperature = None
        self.overtemperature = None


    def is_ready(self):
        if self.date_time is not None and self.power is not None and self.energy is not None and self.state is not None and self.temperature is not None and self.overtemperature is not None:
            return True
        else:
            return False


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


    def fill_data(self, topic, msg):
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topic_list = topic.split("/")
        topic_list.pop(0)
        topic_list.pop(0)

        if topic_list[0] == "temperature":
            self.temperature = float(msg)
        elif topic_list[0] == "overtemperature":
            self.overtemperature = msg
        elif topic_list[0] == "relay":
            if len(topic_list) == 2:
                if msg == "on":
                    msg = 1
                else:
                    msg = 0
                self.state.update({topic_list[1]: msg})
            else:
                if topic_list[2] == "power":
                    self.power.update({topic_list[1]: float(msg)})
                if topic_list[2] == "energy":
                    self.energy.update({topic_list[1]: round(float(msg) * 0.00001666666666666666667, 4)})   # watt minute => kWh
