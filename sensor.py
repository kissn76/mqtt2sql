from devices.LYWSD03MMC_ATC import LYWSD03MMC_ATC
from devices.LYWSD03MMC_ORIGINAL import LYWSD03MMC_ORIGINAL


class Sensor:
    def __init__(self, id, topic, sensorType, location=None) -> None:
        self.id = id
        self.sensorType = sensorType
        self.topic = topic
        self.location = location
        self.sensorData = eval(sensorType)()
        self.description = self.sensorData.description


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
        sd = {
            "id": self.id,
            "sensorType": self.sensorType,
            "description": self.description,
            "topic": self.topic,
            "location": self.location
        }
        td = dict(self.sensorData)
        sd.update(td)
        return sd


    def toString(self):
        toStr = ""
        for key, value in self.asdict().items():
            toStr += f"{key}: {value}\n"
        return toStr.strip()