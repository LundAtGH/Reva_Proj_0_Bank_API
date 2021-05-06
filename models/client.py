class Client:

    def __init__(self, holder_id=0, name=""):
        self.holder_id = holder_id
        self.name = name

    def json(self):
        return {
            "holderId": self.holder_id,
            "name": self.name
        }

    @staticmethod
    def json_parse(json):
        client = Client()
        client.holder_id = json["holderId"] if "holderId" in json else 0
        client.name = json["name"]
        return client

    def __repr__(self):
        return str(self.json())
