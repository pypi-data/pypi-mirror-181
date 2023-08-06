import copy
from pathlib import Path

from .fields.outputs.json import OutputJSONField
from .web import Web
from .page import Page
from .cache import Cache, try_int


class InputPage(Page):
    def __init__(self,
                 fields,
                 demo_function,
                 cache):
        super(InputPage, self).__init__()
        self.fields = fields
        self.demo_function = demo_function
        self.cache = cache

    def get_content(self, **kwargs):
        return self.fields.generate()

    def process(self, **data):
        data = self.parse(self.fields, data)
        output_data = self.demo_function(**data)
        output_id = self.cache.store(data=data, output_data=output_data)
        return f'/outputs?output_id={output_id}'


class OutputPage(Page):
    def __init__(self, fields,
                 cache):
        super(OutputPage, self).__init__()
        self.fields = fields
        self.cache = cache
        self.error_fields = OutputJSONField("Error")

    def get_content(self, **kwargs):
        output_id = try_int(kwargs.get("output_id", -1), other=-1)
        output_data = self.cache.get(output_id)["output_data"]
        if output_id == -1:
            error_fields = copy.deepcopy(self.error_fields)
            error_fields.set_output("output_id < 0")
            return error_fields.generate()
        return self.fill(self.fields, output_data)

    def process(self, **data):
        return '/inputs'


class WebDemo(Web):
    def __init__(self,
                 name="PieDataWebDemo",
                 demo_function=lambda x: x,
                 inputs=None,
                 outputs=None,
                 aggregation_rule='by_underscore',
                 cache_path='./.cache'):
        cache = Cache(Path(cache_path))
        super(WebDemo, self).__init__(name=name,
                                      pages={"inputs": InputPage(inputs, demo_function,
                                                                 cache=cache),
                                             "outputs": OutputPage(outputs,
                                                                   cache=cache)},
                                      aggregation_rule=aggregation_rule)
