import datetime
import json


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


    def toString(self):
        toStr = ""
        for key, value in self.asdict().items():
            toStr += f"{key}: {value}\n"
        return toStr


    def fillData(self, msg):
        self.dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        jsonMsg = json.loads(msg)
        self.rssi = jsonMsg["rssi"]
        self.tempc = jsonMsg["tempc"]
        self.hum = jsonMsg["hum"]
        self.batt = jsonMsg["batt"]
        self.volt = jsonMsg["volt"]