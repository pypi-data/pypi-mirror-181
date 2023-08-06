import os
from .base import OutputField
from typing import List


class ColoredSpan(object):
    def __init__(self, span,
                 color='#000000',
                 background='#FFFFFF'):
        self.span = span
        self.color = color
        self.background = background


class OutputColoredTextField(OutputField):
    def __init__(self, name,
                 default=""):
        super(OutputColoredTextField, self).__init__(name)
        self.value = default

    def generate(self):
        return {
            "card": "OutputColoredTextCard",
            "data": {
                "name": self.name,
                "value": self.value,
            }
        }

    def clear(self):
        self.default = ""

    def set_output(self, data):
        self.value = data

    @staticmethod
    def colorify(text, colored_spans: List[ColoredSpan]):
        output_text = ''
        colored_spans = sorted(colored_spans, key=lambda x: x.span[0])
        k = 0
        for s in colored_spans:
            if k > s.span[0]:
                raise RuntimeError("Bad spans")
            output_text += text[k: s.span[0]]
            output_text += '<span style="color: %s; background: %s;">' % (s.color, s.background) + text[s.span[0]: s.span[1]] + '</span>'
            k = s.span[1]

        output_text += text[k:]
        return output_text

    @staticmethod
    def hx(text, n):
        return f"<h{n}>" + text + f"</h{n}>"

    @staticmethod
    def new_line():
        return "<br />"
