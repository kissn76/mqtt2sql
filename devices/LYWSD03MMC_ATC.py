import datetime
import json


"""
home/OpenMQTTGateway/BTtoMQTT/A4C1386E4AE8 {"id":"A4:C1:38:6E:4A:E8","mac_type":0,"name":"ATC_6E4AE8","rssi":-91,"brand":"Xiaomi","model":"LYWSD03MMC","model_id":"LYWSD03MMC_ATC","tempc":14.2,"tempf":57.56,"hum":56,"batt":75,"volt":2.887}
"""


class LYWSD03MMC_ATC:
    def __init__(self):
        self.description = "Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) with ATC firmware"
        self.dateTime = None

        self.rssi = None
        self.tempc = None
        self.hum = None
        self.batt = None
        self.volt = None


    def __repr__(self):
        return self.toString()


    def __str__(self):
        return self.toString()


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
            "datetime": self.dateTime,
            "rssi": self.rssi,
            "temperature": self.tempc,
            "humidity": self.hum,
            "battery": self.batt,
            "voltage": self.volt
        }


    def reset(self):
        self.dateTime = None
        self.rssi = None
        self.tempc = None
        self.hum = None
        self.batt = None
        self.volt = None


    def isReady(self):
        if self.dateTime is not None and self.rssi is not None and self.tempc is not None and self.hum is not None and self.batt is not None and self.volt is not None:
            return True
        else:
            return False


    def toString(self):
        toStr = ""
        for key, value in self.asdict().items():
            toStr += f"{key}: {value}\n"
        return toStr.strip()


    def fillData(self, topic, msg):
        self.dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        jsonMsg = json.loads(msg)
        self.rssi = jsonMsg["rssi"]
        self.tempc = jsonMsg["tempc"]
        self.hum = jsonMsg["hum"]
        self.batt = jsonMsg["batt"]
        self.volt = jsonMsg["volt"]