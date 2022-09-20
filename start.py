import random
from paho.mqtt import client as mqtt_client
import settings
import configparser
from devices.LYWSD03MMC_ATC import LYWSD03MMC_ATC


broker = settings.mqttHost
port = settings.mqttPort
username = settings.mqttUser
password = settings.mqttPasswd
client_id = 'python-mqtt-5'

router = {}
sensoresFile = "sensores.ini"
sensoresConfig = configparser.ConfigParser()
sensoresConfig.read(sensoresFile)
sensores = sensoresConfig.sections()
for sensor in sensores:
    router.update({sensoresConfig[sensor]["topic"] : {"class": eval(sensoresConfig[sensor]["type"]), "location": sensoresConfig[sensor]["location"]}})


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        msgTopic = msg.topic

        if msgTopic in router:
            obj = router[msgTopic]["class"](msg.payload.decode(), router[msgTopic]["location"])
            print(obj.getData())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    topic = "#"
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()


if __name__ == '__main__':
    run()
