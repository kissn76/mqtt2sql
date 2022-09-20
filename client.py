import random
from paho.mqtt import client as mqtt_client
import settings
from devices.LYWSD03MMC_ATC import LYWSD03MMC_ATC


broker = settings.mqttHost
port = settings.mqttPort
username = settings.mqttUser
password = settings.mqttPasswd
client_id = 'python-mqtt-5'

router = {
    "home/OpenMQTTGateway/BTtoMQTT/A4C1387AB9CF" : LYWSD03MMC_ATC,
    "home/OpenMQTTGateway/BTtoMQTT/A4C138E57826" : LYWSD03MMC_ATC,
    "home/OpenMQTTGateway/BTtoMQTT/A4C1386E4AE8" : LYWSD03MMC_ATC
    }


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
            obj = router[msgTopic](msg.payload.decode())
            obj.print()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    topic = "#"
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()


if __name__ == '__main__':
    run()
