# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long

# pip install paho-mqtt
# pip install mysql-connector-python

import configparser
import json
import os
from paho.mqtt import client as mqtt_client
from sensor import Sensor
from topic import Topic
from device import Device
import settings
import db_mysql as db


SETTINGS = settings.Settings()
BROKER_HOST = SETTINGS.mqtt_host
BROKER_PORT = SETTINGS.mqtt_port
BROKER_USERNAME = SETTINGS.mqtt_user
BROKER_PASSWORD = SETTINGS.mqtt_password
BROKER_CLIENT_ID = 'python-mqtt-5'

TOPICS = {}
DEVICES = {}
ROUTER = {}
DATABASES = {}


# setting = settings.Settings()
# MYSQL_HOST = setting.mysql_host
# MYSQL_USER = setting.mysql_user
# MYSQL_PASSWORD = setting.mysql_password
# MYSQL_DATABASE = setting.mysql_database


def init():
    for filename in os.scandir("etc/mysql_connections"):
        if filename.is_file():
            db_object = db.Mysqldatabase(filename)
            DATABASES.update({db_object.name: db_object})
            db_object.create_tables()
    exit()

    topics_file = "etc/topics.ini"
    topics_config = configparser.ConfigParser()
    topics_config.read(topics_file)
    topics = topics_config.sections()
    for topic in topics:
        topicobj = Topic(topic, topics_config[topic]["type"], topics_config[topic]["device"])
        if topicobj.type == "json":
            pass
        else:
            sensorobj = Sensor(topicobj.type, topics_config[topic]["sensorname"], topics_config[topic]["unit"], topics_config[topic]["conversion"], topics_config[topic]["location"])
            topicobj.sensores.update({0: sensorobj})

        TOPICS.update({topic: topicobj})

    devices_file = "etc/devices.ini"
    devices_config = configparser.ConfigParser()
    devices_config.read(devices_file)
    devices_ids = devices_config.sections()
    for device_id in devices_ids:
        DEVICES.update({device_id: Device(device_id, devices_config[device_id]["type"], devices_config[device_id]["location"])})


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
        msg_message = msg.payload.decode()
        topic_obj = TOPICS[msg_topic]
        device_id = topic_obj.device
        topic_type = topic_obj.type
        topic_topic = topic_obj.topic
        device = DEVICES[device_id]

        if topic_type == "json":
            # msg_json = json.loads(msg_message)
            # for key, value in msg_json.items():
            #     print(topic_topic, key, value)
            pass
        else:
            print(topic_topic, msg_message)

        # print(msg_topic, msg.payload.decode(), '\n')

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    for topic in TOPICS:
        subscribe(client, topic)
    client.loop_forever()


if __name__ == '__main__':
    init()
    db.create_tables()
    run()
