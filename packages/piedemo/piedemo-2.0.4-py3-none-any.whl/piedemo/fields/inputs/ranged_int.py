import os
from .base import InputField


class InputRangedIntField(InputField):
    def __init__(self, name,
                 optional=False,
                 minValue=0,
                 maxValue=100,
                 stepValue=1,
                 formatLabel=""):
        super(InputRangedIntField, self).__init__(name,
                                                  optional=optional)
        self.minValue = minValue
        self.maxValue = maxValue
        self.stepValue = stepValue
        self.formatLabel = formatLabel

    def generate(self):
        return {
            "card": "RangeCard",
            "data": {
                "name": self.name,
                "minValue": self.minValue,
                "maxValue": self.maxValue,
                "step": self.stepValue,
                "formatLabel": self.formatLabel,
                "isRange": False,
                "optional": self.optional
            }
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None

        return int(data)
