import datetime
import json


"""
shellies/shellyplug-s-C572BE/relay/0/power 0.57
shellies/shellyplug-s-C572BE/relay/0/energy 6972
shellies/shellyplug-s-C572BE/relay/0 on
shellies/shellyplug-s-C572BE/temperature 28.20
shellies/shellyplug-s-C572BE/overtemperature 0
"""


class SHELLYPLUG_S:
    def __init__(self):
        self.description = "Shelly Plug S"
        self.dateTime = None
        self.relayPower = {}
        self.relayEnergy = {}
        self.relay = {}
        self.temperature = None
        self.overtemperature = None


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
            "relayPower": self.relayPower,
            "relayEnergy": self.relayEnergy,
            "relay": self.relay,
            "temperature": self.temperature,
            "overtemperature": self.overtemperature
        }


    def toString(self):
        toStr = ""
        for key, value in self.asdict().items():
            toStr += f"{key}: {value}\n"
        return toStr.strip()


    def fillData(self, topic, msg):
        self.dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topicLine = topic.split("/")
        topicLine.pop(0)
        topicLine.pop(0)

        if topicLine[0] == "temperature":
            self.temperature = float(msg)
        elif topicLine[0] == "overtemperature":
            self.overtemperature = msg
        elif topicLine[0] == "relay":
            if len(topicLine) == 2:
                self.relay.update({topicLine[1]: msg})
            else:
                if topicLine[2] == "power":
                    self.relayPower.update({topicLine[1]: float(msg)})
                if topicLine[2] == "energy":
                    self.relayEnergy.update({topicLine[1]: int(msg)})