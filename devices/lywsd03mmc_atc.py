# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

import datetime
import json


# pylint: disable=pointless-string-statement
"""
home/OpenMQTTGateway/BTtoMQTT/A4C1386E4AE8 {"id":"A4:C1:38:6E:4A:E8","mac_type":0,"name":"ATC_6E4AE8","rssi":-91,"brand":"Xiaomi","model":"LYWSD03MMC","model_id":"LYWSD03MMC_ATC","tempc":14.2,"tempf":57.56,"hum":56,"batt":75,"volt":2.887}
"""


class Lywsd03mmcAtc:
    def __init__(self):
        self.description = "Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) with ATC firmware"
        self.date_time = None

        self.rssi = None
        self.tempc = None
        self.hum = None
        self.batt = None
        self.volt = None


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
            "rssi": self.rssi,
            "temperature": self.tempc,
            "humidity": self.hum,
            "battery": self.batt,
            "voltage": self.volt
        }


    def get_unit(self):
        return {
            "rssi": "dBm",
            "temperature": "°C",
            "humidity": "%",
            "battery": "%",
            "voltage": "V"
        }


    def get_subtopics(self):
        return []


    def reset(self):
        self.date_time = None
        self.rssi = None
        self.tempc = None
        self.hum = None
        self.batt = None
        self.volt = None


    def is_ready(self):
        if self.date_time is not None and self.rssi is not None and self.tempc is not None and self.hum is not None and self.batt is not None and self.volt is not None:
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


    def fill_data(self, topic, msg):    # pylint: disable=unused-argument
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_json = json.loads(msg)
        self.rssi = msg_json["rssi"]
        self.tempc = msg_json["tempc"]
        self.hum = msg_json["hum"]
        self.batt = msg_json["batt"]
        self.volt = msg_json["volt"]
