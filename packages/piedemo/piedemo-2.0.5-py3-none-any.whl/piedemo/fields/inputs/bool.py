import os
from .base import InputField


class InputBoolField(InputField):
    def __init__(self,
                 name,
                 flags,
                 optional=False):
        super(InputBoolField, self).__init__(name,
                                             optional=optional)
        self.flags = flags

    def generate(self):
        return {
            "card": "BoolCard",
            "data": {
                "name": self.name,
                "optional": self.optional,
                "flags": self.flags,
            }
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None
        if data == "on":
            return True
        return False
