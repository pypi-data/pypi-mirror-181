from ..base import Field


class OutputField(Field):
    def __init__(self, name):
        super(OutputField, self).__init__(name=name)

    def set_output(self, *args, **kwargs):
        pass
