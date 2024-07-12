import configparser
import os
import dashscope


class ResultAnalyzer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("conf/conf.ini")
        self.api_key = config.get("dashScope", "DASHSCOPE_API_KEY")
        self.model_name = config.get("dashScope", "MODEL_NAME")
        self.client = dashscope.Generation()

    def analyze(self, prompt):

        return content
