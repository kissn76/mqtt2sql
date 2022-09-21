# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long

# pip install paho-mqtt
# pip install mysql-connector-python

import configparser
import json
from paho.mqtt import client as mqtt_client
from sensor import Sensor
import settings
import db_mysql as db


setting = settings.Settings()
BROKER_HOST = setting.mqtt_host
BROKER_PORT = setting.mqtt_port
BROKER_USERNAME = setting.mqtt_user
BROKER_PASSWORD = setting.mqtt_password
BROKER_CLIENT_ID = 'python-mqtt-5'

ROUTER = {}
SENSORES = {}


def init():
    sensores_file = "sensores.ini"
    sensores_config = configparser.ConfigParser()
    sensores_config.read(sensores_file)
    sensores_ids = sensores_config.sections()
    for sensor_id in sensores_ids:
        obj = Sensor(sensor_id, sensores_config[sensor_id]["type"], sensores_config[sensor_id]["location"])
        SENSORES.update({sensor_id: obj})
        subtopics = obj.get_subtopics()
        for topic in json.loads(sensores_config[sensor_id]["topics"]):
            if len(subtopics) > 0:
                for subtopic in subtopics:
                    ROUTER.update({topic + "/" + subtopic: sensor_id})
            else:
                ROUTER.update({topic: sensor_id})


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):    # pylint: disable=unused-argument, invalid-name
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER_HOST, BROKER_PORT)
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):  # pylint: disable=unused-argument
        msg_topic = msg.topic
        if msg_topic in ROUTER:
            obj = SENSORES[ROUTER[msg_topic]]
            obj.sensor_data.fill_data(msg_topic, msg.payload.decode())
            if obj.is_ready():
                print(obj, '\n')
                datas = obj.asdict()
                date_time = datas["datetime"]
                sensor_id = datas["id"]
                location = datas["location"]
                datas.pop("datetime")
                datas.pop("id")
                datas.pop("sensorType")
                datas.pop("description")
                datas.pop("location")
                units = obj.get_unit()
                for key, value in datas.items():
                    unit = ""
                    if key in units:
                        unit = units[key]
                    if unit is None:
                        unit = ""
                    if isinstance(value, dict):
                        for value_key, value_value in value.items():
                            db.data_insert("sensordata", sensorid=sensor_id, datetime=date_time, location=location + "/" + value_key, sensorType=key, unit=unit, value=value_value)
                    else:
                        db.data_insert("sensordata", sensorid=sensor_id, datetime=date_time, location=location, sensorType=key, unit=unit, value=value)
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
    init()
    run()
