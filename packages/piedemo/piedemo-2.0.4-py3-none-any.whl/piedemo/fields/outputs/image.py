import io
import base64
from .base import OutputField


class OutputImageField(OutputField):
    def __init__(self, name):
        super(OutputImageField, self).__init__(name=name)
        self.image = None

    def set_output(self, data):
        self.image = data

    def generate(self):
        img = self.image
        file_object = io.BytesIO()
        img.save(file_object, 'JPEG')
        file_object.seek(0)
        b64 = base64.b64encode(file_object.read()).decode('utf-8')

        return {
            "card": "OutputImageCard",
            "data": {
                "name": self.name,
                "src": f"data:image/jpeg;charset=utf-8;base64, {b64}"
            }
        }

    def clear(self):
        self.image = None
