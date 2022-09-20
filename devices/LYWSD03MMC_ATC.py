import datetime
import json


class LYWSD03MMC_ATC:
    def __init__(self, msg):
        self.dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        jsonMsg = json.loads(msg)
        self.id = jsonMsg["id"]
        self.rssi = jsonMsg["rssi"]
        self.tempc = jsonMsg["tempc"]
        self.hum = jsonMsg["hum"]
        self.batt = jsonMsg["batt"]
        self.volt = jsonMsg["volt"]


    def print(self):
        print("Xiaomi Mi Temperature and Humidity Monitor 2 (LYWSD03MMC) with ATC firmware")
        print(f"dateTime: {self.dateTime}")
        print(f"id: {self.id}")
        print(f"rssi: {self.rssi}")
        print(f"temperature: {self.tempc}°C")
        print(f"humidity: {self.hum}%")
        print(f"battery: {self.batt}% {self.volt}V")