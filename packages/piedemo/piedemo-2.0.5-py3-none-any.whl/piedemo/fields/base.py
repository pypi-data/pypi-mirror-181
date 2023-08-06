import os


class Field(object):
    def __init__(self, name):
        self.name = name

    def generate(self):
        raise NotImplementedError()

    def children(self):
        return [self]

    def clear(self):
        pass

    def get_child_by_name(self, name):
        result = [f for f in self.children() if f.name == name]
        if len(result) == 0:
            return None
        return result[0]
