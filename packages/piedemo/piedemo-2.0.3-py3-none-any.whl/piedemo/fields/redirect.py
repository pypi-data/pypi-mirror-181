from .base import Field


class SubmitButton(Field):
    def __init__(self, name, url):
        super(SubmitButton, self).__init__(name)
        self.default_url = self.url = url

    def set_output(self, data):
        self.url = data

    def clear(self):
        self.url = self.default_url

    def generate(self):
        return {
            "card": "RedirectCard",
            "data": {
                "name": self.name,
                "redirect_url": self.url
            }
        }

    def parse(self, data):
        pass
