import io
import base64
from .base import OutputField


class OutputVideoField(OutputField):
    def __init__(self, name):
        super(OutputVideoField, self).__init__(name=name)
        self.video = None

    def set_output(self, data):
        self.video = data

    def generate(self):
        pass

        return {
            "card": "OutputVideoCard",
            "data": {
                "name": self.name,
            }
        }

    def clear(self):
        self.video = None
