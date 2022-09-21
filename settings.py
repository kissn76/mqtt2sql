# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

import configparser


class Settings:
    def __init__(self):
        settings_file = "settings.ini"

        config = configparser.ConfigParser()
        config.read(settings_file)

        self.mqtt_host = config["MQTT"]["host"]
        self.mqtt_port = int(config["MQTT"]["port"])
        self.mqtt_user = config["MQTT"]["user"]
        self.mqtt_password = config["MQTT"]["passwd"]

        self.mysql_host = config["MYSQL"]["host"]
        self.mysql_user = config["MYSQL"]["user"]
        self.mysql_password = config["MYSQL"]["passwd"]
        self.mysql_database = config["MYSQL"]["database"]
