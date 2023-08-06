import os
import copy

from .fields.grid import HStack, VStack, Stack
from .fields.inputs.hidden import InputHiddenField
from .fields.outputs.json import OutputJSONField
from .fields.outputs.base import OutputField
from .web import Web


class Page(object):
    def __init__(self):
        super(Page, self).__init__()

    def get_content(self, **kwargs):
        raise NotImplementedError()

    def process(self, **data) -> str:
        raise NotImplementedError()

    @staticmethod
    def fill(fields, data,
             inplace=False,
             generate=True,
             hook=lambda a, b: None):
        if not inplace:
            fields = copy.deepcopy(fields)
        name2field = {f.name: f for f in fields.children() if isinstance(f, OutputField)}
        for key in data.keys():
            if key in name2field:
                name2field[key].set_output(data[key])
        hook(fields, data)
        if generate:
            return fields.generate()
        return fields

    @staticmethod
    def parse(fields, data):
        key2field = {f.name: f for f in fields.children()}
        for k in list(data.keys()):
            if k not in key2field:
                del data[k]
                continue
            data[k] = key2field[k].parse(data[k])
        return data

    @staticmethod
    def create_link(text, href):
        return f"""
        <a href="{href}">{text}</a>
        """

    @staticmethod
    def redirect_url(to, **kwargs):
        if len(kwargs) == 0:
            return to
        params = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
        return f"{to}?{params}"

    @staticmethod
    def add_field(fields, f):
        if isinstance(fields, (Stack, HStack, VStack)):
            fields.fields.append(f)
            fields.xs.append(fields.xs[-1])
        else:
            return VStack([fields, f])


class PageVariant(Page):
    def __init__(self, pages_mapping):
        super(PageVariant, self).__init__()
        self.pages_mapping = pages_mapping
        self.hidden_field = InputHiddenField("__page_variant", None)

    def choose_page(self, **kwargs):
        raise NotImplementedError()

    def get_content(self, **kwargs):
        idx = self.choose_page(**kwargs)
        page = self.pages_mapping[idx]
        hidden_field = copy.deepcopy(self.hidden_field)
        hidden_field.set_output(idx)
        return [[{"content": page.get_content(**kwargs), "xs": ""},
                 {"content": hidden_field.generate(), "xs": ""}]]

    def process(self, **data):
        page = self.pages_mapping[data.pop("__page_variant")]
        return page.process(**data)


class ErrorPage(Page):
    def __init__(self, data, redirect_url):
        super(ErrorPage, self).__init__()
        self.error_field = OutputJSONField("Error")
        self.error_field.set_output(data)
        self.url = redirect_url

    def get_content(self, **kwargs):
        return self.error_field.generate()

    def process(self, **data):
        return self.url


class PageWithError(PageVariant):
    def __init__(self, errors):
        super(PageWithError, self).__init__({
            "normal": self,
        })

    def choose_page(self, **kwargs):
        try:
            content = self.get_content(**kwargs)
        except:
            return "error"

    def get_content(self, **kwargs):
        raise NotImplementedError()

    def process(self, **data):
        return self.redirect_url
