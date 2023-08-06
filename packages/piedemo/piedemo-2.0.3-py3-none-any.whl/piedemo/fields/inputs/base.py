import os
from ..base import Field


class InputField(Field):
    def __init__(self, name, optional=False):
        super(InputField, self).__init__(name=name)
        self.optional = optional
