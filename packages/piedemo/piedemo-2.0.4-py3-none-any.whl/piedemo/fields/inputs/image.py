import os
import numpy as np
from PIL import Image
import cv2
from .base import InputField


class InputImageField(InputField):
    def __init__(self, name, optional=False):
        super(InputImageField, self).__init__(name=name,
                                              optional=optional)

    def generate(self):
        return {
            "card": "ImageCard",
            "data": {"name": self.name,
                     "optional": self.optional}
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None

        return Image.open(data)

    def __repr__(self):
        return "InputImageField(%s)" % self.name
