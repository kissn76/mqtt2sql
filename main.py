from datetime import datetime
import random
from paho.mqtt import client as mqtt_client
from sensor import Sensor
import settings
import configparser
import json
import db_mysql as db
from devices.LYWSD03MMC_ATC import LYWSD03MMC_ATC
from devices.SHELLYPLUG_S import SHELLYPLUG_S


broker = settings.mqttHost
port = settings.mqttPort
username = settings.mqttUser
password = settings.mqttPasswd
client_id = 'python-mqtt-5'

router = {}
sensores = {}
sensoresFile = "sensores.ini"
sensoresConfig = configparser.ConfigParser()
sensoresConfig.read(sensoresFile)
sensoresIDs = sensoresConfig.sections()
for sensorID in sensoresIDs:
    sensores.update({sensorID: Sensor(sensorID, sensoresConfig[sensorID]["type"], sensoresConfig[sensorID]["location"])})
    for topic in json.loads(sensoresConfig[sensorID]["topics"]):
        router.update({topic: sensorID})


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        msgTopic = msg.topic
        if msgTopic in router:
            obj = sensores[router[msgTopic]]
            obj.sensorData.fillData(msgTopic, msg.payload.decode())
            if obj.isReady():
                # print(obj, '\n')
                datas = obj.asdict()
                dateTime = datas["datetime"]
                id = datas["id"]
                location = datas["location"]
                datas.pop("datetime")
                datas.pop("id")
                datas.pop("sensorType")
                datas.pop("description")
                datas.pop("location")
                for key, value in datas.items():
                    if type(value) is dict:
                        for valueKey, valueValue in value.items():
                            db.data_insert("sensordata", sensorid=id, datetime=dateTime, location=location + valueKey, sensorType=key, unit=None, value=valueValue)
                    else:
                        db.data_insert("sensordata", sensorid=id, datetime=dateTime, location=location, sensorType=key, unit=None, value=value)

                obj.reset()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    topic = "#"
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()


if __name__ == '__main__':
    db.create_tables()
    run()
