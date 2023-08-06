import os
import os
from .base import InputField


class InputIntListField(InputField):
    def __init__(self, name, optional=False):
        super(InputIntListField, self).__init__(name,
                                                optional=optional)

    def generate(self):
        return {
            "card": "TagsCard",
            "data": {
                "name": self.name,
                "optional": self.optional,
                "isIntOnly": True,
            }
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None
        return list(map(int, list(filter(lambda x: len(x) > 0, data.split(', ')))))
