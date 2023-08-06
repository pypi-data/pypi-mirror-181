import os
from .base import InputField


class InputTextField(InputField):
    def __init__(self, name,
                 default="",
                 languages=None,
                 isArea=False,
                 optional=False):
        super(InputTextField, self).__init__(name,
                                             optional=optional)
        self.default = default
        self.languages = languages
        self.isArea = isArea

    def generate(self):
        if self.languages is None:
            return {
                "card": "TextCard",
                "data": {
                    "name": self.name,
                    "optional": self.optional,
                    "defaultValue": self.default,
                    "isArea": self.isArea,
                }
            }
        else:
            return {
                "card": "TranslatableTextCard",
                "data": {
                    "name": self.name,
                    "optional": self.optional,
                    "defaultValue": self.default,
                    "languages": self.languages,
                    "isArea": self.isArea,
                }
            }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None

        return str(data)

    def clear(self):
        self.default = ""
