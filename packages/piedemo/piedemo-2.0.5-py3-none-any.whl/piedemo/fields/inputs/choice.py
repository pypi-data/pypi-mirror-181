import os
import os
from .base import InputField


class InputChoiceField(InputField):
    def __init__(self,
                 name,
                 choices,
                 enum_type=None,
                 use_values=False,
                 colors=None,
                 default=None,
                 readonly=False,
                 optional=False):
        super(InputChoiceField, self).__init__(name,
                                               optional=optional)
        self.choices = choices
        self.enum_type = enum_type
        self.use_values = use_values
        self.readonly = readonly
        if colors is not None:
            assert len(colors) == len(choices)
        else:
            colors = ["#FFFFFF" for _ in range(len(choices))]
        self.colors = colors
        if default is None:
            default = self.choices[0]
        self.default = default

    def generate(self):
        return {
            "card": "ChoiceCard",
            "data": {
                "name": self.name,
                "optional": self.optional,
                "choices": self.choices,
                "colors": self.colors,
                "defaultValue": self.default,
                "readOnly": self.readonly,
            }
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None
        if self.enum_type is None:
            return data
        enum_member = getattr(self.enum_type, data)
        if self.use_values:
            return enum_member.value
        return enum_member
