import io
import base64
import json
from .base import OutputField
import pandas as pd
from typing import Optional


class OutputJSONField(OutputField):
    def __init__(self, name):
        super(OutputJSONField, self).__init__(name=name)
        self.data = None

    def set_output(self, data):
        self.data = data

    def generate(self):
        return {
            "card": "OutputJSONCard",
            "data": {
                "name": self.name,
                "json_data": self.data,
            }
        }

    def clear(self):
        self.data = None
