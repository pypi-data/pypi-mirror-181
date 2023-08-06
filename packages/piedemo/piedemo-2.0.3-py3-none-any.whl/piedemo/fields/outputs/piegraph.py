import io
import base64
import json
import numpy as np
from .base import OutputField
import pandas as pd
from typing import Optional


class PieGraph(list):
    def __init__(self, data=[]):
        super(PieGraph, self).__init__(data)


class OutputPieGraphField(OutputField):
    def __init__(self, name):
        super(OutputPieGraphField, self).__init__(name=name)
        self.data = None

    def set_output(self, data: PieGraph):
        self.data = data

    def generate(self):
        return {
            "card": "OutputPieGraphCard",
            "data": {
                "name": self.name,
                "distribution": self.data,
            }
        }

    def clear(self):
        self.data = None

    def __repr__(self):
        return "OutputPieGraphField(%s)" % self.name
