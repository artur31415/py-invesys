import json

class Element(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def ToString(self):
        return self.name + " = R$ " + str(self.value) + " Reais"

    def ToJson(self):
        jsonObj = {
            "name": self.name,
            "value": self.value
        }

        return json.dumps(jsonObj)

    
        