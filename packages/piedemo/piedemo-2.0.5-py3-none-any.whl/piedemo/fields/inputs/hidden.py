import os
import numpy as np
from PIL import Image
import cv2
import json
from .base import InputField
from ..outputs.base import OutputField


class InputHiddenField(InputField, OutputField):
    def __init__(self, name,
                 value,
                 optional=False):
        super(InputHiddenField, self).__init__(name=name,
                                               optional=optional)
        self.value = value

    def generate(self):
        return {
            "card": "HiddenCard",
            "data": {"name": self.name,
                     "optional": self.optional,
                     "hidden_value": json.dumps(self.value)}
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None
        return json.loads(data)

    def __repr__(self):
        return "InputHiddenField(%s)" % self.name

    def clear(self):
        self.value = {}

    def set_output(self, data):
        self.value = data
