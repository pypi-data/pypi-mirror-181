import os
import io
import base64

from piedemo.fields.outputs.base import OutputField


class PolyLine(object):
    def __init__(self,
                 points,
                 color,
                 tension=0.,
                 closed=False,
                 ):
        self.points = points
        self.color = color
        self.tension = tension
        self.closed = closed

    def to_json(self):
        return {
            "type": "Line",
            "points": self.points.reshape(-1).tolist(),
            "stroke": self.color,
            "tension": self.tension,
            "closed": self.closed,
            "x": 0,
            "y": 0,
        }


class OutputCanvasField(OutputField):
    def __init__(self, name, default=None):
        if default is None:
            default = {}
        super(OutputCanvasField, self).__init__(name)
        self.data = default

    def set_output(self, data):
        self.data = data

    def generate(self):
        background = self.data["background"]
        width, height = background.size
        img = background
        file_object = io.BytesIO()
        img.save(file_object, 'JPEG')
        file_object.seek(0)
        b64 = base64.b64encode(file_object.read()).decode('utf-8')

        return {
            "card": "OutputCanvasCard",
            "data": {
                "name": self.name,
                "background": f"data:image/jpeg;charset=utf-8;base64, {b64}",
                "width": width,
                "height": height,
                "shapes": list(map(lambda x: x.to_json(), self.data["shapes"]))
            }
        }

    def clear(self):
        self.data = {}
