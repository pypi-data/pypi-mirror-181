from .base import OutputField
from .json import OutputJSONField
from ..grid import VStack
from ..inputs.base import InputField
from ..inputs.hidden import InputHiddenField


class Error(OutputField, InputField):
    def __init__(self):
        super(Error, self).__init__("Error")
        self.fields = VStack([
            OutputJSONField("Error"),
            InputHiddenField("ErrorData", None),
            InputHiddenField("ErrorCode", None)
        ])

    def generate(self):
        return self.fields.generate()

    def parse(self, data):
        pass
