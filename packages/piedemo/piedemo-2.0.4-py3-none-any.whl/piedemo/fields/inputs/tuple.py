import os
import os
from .base import InputField


class InputTupleField(InputField):
    def __init__(self, name, types,
                 optional=False):
        super(InputTupleField, self).__init__(name,
                                              optional=optional)
        self.types = types

    def generate(self):
        return {
            "card": "TupleCard",
            "data": {
                "name": self.name,
                "length": len(self.types),
                "types": [t.__name__ for t in self.types],
                "optional": self.optional
            }
        }

    def parse(self, data):
        if self.optional and hasattr(data, 'disabled') and data.disabled == 'on':
            return None

        data = data.split('\n')
        if len(self.types) != len(data):
            raise RuntimeError("Input tuple didn't match frontend")
        return tuple(map(lambda a: a[0](a[1].replace('\r', '')), zip(self.types, data)))
