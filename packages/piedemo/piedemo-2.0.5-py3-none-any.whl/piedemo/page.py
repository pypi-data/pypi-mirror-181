import os
import copy

from .fields.grid import HStack, VStack, Stack, stack_contents
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
        if len(kwargs) == 0 or all([v is None for v in kwargs.values()]):
            return to
        params = '&'.join([f"{k}={v}" for k, v in kwargs.items() if v is not None])
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
        return stack_contents([
            page.get_content(**kwargs),
            hidden_field.generate()
        ])

    def process(self, **data):
        page = self.pages_mapping[data.pop("__page_variant")]
        return page.process(**data)


class ContentError(Exception):
    def __init__(self, data=None, redirect_url=None):
        super(ContentError, self).__init__()
        self.data = data
        self.redirect_url = redirect_url


class PageWithError(Page):
    def __init__(self, page,
                 default_redirect_url):
        super(PageWithError, self).__init__()
        self.page = page
        self.error_field = VStack([
            OutputJSONField("Error"),
            InputHiddenField("RedirectUrl", None)
        ])
        self.hidden_field = InputHiddenField("__page_variant", None)
        self.default_redirect_url = default_redirect_url

    def get_content(self, **kwargs):
        try:
            content = self.page.get_content(**kwargs)
            hidden_field = copy.deepcopy(self.hidden_field)
            hidden_field.set_output("normal")
            return stack_contents([content, hidden_field.generate()])
        except ContentError as e:
            error_field = copy.deepcopy(self.error_field)
            error_field["Error"].set_output(e.data)
            error_field["RedirectUrl"].set_output(e.redirect_url or self.default_redirect_url)
            content = error_field.generate()
            hidden_field = copy.deepcopy(self.hidden_field)
            hidden_field.set_output("error")
            return stack_contents([content, hidden_field.generate()])

    def process(self, **data):
        page_variant = data.pop("__page_variant")
        if page_variant == "normal":
            try:
                return self.page.process(**data)
            except:
                return self.default_redirect_url
        elif page_variant == "error":
            return data.get("RedirectUrl", self.default_redirect_url)
        else:
            return self.default_redirect_url
