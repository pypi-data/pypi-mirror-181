import os
from .image import OutputImageField


class OutputImageWithSegmentationField(OutputImageField):
    def __init__(self, name):
        super(OutputImageWithSegmentationField, self).__init__(name)

    def set_output(self, data):

        pass
