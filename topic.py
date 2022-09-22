# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, line-too-long

class Topic:
    def __init__(self, topic, topic_type, device):
        self.topic = topic
        self.type = topic_type
        self.device = device
        self.sensores = {}
