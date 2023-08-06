import os

from .base import Field


class Navigation(Field):
    def __init__(self, fields, links=None):
        super(Navigation, self).__init__(None)
        if links is None:
            links = []
        self.links = links
        self.fields = fields

    def __getitem__(self, index):
        return self.fields[index]

    def add_link(self, name, href):
        self.links.append({'name': name, 'href': href})

    @property
    def link(self):
        return {self.links[i]['name']: self.links[i] for i, link in enumerate(self.links)}

    def generate(self):
        return {
            "card": "Navigation",
            "links": self.links,
            "content": self.fields.generate()
        }

    def children(self):
        return self.fields.children()

    def clear(self):
        self.fields.clear()

    def __repr__(self):
        return f"Navigation({self.links}); {repr(self.fields)}"

    def set_output(self, data):
        self.fields.set_output(data)

    def parse(self, data):
        return self.fields.parse(data)
