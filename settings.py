import configparser

settingsFile = "settings.ini"

mqttHost = None
mqttPort = None
mqttUser = None
mqttPasswd = None

mysqlHost = None
mysqlUser = None
mysqlPasswd = None
mysqlDatabase = None

config = configparser.ConfigParser()
config.read(settingsFile)

mqttHost = config["MQTT"]["host"]
mqttPort = int(config["MQTT"]["port"])
mqttUser = config["MQTT"]["user"]
mqttPasswd = config["MQTT"]["passwd"]

mysqlHost = config["MYSQL"]["host"]
mysqlUser = config["MYSQL"]["user"]
mysqlPasswd = config["MYSQL"]["passwd"]
mysqlDatabase = config["MYSQL"]["database"]