import requests


class ChuckFact:

    def __init__(self):
        self.version = "0.1"
        self.api_url = "http://jsalvador.pythonanywhere.com/"

    def get_version(self):
        return self.version

    def get_fact(self):
        return requests.get(self.api_url).content.decode()
