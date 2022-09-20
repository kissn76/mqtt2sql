import datetime
import json


class LYWSD03MMC_ATC:
    def __init__(self, msg, location):
        self.dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.location = location
        jsonMsg = json.loads(msg)
        self.id = jsonMsg["id"]
        self.rssi = jsonMsg["rssi"]
        self.tempc = jsonMsg["tempc"]
        self.hum = jsonMsg["hum"]
        self.batt = jsonMsg["batt"]
        self.volt = jsonMsg["volt"]


    def getData(self):
        return({
            "location": self.location,
            "detetime": self.dateTime,
            "type": "Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) with ATC firmware",
            "id": self.id,
            "rssi": self.rssi,
            "temperature": self.tempc,
            "humidity": self.hum,
            "battery": self.batt,
            "voltage": self.volt
            })


    def print(self):
        print("Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) with ATC firmware")
        print(f"location: {self.location}")
        print(f"dateTime: {self.dateTime}")
        print(f"id: {self.id}")
        print(f"rssi: {self.rssi}")
        print(f"temperature: {self.tempc}°C")
        print(f"humidity: {self.hum}%")
        print(f"battery: {self.batt}% {self.volt}V")